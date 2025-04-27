% geração e digitalização de sinal
% Limpa o workspace e a tela
clear; clc; close all;

% Nome do arquivo .mat contendo o sinal de ECG
dog_ecg = 'elctrography_Dog_01.mat';

% Carrega o arquivo .mat. Assumindo que a variável dentro do .mat
% que contém os dados do ECG se chama 'ecg_signal'.
% Adapte 'ecg_signal' para o nome da variável no SEU arquivo.
try
  load(dog_ecg, 'dog_ecg');
catch
  error('Erro ao carregar o arquivo .mat ou variável "dog_ecg" não encontrada.');
end

% Verifica se 'ecg_signal' existe e se é um vetor
%if ~exist('ecg_signal', 'var') || ~isvector(ecg_signal)
   % error('Variável "ecg_signal" não encontrada ou não é um vetor.');
%end

% Obtém o tamanho do sinal
N = length(dog_ecg);

% Cria um vetor de tempo (assumindo uma taxa de amostragem de 360 Hz, comum em ECGs)
% Ajuste esse valor se a sua taxa de amostragem for diferente.
fs = 360; % Frequência de amostragem (Hz)
t = (0:N-1) / fs;

% Plota o sinal de ECG original (não digitalizado)
figure;
plot(t, dog_ecg);
title('Sinal de ECG Original (Não Digitalizado)');
xlabel('Tempo (s)');
ylabel('Amplitude');
grid on;


