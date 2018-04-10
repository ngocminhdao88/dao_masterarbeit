% Ladekurven müssen bereits eingelesen sein!

if (exist ('Ladekurven'))
    
    % Daten der Messung abfragen, damit alles sauber in Unterordnern landet
   % messinfo=input('Messung bitte benennen: ','s');
   % mkdir(messinfo);
    
    % Feste Daten
   % U_Lade_V = 0.2;
   % R_Lade_ohm = 47390;
    
    
    % Anzahl der Inkremente und Messungen ermitteln aus den Daten
    Inkrementzahl = size(Ladekurven,2);
    Messungszahl = size(Ladekurven{1,1},2);
    
    
    % Schleifendurchlauf für jedes Inkrement und darin jede Messung
    for i=1:Inkrementzahl
        for j=1:10
        % for j=32:32    
            % Zunächst die Messdaten glätten und eine Zeitbasis erzeugen
            [glattekurve, zeitbasis] = kurve_glaetten(Ladekurven{1, i}(:,j), Filterlaenge, Samplerate);
            %[Kapa{1,i}(1,j), R{1,i}(1,j)]= auswerten(1, glattekurve, zeitbasis);
            % neue Matrix mit den glatten Ladekurven erzeugen
            Ladekurven_glatt{1,i}(:,j)=glattekurve;
            % neue Matrix mit den Zeitbasen erzeugen
            Zeitbasen{1,i}(:,j)=zeitbasis;
            % Bewertung der jeweiligen Kurve durchführen
%           [index(j,i), C(j,i), R_p(j,i), stuetz_unten(j,i), stuetz_oben(j,i)]=kurve_bewerten_func(glattekurve,zeitbasis, j, i, U_Lade_V, R_Lade_ohm, messinfo);
          %   [index(j,i), C(j,i), R_p(j,i), stuetz_unten(j,i), stuetz_oben(j,i)]=kurve_bewerten_func_eng(glattekurve,zeitbasis, j, i, U_Lade_V, R_Lade_ohm, messinfo);
           [C_vek{1,i}(:,j), C_med{1,i}(:,j),t0_vek{1,i}(:,j), t0_med{1,i}(:,j)]=kurve_auswerten_func(glattekurve,zeitbasis, U_Lade_V, R_Lade_ohm, messinfo, i, j);
        
        end
    end
    
   %Auswertung={C, index, R_p, stuetz_unten, stuetz_oben};
    Auswertung={C_vek, C_med, t0_vek, t0_med};
    speichername = strcat(messinfo, '\Auswertung.mat');
    save (speichername, 'Auswertung');
%     for i=1:Inkrementzahl
%         C_Copy(:,i)=C(:,i);
%         C_Copy(C_Copy==0)=NaN; 
%         %C_Mean(i)=nanmean( C_Copy(:,i));
%       %  C_Median(i)=nanmedian( C_Copy(:,i));
%     end
    
    
else
    disp('Keine Ladekurven im Speicher!');
end



