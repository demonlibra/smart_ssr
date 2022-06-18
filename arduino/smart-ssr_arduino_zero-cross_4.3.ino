// Умное твердотельное реле (Smart-SSR) или "Питание грелки 220В без потери ШИМ"
// Sketch для Arduino
// Версия 4.3 от 05/09/2020
// Вариант Zero-Cross с равномерным распределением включений симистора
// Обсуждение: http://uni3d.store/viewtopic.php?f=63&t=527
// Файлы проекта: https://github.com/demonlibra/uni/tree/master/smart_ssr


// ------------------ Проверьте параметры ниже ---------------------------------------------------------

const uint16_t power_nominal = 600;   // Номинальная мощность грелки (Вт)
const uint16_t power_limit   = 350;   // Ограничение максимальной мощности грелки (Вт)

const byte   freq_supply   = 50;      //  Частота напряжения в сети (Гц)
const byte   freq_pwm      = 50;      //  Частота ШИМ на выходе платы управления (Гц). Для Lerdge = 50, для Marlin = 8.
const byte   update_pwm    = 1;       //  Периодичность изменения ШИМ на выходе платы управления (раз в секунды). Для Lerdge = 1, для Marlin = ???.

const byte   pwm_in        = 6;       // Вход ШИМ сигнала нагрева стола от платы управления принтером
const byte   ZC_in         = 3;       // Вход сигнала перехода синусоиды напряжения через ноль (Zero Cross)
const byte   dimmer_out    = 5;       // Выход управления димером (PWM)

// ------------------ Проверьте параметры выше ---------------------------------------------------------
// -----------------------------------------------------------------------------------------------------

const byte freq_supply_zc   = freq_supply * 2;                   // Количество полупериодов питающего напряжения
const uint32_t period_pwm   = 1000000 / freq_pwm;                // Период (мкс) ШИМ сигнала на выходе платы управления
const byte duty_cycle_limit = 100 * power_limit / power_nominal; // Ограничение мощности через скважность

uint32_t duty = 0;                    // Длительность импульсов ШИМ от платы управления принтером
byte duty_cycle = 0;                  // Расчётная скважность ШИМ от платы управления принтером

byte duty_cycle_count = 0;            // Счётчик полупериодов, которые нужно открыть
byte zc_count = freq_supply_zc;       // Счётчик переходов через ноль

byte skip = 0;                        // Пропуск полупериодов для равномерного распределения
byte skip_count = 0;                  // Счётчик пропуска полупериодов

uint32_t Lerdge_PWM_Start = micros(); // Время начала импульса ШИМ от платы управления принтером
uint32_t Lerdge_PWM_End   = micros(); // Время окончание импульса ШИМ от пплаты управления принтером
uint32_t timer_debug;                 // Таймер вывода данных в последовательный порт    

bool Lerdge_PWM_state_Now = 1;        // Текущее состояние сигнала ШИМ (сигнал инвертирован)
bool Lerdge_PWM_state_Before = 1;     // Предыдущее состояние сигнала ШИМ (сигнал инвертирован)
bool ZC_now = 0;                      // Текущее состояние сигнала Zero-Cross
bool ZC_before = 0;                   // Предыдущее состояние сигнала Zero-Cross

void setup() {
  pinMode(pwm_in, INPUT_PULLUP);      // Назначение входа для сигнала ШИМ от платы управления
  pinMode(ZC_in, INPUT_PULLUP);       // Назначение входа для сигнала Zero-Cross от димера
  pinMode(dimmer_out, OUTPUT);        // Назначение выхода управления димером

  //Serial.begin(9600);
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

  ZC_now = digitalRead(ZC_in);                              // Запись текущего состояния триггера Zero-Cross

  if (!ZC_now && ZC_before) {                               // Обнаружение спада импульса Zero-Cross
    if (zc_count > 0) zc_count -= 1;                        // Пересчет сигналов Zero-Cross в течении одной секунды
    else {
      zc_count = freq_supply_zc;                            // Сброс счётчика пересчёта сигналов Zero-Cross
      duty_cycle_count = duty_cycle;                        // Сколько полупериодов открыть симистор
      skip = (freq_supply_zc / duty_cycle_count) - 1;       // Первичный расчёт пропуска полупериодов для равномерного распределения
      //Serial.println(duty_cycle);
    }
  }
   
  
  // Активация симистора
  if ((!ZC_now && ZC_before) && (duty_cycle_count > 0)) {
    if (skip_count > 0) skip_count -= 1;
    else                skip_count = skip;                  // Сброс счётчика пропуска полупериодов

    if (skip_count == 0) {
      digitalWrite(dimmer_out, HIGH);                       // Фронт импульса открытия симистора
      digitalWrite(dimmer_out, LOW);                        // Спад импульса открытия симистора
      duty_cycle_count -= 1;                                // Сколько осталось выполнить открытий симистора

      // Остаток количества возможных моментов включения делится на остаток необходимых включений
      // Если > 1, т.е. 2, то значение первичного пропуска увеличивается на 1
      if ((((freq_supply_zc - zc_count) / duty_cycle_count) > 1) && (skip == 0)) skip += 1;
    } 
  }
  ZC_before = ZC_now;                                       // Сохранение текущего состояния сигнала Zero-Cross

}
