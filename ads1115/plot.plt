set terminal pngcairo size 1000,700
set output "plot1.jpg"

set xrange [0:200]
set yrange [0:5]

set grid xtics lc rgb '#555555' lw 1 lt 0
set grid ytics lc rgb '#555555' lw 1 lt 0

set xtics axis
set ytics axis

set xlabel "Время, сек"
set ylabel "Ток, А"

set style line 1 lt 1 lw 3 lc rgb '#4682b4' pt -1

#plot 'ads1115+acs712_log' with lines title 'Ток в цепи 24VDC' ls 1

plot 'ads1115+acs712_log' using ($1*24) with lines title 'Потребялемая мощность цепи 24VDC' ls 1