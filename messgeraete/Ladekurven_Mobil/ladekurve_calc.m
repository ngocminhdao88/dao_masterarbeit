function  [kurve_mess, kurve_ideal] = ladekurve_calc( C_calc_F, R_p_ohm, kurve, zeitbasis, R_lade_ohm, U_lade_volt, stuetz_unten, stuetz_oben, inkrement, messung, messinfo)
%Erzeugt eine berechnete Ladekurve

u1=kurve(stuetz_unten);
% u2=glattekurve(stuetz_oben);
syms t
t1=solve(U_lade_volt*(1-exp(-t/(R_lade_ohm*C_calc_F)))==u1, t);
% t2=solve(U_lade*(1-exp(-t/(R_lade*C)))==u2, t)

%delta_t=double(zeitbasis(stuetz_unten)-t1);
delta_t=0;

for i=1:size(zeitbasis)
    
    
    y_calc_volt(i,:) = U_lade_volt*(1-exp(-zeitbasis(i)/(R_lade_ohm*C_calc_F)));
    %zeitbasis_mod(i,:)=zeitbasis(i)+delta_t;
end

%plot(zeitbasis_mod,y_calc_volt);

h.fig2 = figure(1002);
h.fig2.Position = [226, 175, 1352, 849];
clf
hold on
plot(zeitbasis, kurve);
plot(zeitbasis, y_calc_volt);

% Eingefügt Norbert 14.08.2015
% Plotte die berechnete Kurve gestrichelt nochmal auf die
% Origignalkurve
Ushift = find(y_calc_volt >= u1,1);
shift = stuetz_unten - Ushift;
shifter(1:shift,1) = 0;
plot(zeitbasis, [shifter; y_calc_volt(1:end-shift)],'--r')
xlabel('Zeit in s \rightarrow')
ylabel('Spannung in V \rightarrow')
title(['Inkrement: ',num2str(inkrement),' Messung: ', num2str(messung)])

kurve_mess=kurve;
kurve_ideal=y_calc_volt;
 savefig(h.fig2, [messinfo,'\Ladekurve_ausgewertet_Inc_',num2str(inkrement),'_Messung',num2str(messung)]);
saveas(h.fig2, [messinfo,'\Ladekurve_ausgewertet_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);


end

