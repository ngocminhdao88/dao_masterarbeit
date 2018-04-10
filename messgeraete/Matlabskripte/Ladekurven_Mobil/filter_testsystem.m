% Fs = 1000;            % Sampling frequency
% T = 1/Fs;             % Sampling period
% L = 1000;             % Length of signal
% t = (0:L-1)*T;        % Time vector
% 
% S = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t);
% 
% X = S + 2*randn(size(t));
% h.fig = figure(1001);
% plot(1000*t(1:50),X(1:50))
% title('Signal Corrupted with Zero-Mean Random Noise')
% xlabel('t (milliseconds)')
% ylabel('X(t)')
% 
% Y = fft(X);
% P2 = abs(Y/L);
% P1 = P2(1:L/2+1);
% P1(2:end-1) = 2*P1(2:end-1);
% f = Fs*(0:(L/2))/L;
% h.fig = figure(1002);
% plot(f,P1)
% title('Single-Sided Amplitude Spectrum of X(t)')
% xlabel('f (Hz)')
% ylabel('|P1(f)|')
% 
% 
% Y = fft(S);
% P2 = abs(Y/L);
% P1 = P2(1:L/2+1);
% P1(2:end-1) = 2*P1(2:end-1);
% h.fig = figure(1003);
% plot(f,P1)
% title('Single-Sided Amplitude Spectrum of S(t)')
% xlabel('f (Hz)')
% ylabel('|P1(f)|')

clf
filtertest=medfilt1(test,75);
h.fig = figure(1005);
hold on
plot(test)
plot(filtertest)
legend('orignal signal','filtered signal');

% iN =10;
% Kurve_glatt = filter(ones(1,iN)/iN, 1, filtertest);
% h.fig = figure(1006);
% hold on
% plot(filtertest)
% plot(Kurve_glatt)
% legend('filtered signal','twice filtered signal');
