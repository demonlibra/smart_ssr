// Умное твердотельное реле или Питание грелки без потери ШИМ
// Версия 4.0 от 03/09/2020
// Для Arduino
// Вариант Zero-Cross
// http://uni3d.store/viewtopic.php?f=63&t=527
// https://github.com/demonlibra/uni/tree/master/smart_ssr


// ------------------ Проверьте параметры ниже ---------------------------------------------------------

const uint16_t power_nominal = 600;     // Номинальная мощность грелки (Вт)
const uint16_t power_limit   = 350;     // Ограничение максимальной мощности грелки (Вт)

const byte   freq_supply   = 50;      //  Частота напряжения в сети (Гц)
const byte   freq_pwm      = 50;      //  Частота ШИМ на выходе платы управления (Гц). Для Lerdge = 50, для Marlin = 8.

const byte   pwm_in        = 6;       // Вход ШИМ сигнала нагрева стола от платы управления принтером
const byte   ZC_in         = 3;       // Вход сигнала перехода синусоиды напряжения через ноль (Zero Cross)
const byte   dimmer_out    = 5;       // Выход управления димером (PWM)

// ------------------ Проверьте параметры выше ---------------------------------------------------------
// -----------------------------------------------------------------------------------------------------

const byte freq_supply_zc = freq_supply * 2;

const uint32_t period_pwm    = 1000000 / freq_pwm;      // Период (мкс) ШИМ сигнала на выходе платы управления

const byte duty_cycle_limit = 100 * power_limit / power_nominal;    // Ограничение мощности через скважность

uint32_t duty = 0;                    // Длительность импульсов ШИМ от платы управления принтером
byte duty_cycle;                      // Скважность ШИМ от платы управления принтером

byte duty_cycle_count = 0;                       // Счётчик полупериодов, которые нужно открыть
byte zc_count = freq_supply_zc;       // Счётчик переходов через ноль

uint32_t Lerdge_PWM_Start = micros(); // Время начала импульса ШИМ от платы управления принтером
uint32_t Lerdge_PWM_End   = micros(); // Время окончание импульса ШИМ от пплаты управления принтером
uint32_t timer_debug;                 // Таймер вывода данных в последовательный порт    

bool Lerdge_PWM_state_Now = 1;
bool Lerdge_PWM_state_Before = 1;
bool ZC_before = 0;
bool ZC_now = 0;

void setup() {
  pinMode(pwm_in, INPUT_PULLUP);      // Назначение входа для сигнала ШИМ от платы управления
  pinMode(ZC_in, INPUT_PULLUP);       // Назначение входа для сигнала Zero-Cross от димера
  pinMode(dimmer_out, OUTPUT);        // Назначение выхода управления димером

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
  if (Lerdge_PWM_state_Now && (micros() - Lerdge_PWM_End > period_pwm)) duty = 0;             // Если нет импульсов и скважность 0%
  
  duty_cycle = 100 * duty / period_pwm;                               // Скважность ШИМ = Длительность импульса / период (20000 мкс)
  if (duty_cycle > duty_cycle_limit) duty_cycle = duty_cycle_limit;   // Ограничение мощности

  Lerdge_PWM_state_Before = Lerdge_PWM_state_Now;           // Сохранение предыдущего состояния сигнала ШИМ

  ZC_now = digitalRead(ZC_in);                              // Текущее состояние триггера Zro-Cross

  if (!ZC_now && ZC_before) {                               // Обнаружение спада импульса Zero-Cross
    if (zc_count > 0) {
      zc_count -= 1;                              // Пересчет сигналов Zero-Cross за одну секунду
    } else {
      zc_count = freq_supply_zc;                            // Сброс счётчика пересчёта сигналов Zero-Cross
      duty_cycle_count = duty_cycle;                                   // Запись текущей скважности сигнала ШИМ
    }
  }
   
  
  // Активации симистора
  if ((!ZC_now && ZC_before) && (duty_cycle_count > 0)) {
    duty_cycle_count -= 1;
    digitalWrite(dimmer_out, HIGH);                             // Фронт импульса открытия симистора
    digitalWrite(dimmer_out, LOW);                              // Спад импульса открытия симистора
  } else {
    digitalWrite(dimmer_out, LOW);                              // Контрольный спад импульса открытия симистора
  }
  ZC_before = ZC_now;                                           // Сохранение текущего состояния

  // Вывод данных в терминал для отладки
  if (millis() - timer_debug > 1000 ) {
    //Serial.println("duty=" + String(duty) + " duty_cycle=" + String(duty_cycle) + " T=" + String(T));
    Serial.println(duty);
    //Serial.println("period_supply=" + String(period_supply) + " period_pwm=" + String(period_pwm));
    timer_debug = millis();
  }
}
