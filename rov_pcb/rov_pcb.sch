EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 5F3C6808
P 5500 3000
F 0 "J1" H 5500 4481 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 5500 4390 50  0000 C CNN
F 2 "" H 5500 3000 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 5500 3000 50  0001 C CNN
	1    5500 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 1400 5400 1400
Wire Wire Line
	5400 1400 5400 1700
$Comp
L Sensor_Motion:MPU-6050 U?
U 1 1 5F43CD41
P 7150 4750
F 0 "U?" H 7150 3961 50  0000 C CNN
F 1 "MPU-6050" H 7150 3870 50  0000 C CNN
F 2 "Sensor_Motion:InvenSense_QFN-24_4x4mm_P0.5mm" H 7150 3950 50  0001 C CNN
F 3 "https://store.invensense.com/datasheets/invensense/MPU-6050_DataSheet_V3%204.pdf" H 7150 4600 50  0001 C CNN
	1    7150 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 2050 8150 1400
$Comp
L MCU_Module:Arduino_UNO_R3 A?
U 1 1 5F438123
P 8350 3050
F 0 "A?" H 8350 4231 50  0000 C CNN
F 1 "Arduino_UNO_R3" H 8350 4140 50  0000 C CNN
F 2 "Module:Arduino_UNO_R3" H 8350 3050 50  0001 C CIN
F 3 "https://www.arduino.cc/en/Main/arduinoBoardUno" H 8350 3050 50  0001 C CNN
	1    8350 3050
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
