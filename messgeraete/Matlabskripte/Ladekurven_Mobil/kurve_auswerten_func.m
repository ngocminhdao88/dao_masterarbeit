function [C_F, C_median_F, t0_s, t0_median_s] = kurve_auswerten_func (kurve, zeitbasis, U_Lade_V, R_Lade_Ohm, messinfo, inkrement, messung)
% Funktion um eine Ladekurve zu auszuwerten nach dem Verfahren von Blomeyer
% Gibt die Kapazität als Vektor und die Median-Kapazität zurück


% U_Lade_V    = 0.2;
% R_Lade_Ohm  = 509000;
Rsquare_Grenze = 0.995;
%%
%CorrSampleLength = 1000;
CorrSampleLength = round(size(kurve,1)*0.01);

Uc_V = kurve;
%Uc_V = U_blom;
Y = -R_Lade_Ohm .* log((1 - Uc_V./U_Lade_V));

Abtastrate_Hz = 4000000;
MesswertAnz = length(Uc_V);

%t_s = (0:1/Abtastrate_Hz:(MesswertAnz-1)/Abtastrate_Hz)';
t_s = zeitbasis;



h.fig = figure(1001);
clf
hold on
plot(t_s, Uc_V, 'b');
title(['Ladekurve: Inkrement: ',num2str(inkrement),' Messung: ', num2str(messung)])
xlabel('Zeit in s \rightarrow')
ylabel('Spannung in V \rightarrow')
savefig(h.fig, [messinfo,'\figures\Ladekurve_Inc_',num2str(inkrement),'_Messung',num2str(messung)]);
%saveas(h.fig, [messinfo,'\figures\Ladekurve_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);
print(h.fig,'-dpng',[messinfo,'\figures\Ladekurve_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);




CntTill = MesswertAnz;
CntFrom = CorrSampleLength+1;
R_sq(1:CntFrom) = NaN;
C_F(1:CntFrom) = NaN;
t0_s(1:CntFrom) = NaN;
for Cnt = CntFrom:1:CntTill
    
    Y_akt = Y(Cnt-CorrSampleLength:Cnt);
    t_akt = t_s(Cnt-CorrSampleLength:Cnt);
    %plot(t_akt, Y_akt, 'r')
    %     keyboard
    mm =  corrcoef(Y_akt, t_akt);
    R_sq(Cnt) = abs(mm(2).^2);
    if R_sq(Cnt) >= Rsquare_Grenze
        p = polyfit(t_s(Cnt-CorrSampleLength:Cnt), Y(Cnt-CorrSampleLength:Cnt),1);
        C_F(Cnt) = 1/p(1);
        t0_s(Cnt)=p(2);
    else
        C_F(Cnt) = NaN;
        t0_s(Cnt) = NaN;
    end
end

h.fig = figure(1002);
clf
hold on
plot(t_s, Y, 'r')
title(['Geradenform der Ladekurve Inkrement: ',num2str(inkrement),' Messung: ', num2str(messung)])
xlabel('Zeit in s \rightarrow')
ylabel('Kurve in Geradenform \rightarrow')
savefig(h.fig, [messinfo,'\figures\Ladekurve_gerade_Inc_',num2str(inkrement),'_Messung',num2str(messung)]);
%saveas(h.fig, [messinfo,'\figures\Ladekurve_gerade_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);
print(h.fig,'-dpng',[messinfo,'\figures\Ladekurve_gerade_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);

% Kurve noch einmal durchgehen und nur den ersten Block an Daten werten
Flag_Begin_Data=0;
Flag_End_Data=0;
Median_Start=1;
Median_Ende=1;
for i=1:1:CntTill
    if (Flag_Begin_Data==0)&&(Flag_End_Data==0)
        if isnan(C_F(i))
            C_F(i)=C_F(i);
            t0_s(i)=C_F(i);
        else
            C_F(i)=C_F(i);
            t0_s(i)=C_F(i);
            Flag_Begin_Data=1;
            Median_Start = i;
            Median_Ende = i;
        end
    elseif (Flag_End_Data==0)&&(Flag_Begin_Data==1)
        if isnan(C_F(i))
            Flag_End_Data=1;
            Median_Ende = i-1;
            C_F(i)=C_F(i);
            t0_s(i)=C_F(i);
        else
            C_F(i)=C_F(i);
            t0_s(i)=C_F(i);
        end
    elseif (Flag_End_Data==1)&&(Flag_Begin_Data==1)
        C_F(i)=NaN;
        t0_s(i)=NaN;
    end
end


max_c=1;
% Kurve plotten, falls ausgewertete Daten vorhanden
if (Flag_Begin_Data)
h.fig = figure(1003);
clf
hold on
[AX,H1,H2]= plotyy(t_s, Y, t_s, C_F);
%max_c = max(C_F);
%max_c=round(2*max_c,9);
if (max_c<0)
    max_c=1e-9;
end
%set(AX(2),'YLim',[0 max_c])
%set(AX(2),'YTick',[0:0.5e-9:max_c])

ylabel(AX(1),'Kurve in Geradenform \rightarrow') % left y-axis
ylabel(AX(2),'Kapazität in F') % right y-axis

title(['Kurve und Korrelation / Inkrement: ',num2str(inkrement),' Messung: ', num2str(messung)])
xlabel('Zeit in s \rightarrow')

savefig(h.fig, [messinfo,'\figures\Ladekurve_auswertung_Inc_',num2str(inkrement),'_Messung',num2str(messung)]);
%saveas(h.fig, [messinfo,'\figures\Ladekurve_auswertung_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);
print(h.fig,'-dpng',[messinfo,'\figures\Ladekurve_auswertung_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);

end
C_F=C_F.';
t0_s=t0_s.';

C_median_F = median(C_F(Median_Start:Median_Ende));
t0_median_s = median(t0_s(Median_Start:Median_Ende));
end
