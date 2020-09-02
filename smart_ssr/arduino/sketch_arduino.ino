// Умное твердотельное реле или Питание грелки без потери ШИМ
// Версия 3.3 от 14/08/2020
// http://uni3d.store/viewtopic.php?f=63&t=527



// ------------------ Проверьте параметры ниже ---------------------------------------------------------

unsigned int power_nominal = 600;     // Номинальная мощность грелки (Вт)
unsigned int power_limit   = 600;     // Ограничение максимальной мощности грелки (Вт)

const byte   freq_supply   = 50;      //  Частота напряжения в сети (Гц)
const byte   freq_pwm      = 50;      //  Частота ШИМ на выходе платы управления (Гц). Для Lerdge = 50, для Marlin = 8.

const byte   pwm_in        = 6;       // Вход ШИМ сигнала нагрева стола от платы управления принтером
const byte   ZC_in         = 3;       // Вход сигнала перехода синусоиды напряжения через ноль (Zero Cross)
const byte   dimmer_out    = 5;       // Выход управления димером (PWM)

// ------------------ Проверьте параметры выше ---------------------------------------------------------
// -----------------------------------------------------------------------------------------------------


const unsigned int period_supply = 1 * 1000000 / freq_supply;   // Период (мкс) напряжения в сети
const unsigned int period_pwm    = 1 * 1000000 / freq_pwm;         // Период (мкс) ШИМ сигнала на выходе платы управления

unsigned int T = period_supply / 2;   // Задержка включения симистора

float duty_cycle_limit = (float)power_limit / power_nominal;    // Ограничение мощности

int duty = 0;                         // Длительность импульсов ШИМ от платы управления принтером
float duty_cycle;                     // Скважность ШИМ от платы управления принтером
float radian;

uint32_t Lerdge_PWM_Start = micros(); // Время начала импульса ШИМ от платы управления принтером
uint32_t Lerdge_PWM_End   = micros(); // Время окончание импульса ШИМ от пплаты управления принтером
uint32_t timer_ZC         = micros(); // Время перехода синусоиды напряжения через ноль

unsigned int ZC_duration  = 0;        // Длительность импульса определения перехода синусоиды напряжения через ноль

uint32_t timer_debug      = millis(); // Таймер вывода данных в терминал для отладки

bool Lerdge_PWM_state_Now = 1;
bool Lerdge_PWM_state_Before = 1;
bool ZC_before = 0;
bool ZC_now = 0;
bool pwm_out = 0;

void setup() {
  pinMode(pwm_in, INPUT_PULLUP);
  pinMode(ZC_in, INPUT_PULLUP);
  pinMode(dimmer_out, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {

  Lerdge_PWM_state_Now = digitalRead(pwm_in);               // Текущее состояние ШИМ
  
  if (!Lerdge_PWM_state_Now && Lerdge_PWM_state_Before) {
    Lerdge_PWM_Start = micros();                            // Определение фронта импульса ШИМ сигнала
  }
  if (Lerdge_PWM_state_Now && !Lerdge_PWM_state_Before) {
    Lerdge_PWM_End = micros();                              // Определение спада импульса ШИМ сигнала
    duty = Lerdge_PWM_End - Lerdge_PWM_Start;               // Расчёт длительности импульса ШИМ сигнала
  }
  
  if (!Lerdge_PWM_state_Now && (micros() - Lerdge_PWM_Start > period_pwm)) duty = period_pwm; // Если нет импульсов и скважность 100%
  if ( Lerdge_PWM_state_Now && (micros() - Lerdge_PWM_Start > period_pwm)) duty = 0;          // Если нет импульсов и скважность 0%
  if (duty < 0 ) duty = 0;                                        // Устранение отрицательных значений в моменты смены скважности ШИМ

  duty_cycle = (float)duty / period_pwm;                    // Скважность ШИМ = Длительность импульса / период (20000 мкс)
  if (duty_cycle > duty_cycle_limit) duty_cycle = duty_cycle_limit;   // Ограничение мощности
  
  Lerdge_PWM_state_Before = Lerdge_PWM_state_Now;           // Сохранение состояния ШИМ (предыдущее состояние)


  // Расчет момента времени открытия симистора через пропорцию площади ШИМ и площади синусоиды:
  // ------------------------------------------------------------------------------------------
  //
  // Площадь полупериода синусоиды = 2
  // Необходимая площадь S = (Площадь полупериода синусоиды) х (Скважность) = duty_cycle x 2
  //
  // Площадь под аркой синусоиды S = cos(x1) - cos(x2)
  // Конец арки синусоиды совпадает с переходом через 0, т.е. x2 = Pi и cos(x2) = cos(Pi) = -1
  // 
  // duty_cycle x 2 = cos(x1) - (-1)
  // cos(x1) = duty_cycle x 2 - 1
  // radian = acos(duty_cycle * 2 - 1);                         // !!! Вычисление занимает около ~270 мкс
  //
  // Pi     <=> 10000 мс
  // radian <=> T
  //
  // T = radian * period/2 / 3.14;                              // Момент времени открытия симистора
  

  ZC_now = digitalRead(ZC_in);                                  // Текущее состояние триггера перехода напряжения через ноль

  if (ZC_now && !ZC_before) {                                   // Выполнять, если обнаружен фронт перехода напряжения через ноль
    pwm_out = 1;                                                // Триггер разрешения выдачи импульса открытия симистора
    timer_ZC = micros();                                        // Запись времени перехода напряжения через ноль
    radian = acos(duty_cycle * 2 - 1);                          
    T = radian * period_supply/2 / 3.1415;                      // Момент времени открытия симистора    
  }

  if (!ZC_now && ZC_before) ZC_duration = micros() - timer_ZC;  // Расчет длительности импульса определения перехода фазы через ноль

  ZC_before = ZC_now;                                           // Сохранение текущего состояния

  // Активация симистора. Импульс необходимо выключить заблаговременно. Иначе спад импульса может оказаться после момент перехода фазы через ноль.
  if ((micros() - timer_ZC > T + ZC_duration/2) && pwm_out && (T < period_supply/2)) {
    digitalWrite(dimmer_out, HIGH);                             // Фронт импульса открытия симистора
    pwm_out = 0;                                                // Обнуление триггера для обеспечения выдачи короткого импульса
    digitalWrite(dimmer_out, LOW);                              // Спад импульса открытия симистора
  } else {
    digitalWrite(dimmer_out, LOW);
  }
  

  // Вывод данных в терминал для отладки
  if (millis() - timer_debug > 1000 ) {
    //Serial.println("duty=" + String(duty) + " duty_cycle=" + String(duty_cycle) + " T=" + String(T));
    Serial.println(duty_cycle);
    //Serial.println("period_supply=" + String(period_supply) + " period_pwm=" + String(period_pwm));
    timer_debug = millis();
  }
}
