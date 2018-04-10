function [Ladekurven, name, Einstellungen] = ladekurven_einlesen()

% Öffnen der Lagerdatei. Selbsständiges Auslesen der Lagerart mit
% anschließender Berechnung.
[filename,pathname]=uigetfile({'*.txt',  'Messung (*.txt)'});
filename
% Abbruchkriterium festlegen.
Programmstopp=0;
ok=0;

% Datei in den Arbeitsordner verschieben
movefile(strcat(pathname, filename));

% Datei so umbenennen, dass keine Leerzeichen und Punkte im String sind
[path, name, ext]=fileparts(filename);

newname = strrep(name, '.', '_');
newname = strrep(newname, ' ', '_');

newfilename = strcat(newname, ext);
if strcmp(filename,newfilename)
else
movefile(filename, newfilename);
end

filename= newfilename;

% Dateiauswahl aus beliebigem Ordner ermöglichen.
if pathname==0
    fid=0;
    Programmstopp=1;
    disp('Auswahl abgebrochen! Bitte gültige Datei auswählen!');
else
   addpath(pathname);
   fid=fopen(filename); 
 end


% Überprüfung ob Datei erfolgreich geöffnet.
while fid < 0 
    
   errmsg= 'Fehler beim öffnen der Datei!';
   disp(errmsg);
   Programmstopp=1;
   break
end

datenpunkt = 1;

% Definition der Suchstrings
Kurve_string = 'Kurve ';
Zeit_string = 'Zeit: ';
Info_string = 'Info: ';
Ladewiderstand_string = 'Ladewiderstand[Ohm]: ';
Stoerkapa_string = 'Störkapazität[nF]: ';
Entladezeit_string = 'Entladezeit[ms]: ';
Abtastrate_string = 'Abtastrate[Hz]: ';
Messzeit_string = 'Messzeit [ms]: ';
Verzoegerung_string = 'Verzögerung[ms]: ';
Ladespannung_string = 'Ladespannung[V]: ';
% initalisieren der eingelesenen Header-Werte

Datum ='';
Info='';
Ladewiderstand_Ohm=0;
Stoerkapazitaet_pF = 0;
Ladespannung_V = 0;
Abtastrate_Hz=0;
Entladezeit_ms=0;
Messzeit_ms =0;
Verzoegerung_ms=0;

tline=fgetl(fid);

% Headerzeilen einlesen
while  ~(strncmpi(tline,Kurve_string,size(Kurve_string,2)))
    if (strncmpi(tline,Zeit_string,size(Zeit_string,2)))
        % Messzeit einlesen
        %tline=fgetl(fid);
        Datum=tline(size(Zeit_string,2)+1:size(tline,2));
       
        
    elseif (strncmpi(tline,Info_string,size(Info_string,2)))
        Info=tline(size(Info_string,2)+1:size(tline,2));
              
    elseif (strncmpi(tline,Ladewiderstand_string,size(Ladewiderstand_string,2)))
        Ladewiderstand_Ohm=str2double(tline(size(Ladewiderstand_string,2)+1:size(tline,2)));
        
    elseif (strncmpi(tline,Stoerkapa_string,size(Stoerkapa_string,2)))
        Stoerkapazitaet_pF=str2double(tline(size(Stoerkapa_string,2)+1:size(tline,2)));
        
    elseif (strncmpi(tline,Entladezeit_string,size(Entladezeit_string,2)))
        Entladezeit_ms=str2double(tline(size(Entladezeit_string,2)+1:size(tline,2)));
        
    elseif (strncmpi(tline,Abtastrate_string,size(Abtastrate_string,2)))
        Abtastrate_Hz=str2double(tline(size(Abtastrate_string,2)+1:size(tline,2)));
        
    elseif (strncmpi(tline,Messzeit_string,size(Messzeit_string,2)))
        Messzeit_ms=str2double(tline(size(Messzeit_string,2)+1:size(tline,2)));
        
    elseif (strncmpi(tline,Verzoegerung_string,size(Verzoegerung_string,2)))
        Verzoegerung_ms=str2double(tline(size(Verzoegerung_string,2)+1:size(tline,2)));
   
    elseif (strncmpi(tline,Ladespannung_string,size(Ladespannung_string,2)))
        Ladespannung_V=str2double(tline(size(Ladespannung_string,2)+1:size(tline,2)));
        
    end
    tline=fgetl(fid);
    
end

% Schleife zum zeilenweise Einlesen der Datei.
while ischar(tline)
    if (strncmpi(tline,'',1))
        % eine Zeile überspringen
        %tline=fgetl(fid);
        
        % Suchen nach dem Text Kurve
    elseif (strncmpi(tline,'Kurve ',6))
        % als erstes Nummer der Messung erkennen
        zeilenlaenge = size(tline,2);
        aktuelle_pos = 6;
        i = 1;
        while(zeilenlaenge-aktuelle_pos>=0)
            messung_nummer_temp(i) = tline(aktuelle_pos);
            aktuelle_pos = aktuelle_pos + 1;
            i = i+1;
        end
        messung_nummer = str2num(messung_nummer_temp);
        inkrement_nummer=1;
        datenpunkt = 1;
%         % Suchen nach dem Text Inkrement

%     elseif (strncmpi(tline,'Inkrement: ',11))
%         % jetzt die Nummer des Inkrements erkennen
%         zeilenlaenge = size(tline,2);
%         aktuelle_pos = 12;
%         inkrement_nummer_temp='';
%         i = 1;
%         while(zeilenlaenge-aktuelle_pos>=0)
%             inkrement_nummer_temp(i) = tline(aktuelle_pos);
%             aktuelle_pos = aktuelle_pos + 1;
%             i = i+1;
%         end
%         inkrement_nummer = str2num(inkrement_nummer_temp);
%         % Datenpunkte zurücksetzen
%         datenpunkt = 1;
    elseif ~isnan(str2double(tline))
        temp=str2double(tline);
        ladekurven_allgemein{1,inkrement_nummer}(datenpunkt, messung_nummer)=temp;
        datenpunkt = datenpunkt + 1;
    else
        
    end
    tline=fgetl(fid);
    
    
end
fclose(fid);                   % Datei schließen

Ladekurven=ladekurven_allgemein;
[path, name, ext]=fileparts(filename);
mkdir(name);
speichername = strcat(name, '\Ladekurven.mat');
save (speichername, 'Ladekurven');
movefile(filename, name);

if Abtastrate_Hz==0
    disp('Error, Samplerate ist null!');
end

Einstellungen = {Datum, Info, Ladewiderstand_Ohm, Stoerkapazitaet_pF, Ladespannung_V, Abtastrate_Hz, Entladezeit_ms, Messzeit_ms, Verzoegerung_ms};

end