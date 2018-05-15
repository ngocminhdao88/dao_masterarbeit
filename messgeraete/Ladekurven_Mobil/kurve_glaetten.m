function [Kurve_glatt, zeitbasis]=kurve_glaetten(kurve, filterlaenge, samplerate) 
% Glättet eine gemessene Ladekurve, so dass diese besser ausgewertet werden
% kann. Gibt zudem eine passende Zeitbasis für die Kurve aus basierend auf
% der Samplerate
% Kurve: Gemessene Kurve
% filterlaenge: Länge des Filters
% samplerate: Samplerate der aufgenommenen Kurve

iN = filterlaenge; % Länge des Filters
% Glätten der Kurve
% Kurve_glatt = filter(ones(1,iN)/iN, 1, kurve);
Kurve_glatt=medfilt1(kurve,iN);


% Erzeugen einer passenden Zeitbasis für die Kurve
% Zunächst leere Matrix erzeugen
zeitbasis=zeros(size(Kurve_glatt));

% Zeitbasis füllen entsprechend der Samplerate
for i=1:size(Kurve_glatt)
    zeitbasis(i)=i*1/samplerate;
end

end