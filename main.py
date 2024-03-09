import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, freqz

def fir_filter_unrolled(input_signal, filter_coefficients):
    M = len(filter_coefficients)
    output_signal = np.zeros_like(input_signal)

    for n in range(0, len(input_signal), 4):  # Unrolling la idea es ampliarlo
        for k in range(M):
            output_signal[n] += filter_coefficients[k] * input_signal[n - k]
            output_signal[n+1] += filter_coefficients[k] * input_signal[n+1 - k]
            output_signal[n+2] += filter_coefficients[k] * input_signal[n+2 - k]
            output_signal[n+3] += filter_coefficients[k] * input_signal[n+3 - k]

    return output_signal


# Parámetros de la señal
frecuencia = 500  # Frecuencia de la onda sinusoidal en Hz
duracion = 5  # Duración de la señal en segundos
frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz


# Crear el vector de tiempos de muestreo
t = np.arange(0, duracion, 1/frecuencia_muestreo)
print("T creado")
# Generar la onda sinusoidal
y = np.sin(2 * np.pi * frecuencia * t)
print("y creado")

# Parámetros del ruido
media_ruido = 0  # Media del ruido
std_ruido = 0.3  # Desviación estándar del ruido (ajusta este valor para cambiar la intensidad del ruido)

# Generar ruido blanco
ruido = np.random.normal(media_ruido, std_ruido, y.shape)
print("ruido creado")

# Señal con ruido
y_ruidosa = y + ruido
print("y_ruidosa creado")

# Parámetros del filtro
orden_del_filtro = 16  # Número de taps coeficientes
frecuencia_de_corte = 2000  # Frecuencia de corte en Hz

#Práctica común en filtrado de señales de audio se divide la frecuencia de corte entre la mitad de la
#frecuencia de muestreo
frecuencia_de_corte_normalizada = frecuencia_de_corte / (0.5 * frecuencia_muestreo)

# Obtener los coeficientes del filtro FIR usando una ventana de Hamming
coeficientes = firwin(orden_del_filtro, frecuencia_de_corte_normalizada, window='hamming')
coeficientes= coeficientes[::-1]

print("Coef. creados")
print(coeficientes)


Señal_filtro=fir_filter_unrolled(y_ruidosa,coeficientes)
print("Señal Filt. creado")

plt.figure(figsize=(10, 6))
plt.plot(y[:1000], label='Señal Original')
plt.plot(y_ruidosa[:1000], label='Señal con Ruido', alpha=0.75)
plt.plot(Señal_filtro[:1000], label='Señal Filtrada', linestyle='--')
plt.legend()
plt.title('Comparación de Señales')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()