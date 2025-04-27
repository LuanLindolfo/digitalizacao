clear; clc; close all;

% Executando o arquivo de configuração
run('teste.m');

% Carrega os dados
try
    load(nome_arquivo_ecg, nome_variavel_ecg);
    ecg_signal = load(nome_arquivo_ecg).(nome_variavel_ecg);
catch
    error('Erro ao carregar a variável %s do arquivo %s', nome_variavel_ecg, nome_arquivo_ecg);
end

try
    load(nome_arquivo_picos, nome_variavel_picos);
    peaks = load(nome_arquivo_picos).(nome_variavel_picos);
catch
    error('Erro ao carregar a variável %s do arquivo %s', nome_variavel_picos, nome_arquivo_picos);
end


N = length(ecg_signal);
fs = 360; %Frequência do sinal
t = (0:N-1) / fs;

% Plota o sinal de ECG original
figure;
plot(t, ecg_signal);
title('Sinal de ECG Original');
xlabel('Tempo (s)');
ylabel('Amplitude');
hold on;

% --- SELEÇÃO DE AMOSTRAS ---
numero_amostras =150;% Define o número de amostras desejado

if numero_amostras > N
    warning('Número de amostras solicitado (%d) é maior que o número total de amostras disponíveis (%d). Usando todas as amostras.', numero_amostras, N);
    numero_amostras = N;
end

ecg_signal_selecionado = ecg_signal(1:numero_amostras); % Seleciona as amostras do sinal
t_selecionado = t(1:numero_amostras);                 % Seleciona os tempos correspondentes

% --- TRATAMENTO DOS PICOS ---
try
    if isstruct(peaks) && isfield(peaks, 'Channels') && isfield(peaks.Channels, 'Position')
        peaks_indices = peaks.Channels.Position; % Extrai os índices dos picos (caso específico)
        peaks_indices = peaks_indices(peaks_indices <= numero_amostras); % Ajusta os índices para o sinal selecionado
    %Outros casos que possam existir no seu código
    elseif iscell(peaks) && length(peaks) == 1 && isvector(peaks{1})
        peaks_indices = peaks{1};
    elseif isvector(peaks)
        peaks_indices = peaks;
    elseif isstruct(peaks) && isfield(peaks, 'pos')
        peaks_indices = peaks.pos;
    elseif isstruct(peaks) && isfield(peaks, 'data')
        peaks_indices = peaks.data;
    elseif isstruct(peaks) && isfield(peaks, 'time')
        [~, peaks_indices_original] = ismember(peaks.time, t);
        peaks_indices_original(peaks_indices_original == 0) = [];
        peaks_indices = peaks_indices_original(peaks_indices_original <= numero_amostras);
    else
        disp('Estrutura de "peaks":');
        disp(peaks);
        error('Formato da variável "peaks" não reconhecido. Inspecione a estrutura acima e ajuste o código.');
    end
    % Validação dos índices (IMPORTANTE)
    if any(peaks_indices < 1) || any(peaks_indices > length(t_selecionado)) || any(isnan(peaks_indices)) || ~isnumeric(peaks_indices) || any(mod(peaks_indices,1)~=0)
        error('Índices de picos inválidos. Verifique o arquivo .mat e a lógica de detecção de picos.');
    end
catch ME
    warning(ME.message);
    peaks_indices = []; % Define peaks_indices como vazio para evitar erros posteriores
end

% --- DIGITALIZAÇÃO DO SINAL SELECIONADO ---
ad = 16;                       % Número de bits para a quantização
nd = 2^ad;                    % Número de níveis de quantização
max_ecg = max(ecg_signal_selecionado); % Valor máximo do sinal selecionado
min_ecg = min(ecg_signal_selecionado); % Valor mínimo do sinal selecionado
alf = linspace(min_ecg, max_ecg, nd); % Vetor de níveis de quantização
ecg_digitalizado = zeros(size(ecg_signal_selecionado)); % Inicializa o sinal digitalizado

for i = 1:length(ecg_signal_selecionado)
    erro = abs(ecg_signal_selecionado(i) - alf); % Calcula o erro entre a amostra e os níveis de quantização
    [~, ind] = min(erro);                % Encontra o índice do nível de quantização mais próximo
    ecg_digitalizado(i) = alf(ind);      % Atribui o nível de quantização à amostra digitalizada
end

% --- PLOTAGENS ---
figure;
plot(t_selecionado, ecg_signal_selecionado, 'b', 'LineWidth', 1.5); hold on;
if ~isempty(peaks_indices)
    plot(t_selecionado(peaks_indices), ecg_signal_selecionado(peaks_indices), 'ro', 'MarkerSize', 8);
    legend('Original', 'Picos');
end
hold off;
title(['Sinal de ECG Selecionado (Primeiras ' num2str(numero_amostras) ' amostras) com picos']);
xlabel('Tempo (s)');
ylabel('Amplitude');
grid on;

figure;
stairs(t_selecionado, ecg_digitalizado, 'r', 'LineWidth', 1.5);
title(['Sinal de ECG Digitalizado (' num2str(ad) ' bits) - Sinal Selecionado']);
xlabel('Tempo (s)');
ylabel('Amplitude');
grid on;
