# Умное твердотельное реле с анализом ШИМ

### Ссылки
- [Обсуждение в теме форума UNI](https://uni3d.store/viewtopic.php?t=527)
- [Как залить Sketch в Arduino?](https://alexgyver.ru/arduino-first)

### Описание проблемы
Твердотельное реле Zero-Cross в процессе работы пропустит только те полупериоды синусоидального напряжения питания, начало которых совпадёт с импульсами сигнала ШИМ от платы управления. В результате реле может находится в трёх состояниях: закрыто, открыто и открыто для одного полупериода. 


Например, при частоте питающего напряжения равной частоте ШИМ сигнала управления (50 Гц) и коэффициентом заполнения сигнала управления отличным от 1.0, можно говорить лишь о вероятности одного из трех состояний твердотельного реле.
- Коэффициент заполнения = 1.0 - полная мощность
- Коэффициент заполнения ≥ 0.5 - половина или полная мощность
- Коэффициент заполнения < 0.5 - 0 или половина мощности

<img src="https://github.com/demonlibra/smart_ssr/blob/master/oscilloscope/1.jpg" width="200"> <img src="https://github.com/demonlibra/smart_ssr/blob/master/oscilloscope/2.jpg" width="200"> <img src="https://github.com/demonlibra/smart_ssr/blob/master/oscilloscope/3.jpg" width="200"> <img src="https://github.com/demonlibra/smart_ssr/blob/master/oscilloscope/4.jpg" width="200">

Несоответствие выходной мощности может быть причиной больших отклонений температуры от заданной. 
Решить описанную проблему может следующее решение:

<img src="https://github.com/demonlibra/smart_ssr/blob/master/arduino/dimmer+arduino.jpg" width="400"> <img src="https://github.com/demonlibra/smart_ssr/blob/master/digispark/smart_ssr_digispark.jpg" width="400">

### Комплектующие
- Arduino или digispark
- [Димер от Robotdyn](https://robotdyn.aliexpress.ru/store/1950989/search?origin=n&SortType=new_desc&SearchText=dimmer)

### Принцип работы
1. Сигнал управления с платы управления  поступает вход Arduino, которая определяет длительность импульсов включения и коэффициент заполнения ШИМ.
2. Димер подаёт на Arduino сигналы перехода синусоиды напряжения через 0 для определения моментов времени открытия симистора. Таким образом достигается синхронизация сигнала управления и сетевого напряжения.
3. Arduino выдаёт сигналы управления на димер для получения необходимой мощности, пропуская в единицу времени часть полупериодов сетевого напряжения. Сетевое напряжение с частотой 50 Гц имеет 100 полупериодов за одну секунду. Например, если за секунду пропустить только 30 полупериодов, будет получено 30% мощности.
Дискретность задания мощности 1%.

<img src="https://github.com/demonlibra/smart_ssr/blob/master/oscilloscope/5.jpg" width="400">

Данное решение позволяет:
- Устранитть проблему неадекватной работы нагревателя с обычным твердотельным реле.
- Обеспечить более точное поддержание температуры.
- Задать ограничение мощности. Может быть актуально для мощных грелок, если стол искривляется от быстрого нагрева.

### Важно
У большинства всё работает и без этого велосипеда. Не торопитесь реализовывать данную схему.
В большинстве случаев проблема управления твердотельным реле решается понижением частоты ШИМ меньше 10 Гц.
