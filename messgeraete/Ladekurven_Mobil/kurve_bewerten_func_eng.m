function [index,  C, R_p, stuetz_unten, stuetz_oben] = kurve_bewerten_func_eng (kurve, zeitbasis, messung, inkrement, U_lade, R_lade, messinfo)
% Funktion um eine Ladekurve zu bewerten
% Gibt zurück, ob die Kurve nutzbar ist, die ermittelten Kennwerte und welche Stützstellen nach
% Nutzereingabe genutzt wurden.

% feste Variablen
abfrage_string = ('Kurve auswerten? j(=1)/n(=2)? [n]     ');
bewerten_string = ('Ergebnis ok? ja(=1)/nochmal(=2)/Abbruch(=3)? [j]     ');

% Als erstes  bewerten, ob Kurve überhaupt nutzbar ist:
abfrage = 1;
while (abfrage)
    
    % zunächst Kurve darstellen:
    h.fig1 = figure(1001);
    clf
    hold on
    %h.fig1.Position = [226, 175, 1352, 849];
    plot(zeitbasis,kurve);
    title(['Parasitic System-Capacitance'])
    xlabel('Time in s \rightarrow')
    ylabel('Capacitor Voltage in V \rightarrow')
    savefig(h.fig1, [messinfo,'\Ladekurve_Inc_',num2str(inkrement),'_Messung',num2str(messung)]);
    saveas(h.fig1, [messinfo,'\Ladekurve_Inc_',num2str(inkrement),'_Messung',num2str(messung),'.png']);
    % Abfrage ob die Kurve ausgewertet werden soll
    antwort=input(abfrage_string,'s');
    % Standardantwort = direkt mit Enter bestätigen
    if isempty(antwort)
        antwort = 'n';
    end
    % Antwort auswerten
    if (strcmp(antwort,'j'))
        index = 1;
        bewerten=1;
        abfrage=0;
    elseif (strcmp(antwort,'n'))
        index =0;
        abfrage=0;
    else
        disp ('Fehleingabe, bitte Wiederholen!');
    end
end

% Schleife zum Bewerten
if (index==1)
    while (bewerten)
        
        disp('x-Position des unteren Stützpunkts angeben');
        [x_unten, y_unten] = ginput(1);
        i_unten=sverweis_zeile(x_unten,zeitbasis,1);
        disp(['gewählter unterer Stützpunkt: ']);
        disp(['Zeit: ',num2str(zeitbasis(i_unten))]);
        disp(['Spannung: ', num2str(kurve(i_unten))]);
       
        
        disp('x-Position des oberen Stützpunkts angeben');
        [x_oben, y_oben] = ginput(1);
        i_oben=sverweis_zeile(x_oben,zeitbasis,1);
        disp(['gewählter oberer Stützpunkt: ']);
        disp(['Zeit: ',num2str(zeitbasis(i_oben))]);
        disp(['Spannung: ', num2str(kurve(i_oben))]);
        [C, R_p] =ladekurve_auswerten(kurve,zeitbasis, i_unten, i_oben, R_lade, U_lade);
        
        
        plot([zeitbasis(i_unten), zeitbasis(i_oben)],[kurve(i_unten),kurve(i_oben)],'x');

        ladekurve_calc_eng( C, R_p, kurve, zeitbasis, R_lade, U_lade, i_unten, i_oben, inkrement, messung, messinfo);
        
       antwort2=input(bewerten_string,'s');
        if isempty(antwort2)
            antwort2 = 'j';
        end
        if (strcmp(antwort2,'j'))|(antwort2==1)
            bewerten=0;
            stuetz_unten=i_unten;
            stuetz_oben=i_oben;
           
        elseif (strcmp(antwort2,'nochmal'))|(antwort2==2)
            % Kurve neu erstellen
            h.fig1 = figure(1001);
            clf
            hold on
            %h.fig1.Position = [226, 175, 1352, 849];
            plot(zeitbasis,kurve);
    title(['Parasitic System-Capacitance'])
    xlabel('Time in s \rightarrow')
    ylabel('Capacitor Voltage in V \rightarrow')
            
        elseif (strcmp(antwort2,'Abbruch'))|(antwort2==3)
            index =0;
            bewerten=0;
            C=0;
            R_p=0;
            stuetz_unten=0;
            stuetz_oben=0;
        else
            disp ('Fehleingabe, bitte Wiederholen!');
        end
    end
else
         index =0;
            C=0;
            R_p=0;
            stuetz_unten=0;
            stuetz_oben=0;
end






%     i=x_oben;
%     while (kurve(i)<obergrenze)
%         i=i+1;
%     end
%     stuetz_oben = i;
%

end



