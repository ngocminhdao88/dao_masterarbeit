function [Kurve_glatt, zeitbasis]=kurve_glaetten(kurve, filterlaenge, samplerate) 
% Gl�ttet eine gemessene Ladekurve, so dass diese besser ausgewertet werden
% kann. Gibt zudem eine passende Zeitbasis f�r die Kurve aus basierend auf
% der Samplerate
% Kurve: Gemessene Kurve
% filterlaenge: L�nge des Filters
% samplerate: Samplerate der aufgenommenen Kurve

iN = filterlaenge; % L�nge des Filters
% Gl�tten der Kurve
% Kurve_glatt = filter(ones(1,iN)/iN, 1, kurve);
Kurve_glatt=medfilt1(kurve,iN);


% Erzeugen einer passenden Zeitbasis f�r die Kurve
% Zun�chst leere Matrix erzeugen
zeitbasis=zeros(size(Kurve_glatt));

% Zeitbasis f�llen entsprechend der Samplerate
for i=1:size(Kurve_glatt)
    zeitbasis(i)=i*1/samplerate;
end

end