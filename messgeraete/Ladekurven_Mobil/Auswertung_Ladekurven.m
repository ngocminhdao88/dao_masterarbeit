clf;
clear;

% Aufrufen des Einleseskripts

[Ladekurven, name, Einstellungen] = ladekurven_einlesen;



% Aufrufen des Auswerteskripts

  % Feste Daten
   U_Lade_V = Einstellungen{1,5};
    R_Lade_ohm = Einstellungen{1,3}; % in Ohm
    Samplerate = Einstellungen{1,6};
    Filterlaenge=10;
 
% Anpassung der Ladespannung auf systemimmanenten Parallelwiderstand

R_P_Ohm = 370500; % in Ohm

U_Lade_V_sys = U_Lade_V;
U_Lade_V = (R_P_Ohm * U_Lade_V_sys)/(R_P_Ohm + R_Lade_ohm);
    
messinfo=name;
figureordner = strcat(name, '\figures');
mkdir(figureordner);
ladekurven_abarbeiten;
