float power_limit = 0.5;              // Ограничение мощности 0.33 - 200Вт, 0.5 - 300Вт, 0.67 - 400Вт, 0.83 - 500Вт, 1 - 600Вт
                                      // Номинальная мощность грелки 600 Вт

const byte pwm_in = 6;                // Вход для сигнала ШИМ от Lerdge
const byte ZC_in = 3;                 // Вход контроля перехода синусоиды через ноль
const byte dimmer_out = 5;            // Выход управления димером
const int period = 20000;             // Время (мкс) периода напряжения в сети: 1/50Гц = 20мс = 20000мкс

int duty = 0;                         // Длительность импульсов ШИМ от Lerdge
float duty_cycle;                     // Скважность ШИМ от Lerdge
float radian;
int T = 10000;                        // Задержка включения симистора

uint32_t Lerdge_PWM_Start = micros(); // Время начала импульса ШИМ от платы Lerdge
uint32_t Lerdge_PWM_End = micros();   // Время окончание импульса ШИМ от платы Lerdge
uint32_t timer_ZC = micros();         // Время перехода синусоиды напряжения через ноль

uint32_t timer_debug = millis();      // Таймер вывода данных в терминал для отладки

byte Lerdge_PWM_state_Now = 1;
byte Lerdge_PWM_state_Before = 1;
byte ZC_before = 0;
byte ZC_now = 0;

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
  
  if (!Lerdge_PWM_state_Now && (micros() - Lerdge_PWM_Start > period)) duty = period; // Если нет импульсов и скважность 100%
  if ( Lerdge_PWM_state_Now && (micros() - Lerdge_PWM_Start > period)) duty = 0;      // Если нет импульсов и скважность 0%
  if (duty < 0 ) duty = 0;                                  // Устранение отрицательных значений в моменты смены скважности ШИМ

  duty_cycle = (float)duty / period;                        // Скважность ШИМ = Длительность импульса / период (20 мс)
  if (duty_cycle > power_limit) duty_cycle = power_limit;   // Ограничение мощности
  
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
    timer_ZC = micros();                                        // Запись времени перехода напряжения через ноль
    radian = acos(duty_cycle * 2 - 1);                          
    T = radian * period/2 / 3.14;                               // Момент времени открытия симистора
    
  }
  ZC_before = ZC_now;                                           // Сохранение текущего состояния

  // Активация симистора. Импульс необходимо выключить заблаговременно. Иначе спад импульса может оказаться после момент перехода фазы через ноль.
  if ((micros()-timer_ZC > T) && (micros()-timer_ZC < 9800)) digitalWrite(dimmer_out, HIGH);
  else digitalWrite(dimmer_out, LOW);

  // Вывод данных в терминал для отладки
  if (millis() - timer_debug > 1000 ) {
    //Serial.println("duty="+String(duty) + " duty_cycle=" + String(duty_cycle) + " T=" + String(T));
    //Serial.println(duty_cycle);
    timer_debug = millis();
  }
}
