EESchema Schematic File Version 4
LIBS:lcr_ebox-cache
EELAYER 26 0
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
L Device:R R1
U 1 1 5AD08279
P 5550 2100
F 0 "R1" H 5480 2054 50  0000 R CNN
F 1 "2k" H 5480 2145 50  0000 R CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5480 2100 50  0001 C CNN
F 3 "~" H 5550 2100 50  0001 C CNN
	1    5550 2100
	-1   0    0    1   
$EndComp
$Comp
L Device:C C1
U 1 1 5AD08309
P 5950 2100
F 0 "C1" H 6065 2146 50  0000 L CNN
F 1 "22pF" H 6065 2055 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm" H 5988 1950 50  0001 C CNN
F 3 "~" H 5950 2100 50  0001 C CNN
	1    5950 2100
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01_Male J2
U 1 1 5AD0840E
P 6450 1700
F 0 "J2" H 6557 1878 50  0000 C CNN
F 1 "A" H 6557 1787 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 6450 1700 50  0001 C CNN
F 3 "~" H 6450 1700 50  0001 C CNN
	1    6450 1700
	-1   0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01_Male J3
U 1 1 5AD0847E
P 6450 2500
F 0 "J3" H 6557 2678 50  0000 C CNN
F 1 "B" H 6557 2587 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 6450 2500 50  0001 C CNN
F 3 "~" H 6450 2500 50  0001 C CNN
	1    6450 2500
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5550 1950 5550 1850
Wire Wire Line
	5550 1850 5750 1850
Wire Wire Line
	5950 1850 5950 1950
Wire Wire Line
	5550 2250 5550 2350
Wire Wire Line
	5550 2350 5750 2350
Wire Wire Line
	5950 2350 5950 2250
Wire Wire Line
	5750 2350 5750 2500
Wire Wire Line
	5750 2500 6250 2500
Connection ~ 5750 2350
Wire Wire Line
	5750 2350 5950 2350
Wire Wire Line
	6250 1700 5750 1700
Wire Wire Line
	5750 1700 5750 1850
Connection ~ 5750 1850
Wire Wire Line
	5750 1850 5950 1850
Wire Wire Line
	5750 1700 5200 1700
Connection ~ 5750 1700
Wire Wire Line
	5750 2500 5200 2500
Connection ~ 5750 2500
Wire Notes Line
	4950 2100 5050 2100
Wire Notes Line
	5000 2100 5000 2000
Wire Notes Line
	4950 2150 5050 2150
Wire Notes Line
	5000 2150 5000 2250
$Comp
L Connector_Generic:Conn_01x01_Female J1
U 1 1 5AD12BFC
P 5000 1700
F 0 "J1" H 5028 1726 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5028 1635 50  0000 L CNN
F 2 "Connector_Custom:Banana_Jack_1Pin_PCB" H 5000 1700 50  0001 C CNN
F 3 "~" H 5000 1700 50  0001 C CNN
	1    5000 1700
	-1   0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01_Female J4
U 1 1 5AD12C54
P 5000 2500
F 0 "J4" H 5028 2526 50  0000 L CNN
F 1 "Conn_01x01_Female" H 5028 2435 50  0000 L CNN
F 2 "Connector_Custom:Banana_Jack_1Pin_PCB" H 5000 2500 50  0001 C CNN
F 3 "~" H 5000 2500 50  0001 C CNN
	1    5000 2500
	-1   0    0    -1  
$EndComp
Text Notes 4450 2150 0    50   ~ 0
Messproben
$EndSCHEMATC
