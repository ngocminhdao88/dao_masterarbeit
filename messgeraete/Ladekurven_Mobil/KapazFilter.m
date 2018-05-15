function [filteredData] = KapazFilter(Ladekurven, Einstellungen)
% Filterung der Ladkurven mit einem Tiefpass Butterworth. Grenzfrequenz und
% Abtastrate sind stand 21.06.2016 fest im Skript eingestellt!!

fid = fopen('Filterung.log', 'w');
dispfileprint(fid,'Starting Filtering %s\n', datestr(datetime('now')));

Fs = Einstellungen{1,6}; %250000;          % Sampling frequency
T = 1/Fs;             % Sampling period
L = Fs/Einstellungen{1,7}; % 2500;             % Length of signal
t = (0:L-1)*T;        % Time vector
f_tp = 8e3;           % FilterWellenlänge

dispfileprint(fid, ['Filter parameters:\n Sampling Frquency Fs = ', ...
    num2str(Fs), ' Hz\n Sampling Period T = ', ...
    num2str(T), ' s;\n Signal length L = ', ...
    num2str(L), ';\n Filter wave length f_TP = ', num2str(f_tp), ' Hz\n'])

X = Ladekurven; 

figure(1001)
clf
hold on
plot(1000*t,X)
title('Signal')
xlabel('t in ms')
ylabel('X(t)')


Y = fft(X);

P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(1002)
clf
plot(f,P1)
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')



%Tiefpassfilterung
[b, a] = butter(1,f_tp/(0.5*Fs),'low'); % Koeffizienten der Übertragungsfunktion, f_tp ist die Grenzfrequenz, fs die Abtastfrequ., Butterworthfilter
x = filter(b,a,X); %x ist das Signal

figure(1001)
plot(1000*t-0.02,x,'k')
ax = gca;
ax.XLim = [1.8, 2.5];
ax.YLim = [-0.025, 0.2];


figure(1003)
plot(1000*t-0.02,x,'k.')
ax = gca;
ax.XLim = [1.8, 2.5];
ax.YLim = [-0.025, 0.2];


filteredData = x;
fclose(fid);
end
function dispfileprint(fid, string, varargin)
fprintf(fid, string,varargin{1:nargin-2});
fprintf(string,varargin{1:nargin-2});
end



