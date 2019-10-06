#!/bin/bash

stty 115200 -F /dev/ttyUSB0 raw -echo

echo "G28" > /dev/ttyUSB0

read -p "Нажмите ENTER выполнить перемещение к 1-й точке"

echo "G0 F800 Z10" > /dev/ttyUSB0
echo "G0 F1000 X20 Y20" > /dev/ttyUSB0
echo "G0 F500 Z0" > /dev/ttyUSB0

echo; read -p "Нажмите ENTER выполнить перемещение к 2-й точке"

echo "G0 F500 Z10" > /dev/ttyUSB0
echo "G0 F1000 X200" > /dev/ttyUSB0
echo "G0 F500 Z0" > /dev/ttyUSB0

echo; read -p "Нажмите ENTER выполнить перемещение к 3-й точке"

echo "G0 F500 Z10" > /dev/ttyUSB0
echo "G0 F1000 Y175" > /dev/ttyUSB0
echo "G0 F500 Z0" > /dev/ttyUSB0

echo; read -p "Нажмите ENTER выполнить перемещение к 4-й точке"

echo "G0 F500 Z10" > /dev/ttyUSB0
echo "G0 F1000 X20" > /dev/ttyUSB0
echo "G0 F500 Z0" > /dev/ttyUSB0

echo; read -p "Нажмите ENTER выполнить переместиться в безопасную зону"

echo "G0 F800 Z10 R" > /dev/ttyUSB0
echo "G0 F500 X20 Y20 Z50" > /dev/ttyUSB0
echo "M18" > /dev/ttyUSB0






