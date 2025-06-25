#!/usr/bin/env python3

# Stand alone script to validate demand data This script validates the
# demand data by checking the mean, confidence interval, and goodness of
# fit using the Kolmogorov-Smirnov test.   It also generates a histogram
# of the demand data.

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Demandas simuladas como ejemplo
np.random.seed(626)
demand_data = np.random.uniform(1, 100, 100)  # 100 valores de demanda

# Validaciones
# Intervalo de confianza
mean_demand = np.mean(demand_data)
std_demand = np.std(demand_data)
confidence_interval = stats.norm.interval(0.95, loc=mean_demand, scale=std_demand / np.sqrt(len(demand_data)))

print("Media de demanda:", mean_demand)
print("Intervalo de confianza 95%:", confidence_interval)

# Validaciones
# Bondad de ajuste (Kolmogorov-Smirnov)
ks_statistic, p_value = stats.kstest(demand_data, 'uniform', args=(1, 100))

print("Estadístico KS:", ks_statistic)
print("p-valor:", p_value)

if p_value < 0.05:
    print("Los datos NO siguen una distribución uniforme (nivel de significancia 0.05).")
else:
    print("Los datos siguen distribución uniforme.")

# Histograma
plt.hist(demand_data, bins=10, alpha=0.7, color='blue', edgecolor='black')
plt.title("Distribución de demandas")
plt.xlabel("Demanda")
plt.ylabel("Frecuencia")
plt.show()
