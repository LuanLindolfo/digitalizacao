import scipy.io
import numpy as np  # Importação da NumPy
import os

# Configurações
nome_arquivo_ecg = 'elctrography_Dog_01.mat'
nome_arquivo_picos = 'peaks_Dog_01.mat'

# Verifica se o arquivo de ECG existe
if not os.path.exists(nome_arquivo_ecg):
    raise FileNotFoundError(f'Arquivo {nome_arquivo_ecg} não encontrado no diretório atual: {os.getcwd()}')

# *** CARREGAMENTO E IDENTIFICAÇÃO DA VARIÁVEL DE ECG ***
try:
    # Carrega o arquivo .mat
    S = scipy.io.loadmat(nome_arquivo_ecg)
    
    # Obtém os nomes das variáveis no arquivo
    nomes_vars = [var for var in S if not var.startswith('__')]  # Ignora variáveis internas do MATLAB
    
    # Tenta encontrar 'Data' primeiro
    if 'Data' in nomes_vars:
        nome_variavel_ecg = 'Data'
    else:
        # Se 'Data' não existe, encontra a primeira variável numérica vetorial
        nome_variavel_ecg = None
        for var in nomes_vars:
            if isinstance(S[var], np.ndarray) and S[var].ndim == 1:  # Verifica se é um vetor numérico
                nome_variavel_ecg = var
                break
        
        if nome_variavel_ecg is None:
            raise ValueError(f'Nenhuma variável numérica vetorial encontrada em {nome_arquivo_ecg}')
    
    print(f'Variável de ECG encontrada em {nome_arquivo_ecg}: {nome_variavel_ecg}')

except Exception as e:
    raise ValueError(f'Erro ao carregar o arquivo {nome_arquivo_ecg}: {e}')

# Verifica se o arquivo de picos existe
if not os.path.exists(nome_arquivo_picos):
    raise FileNotFoundError(f'Arquivo {nome_arquivo_picos} não encontrado no diretório atual: {os.getcwd()}')

# *** CARREGAMENTO E IDENTIFICAÇÃO DA VARIÁVEL DE PICOS ***
try:
    # Carrega o arquivo .mat
    S = scipy.io.loadmat(nome_arquivo_picos)
    
    # Obtém os nomes das variáveis no arquivo
    nomes_vars = [var for var in S if not var.startswith('__')]  # Ignora variáveis internas do MATLAB
    
    # Procura pela variável que não seja 'ans'
    nome_variavel_picos = None
    for var in nomes_vars:
        if var != 'ans':  # Ignora a variável 'ans'
            nome_variavel_picos = var
            break
    
    if nome_variavel_picos is None:
        raise ValueError(f'Nenhuma variável encontrada em {nome_arquivo_picos}')
    
    print(f'Variável de picos encontrada em {nome_arquivo_picos}: {nome_variavel_picos}')

except Exception as e:
    raise ValueError(f'Erro ao carregar o arquivo {nome_arquivo_picos}: {e}')

# Limpa variáveis temporárias (não necessário em Python, mas feito por consistência)
del S, nomes_vars