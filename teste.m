
% config_ecg.m
nome_arquivo_ecg = 'elctrography_Dog_01.mat';
nome_arquivo_picos = 'peaks_Dog_01.mat';

% *** CARREGAMENTO E IDENTIFICAÇÃO DA VARIÁVEL DE ECG ***
try
    S = load(nome_arquivo_ecg); % Carrega o arquivo para uma struct 'S'
    nomes_vars = fieldnames(S); % Obtém os nomes dos campos da struct

    % Tenta encontrar 'Data' primeiro
    if isfield(S, 'Data')
        nome_variavel_ecg = 'Data';
    else
        % Se 'Data' não existe, encontra a primeira variável numérica vetorial
        for i = 1:length(nomes_vars)
            if isnumeric(S.(nomes_vars{i})) && isvector(S.(nomes_vars{i}))
                nome_variavel_ecg = nomes_vars{i};
                break;
            end
        end
        if ~exist('nome_variavel_ecg', 'var')
            error('Nenhuma variável numérica vetorial encontrada em %s', nome_arquivo_ecg);
        end
    end

    fprintf('Variável de ECG encontrada em %s: %s\n', nome_arquivo_ecg, nome_variavel_ecg);

catch
    error('Erro ao carregar o arquivo %s.', nome_arquivo_ecg);
end

% *** CARREGAMENTO E IDENTIFICAÇÃO DA VARIÁVEL DE PICOS ***
try
    S = load(nome_arquivo_picos);
    nomes_vars = fieldnames(S);

    %Procura pela variavel que não seja 'ans'
    for i = 1:length(nomes_vars)
        if ~strcmp(nomes_vars{i}, 'ans')
            nome_variavel_picos = nomes_vars{i};
            break;
        end
    end

    if ~exist('nome_variavel_picos', 'var')
        error('Nenhuma variável encontrada em %s.', nome_arquivo_picos);
    end

    fprintf('Variável de picos encontrada em %s: %s\n', nome_arquivo_picos, nome_variavel_picos);

catch
    error('Erro ao carregar o arquivo %s.', nome_arquivo_picos);
end

clear S nomes_vars i; % Limpa variáveis temporárias
