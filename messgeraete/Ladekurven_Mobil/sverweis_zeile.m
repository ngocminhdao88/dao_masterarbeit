function [ index ] = sverweis_zeile( suchkriterium, matrix, spalte )
%sverweis sucht die Zeile, in der das Suchkriterium gerade gr��er ist und
%gibt aus der entsprechenden Zeile den Wert zur�ck
%   Detailed explanation goes here

% Erste Spalte als Vektor
f= matrix(:,1);
index = 1;
gefunden = 0;
% for i=1:size(f)
 for i=1:size(matrix)
    if (f(i)>=suchkriterium)&&(gefunden==0)
        index = i;
        gefunden = 1;
    else
        %sonst nix machen
    end   
end
% Suchen des am n�chsten liegenden Wertes, passt nicht zu SVERWEIS aus
% EXCEL!!! Daher hier nicht nutzen!
%[c, index] = min(abs(f-suchkriterium));

% Ausgabe des Ausgabewertes in der gefundenen Zeile nach gew�nschter Spalte
gesucht = matrix(index, spalte);
end
