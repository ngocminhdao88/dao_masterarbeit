function [C_F, R_p_ohm]=ladekurve_auswerten(ladekurve, t, stuetz_unten, stuetz_oben, R_lade_ohm, U_lade_volt)
% Auswerten eines Spannungsverlaufs (ladekurve) zur passenden Zeitbasis (t). Stuetzstellen
% als Datenpunkt. R_Lade_ohm in Ohm und U_Lade_volt in Volt




t1_sec = t(stuetz_unten);
U1_volt = ladekurve(stuetz_unten);
t2_sec = t(stuetz_oben);
U2_volt = ladekurve(stuetz_oben);

tau = (t2_sec - t1_sec)/(log(1 - U1_volt/U_lade_volt) - log(1 - U2_volt/U_lade_volt)); % Korrigiert Norbert
C_F=tau*(1/R_lade_ohm);

% Parallelwiderstand nicht betrachten und auf Null setzen
R_p_ohm=0;

% % disp('End ladekurve_auswerten')
end
