import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import butter, filtfilt

# Carregar os dados do arquivo .mat
try:
    data_ecg = loadmat(nome_arquivo_ecg)
    ecg_signal = data_ecg[nome_variavel_ecg].flatten()  # Carrega o sinal de ECG
except Exception as e:
    raise ValueError(f'Erro ao carregar a variável {nome_variavel_ecg} do arquivo {nome_arquivo_ecg}: {e}')

try:
    data_peaks = loadmat(nome_arquivo_picos)
    peaks = data_peaks[nome_variavel_picos]  # Carrega os picos
except Exception as e:
    raise ValueError(f'Erro ao carregar a variável {nome_variavel_picos} do arquivo {nome_arquivo_picos}: {e}')

# Parâmetros do sinal
N = len(ecg_signal)  # Número de amostras
fs = 360  # Frequência de amostragem (Hz)
t = np.arange(N) / fs  # Vetor de tempo

# Plotar o sinal de ECG original
plt.figure()
plt.plot(t, ecg_signal, 'b', linewidth=1.5)
plt.title('Sinal de ECG Original')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# --- SELEÇÃO DE AMOSTRAS ---
numero_amostras = N  # Define o número de amostras desejado (ajuste este valor)

if numero_amostras > N:
    print(f'Aviso: Número de amostras solicitado ({numero_amostras}) é maior que o número total de amostras disponíveis ({N}). Usando todas as amostras.')
    numero_amostras = N

ecg_signal_selecionado = ecg_signal[:numero_amostras]  # Seleciona as amostras do sinal
t_selecionado = t[:numero_amostras]  # Seleciona os tempos correspondentes

# --- TRATAMENTO DOS PICOS ---
try:
    if isinstance(peaks, dict) and 'Channels' in peaks and 'Position' in peaks['Channels']:
        peaks_indices = peaks['Channels']['Position'].flatten()  # Extrai os índices dos picos
        peaks_indices = peaks_indices[peaks_indices <= numero_amostras]  # Ajusta os índices para o sinal selecionado
    elif isinstance(peaks, np.ndarray) and peaks.ndim == 1:
        peaks_indices = peaks
    elif isinstance(peaks, dict) and 'pos' in peaks:
        peaks_indices = peaks['pos'].flatten()
    elif isinstance(peaks, dict) and 'data' in peaks:
        peaks_indices = peaks['data'].flatten()
    elif isinstance(peaks, dict) and 'time' in peaks:
        peaks_indices_original = np.isin(peaks['time'], t_selecionado)
        peaks_indices = np.where(peaks_indices_original)[0]
    else:
        print('Estrutura de "peaks":')
        print(peaks)
        raise ValueError('Formato da variável "peaks" não reconhecido. Inspecione a estrutura acima e ajuste o código.')

    # Validação dos índices
    if np.any(peaks_indices < 0) or np.any(peaks_indices >= len(t_selecionado)) or np.any(np.isnan(peaks_indices)):
        raise ValueError('Índices de picos inválidos. Verifique o arquivo .mat e a lógica de detecção de picos.')
except Exception as e:
    print(f'Aviso: {e}')
    peaks_indices = np.array([])  # Define peaks_indices como vazio para evitar erros posteriores

# --- FILTRAGEM DO SINAL ---
# Projeto do filtro passa-baixa
fc = 40  # Frequência de corte do filtro (Hz)
ordem = 4  # Ordem do filtro
b, a = butter(ordem, fc / (fs / 2), btype='low')  # Projeta o filtro Butterworth de 4ª ordem

# Aplicando o filtro ao sinal de ECG
ecg_filtrado = filtfilt(b, a, ecg_signal_selecionado)

# --- DIGITALIZAÇÃO DO SINAL SELECIONADO ---
ad = 3  # Número de bits para a quantização
nd = 2 ** ad  # Número de níveis de quantização
max_ecg = np.max(ecg_signal_selecionado)  # Valor máximo do sinal selecionado
min_ecg = np.min(ecg_signal_selecionado)  # Valor mínimo do sinal selecionado
alf = np.linspace(min_ecg, max_ecg, nd)  # Vetor de níveis de quantização
ecg_digitalizado = np.zeros_like(ecg_signal_selecionado)  # Inicializa o sinal digitalizado

for i in range(len(ecg_signal_selecionado)):
    erro = np.abs(ecg_signal_selecionado[i] - alf)  # Calcula o erro entre a amostra e os níveis de quantização
    ind = np.argmin(erro)  # Encontra o índice do nível de quantização mais próximo
    ecg_digitalizado[i] = alf[ind]  # Atribui o nível de quantização à amostra digitalizada

# --- PLOTAGENS ---
# Figura 1: Sinal original e filtrado
plt.figure()
plt.plot(t_selecionado, ecg_signal_selecionado, 'b', linewidth=1.5, label='Original')
plt.plot(t_selecionado, ecg_filtrado, 'r', linewidth=2, label='Filtrado')  # Sinal filtrado em vermelho
if len(peaks_indices) > 0:
    plt.plot(t_selecionado[peaks_indices], ecg_signal_selecionado[peaks_indices], 'ro', markersize=8, label='Picos')
plt.title(f'Sinal de ECG Selecionado (Primeiras {numero_amostras} amostras) com picos')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()

# Figura 2: Sinal digitalizado
plt.figure()
plt.step(t_selecionado, ecg_digitalizado, 'r', linewidth=1.5, where='post')
plt.title(f'Sinal de ECG Digitalizado ({ad} bits) - Sinal Selecionado')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
