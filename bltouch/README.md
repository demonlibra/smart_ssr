# Получение изображения поверхности стола при помощи BL-TOUCH/3D-TOUCH с платой Lerdge
# Mesure surface of table with BL-TOUCH/3D-TOUCH and Lerdge

## Почему так сделано?

После выполнения процедуры измерения стола (G29), Lerdge не выводит результаты в терминал.

## Как это работает?
Вместо выполнения общей команды измерения стола (G29) используется команда (G30) для измерения высот в заданных позициях.

## На чём это работает?
Проверено на Lerdge-K и Raspberry Pi 3B+ с операционной системой Raspbian, но должно работать на любой GNU/Linux операционной системе.

## Из чего состоит?
| Файл | Описание |
| ---- | -------- |
| `bltouch.sh` | Основной сценарий bash. Отправляет команды через UART, собирает и обрабатывает данные.|
| `bltouch_lerdge_output` | Вывод данных с UART. Преобразуется в файл `bltouch_mesh`. |
| `bltouch_mesh` | Массив точек. Подготовленный для обработки в `gnuplot`. |
| `bltouch_plot` | Сценарий для gnuplot. Формирует изображение (в формате png) поверхности из массива точек `bltouch_mesh`. |

## Подготовка
## Prepare

### Для построения изображения поверхности используется программа gnuplot
### For create image used gnuplot

For installation `gnuplot` run in terminal:  
Для установки `gnuplot` выполните в терминале:  
`sudo apt update`  
`sudo apt install gnuplot`

### Размещение файлов
### Place files
- Create folder `\home\username\bltouch`.
- Copy files `bltouch.sh` and `bltouch_plot`.

- Создайте каталог bltouch в домашнем каталоге.
- Скопируйте в каталог bltouch файлы `bltouch.sh` и `bltouch_plot`.

### Параметры
### Parameters
File `bltouch.sh` contain main parameters at the top.
В начале файла `bltouch.sh` задаются основные параметры:
- зона измерений
- количество точек
- ...

## Запуск
## Run
Open terminal in folder `\home\username\bltouch` and run command `bash bltouch.sh`.
Для запуск выполните в терминале `bash bltouch.sh`.

After finish mesure procedure You will get image `bltouch_plot.png`.
В результате будет создан файл `bltouch_plot.png` с изображением поверхности.

![bltouch_plot.png](https://github.com/demonlibra/uni/blob/master/bltouch/bltouch_plot.png)
