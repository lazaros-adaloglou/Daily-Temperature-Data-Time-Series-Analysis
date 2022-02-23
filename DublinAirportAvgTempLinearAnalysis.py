# Imports.
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import LinearAnalysisFunctions as lf
import matplotlib.pyplot as plt
import pmdarima as pm
import datetime as dt
import pandas as pd
import numpy as np
import statistics
import warnings
import csv
import os

# Suppress Warnings.
warnings.filterwarnings("ignore")

# Load Data.
filename = 'data/DublinAirport_Data.csv'
try:
    data = pd.read_csv(filename, delimiter=',', parse_dates=['date'])
except FileNotFoundError:
    os.system('python DublinAirportDataPreprocessing.py')
    data = pd.read_csv(filename, delimiter=',', parse_dates=['date'])
print("===============================================================================================================")
print("Average Temperature Time Series:\n")
savepath = 'data/'
data = data.drop("Unnamed: 0", axis=1)
print(data)
dates = data.date
date_axis = [d.to_pydatetime() for d in dates]

# Define Average Temperature Time Series.
x = data.AvgTemp.values
# x_df = pd.DataFrame({data.AvgTemp.name: x})
#
# # Plot Average Temperature.
# lf.plot_timeseries(x, 'AvgTemp (°C)', 'Average Temperature', 'data/', date_axis)
# plt.show()
#
# # Average Temperature Histogram.
# lf.plot_histogram(x, 'AvgTemp (°C)', 'Average Temperature Histogram', 'data/')
# plt.show()
#
# # Plot Zoomed Average Temperature.
# lf.plot_timeseries(x, 'AvgTemp (°C)', 'Average Temperature (1998-2014)', 'data/', date_axis, zoomx=True)
# plt.show()
#
# # Plot Yearly Mean Average Temperature.
# x_year = []
# years = 80
# days = 365
# for year in range(0, years):
#     k = 0
#     for day in range(1, days + 1):
#         k = k + x[year * days + day]
#     x_year.append(k/days)
# dates_year = range(1942, 2022)
# plt.plot(dates_year, x_year, color='red', marker='x', linestyle='--', linewidth=1)
# plt.xlabel('Time (Years)')
# plt.ylabel('AvgTemp (°C)')
# title = 'Yearly Mean Average Temperature'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Average Temperature Autocorrelation.
# plot_acf(x, zero=False)
# title = 'Autocorrelation'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Remove Trend.
# # Polynomial Fit.
# p = 40
# pol = lf.polynomial_fit(x, p=p)
#
# # Linear Breakpoint Fit.
# p1 = 1
# pol1 = []
# breakpoints = 160
# for i in range(0, 80 * 12 * 30, 180):
#     pol1[i:i + 180] = lf.polynomial_fit(x[i:i + 180], p=p1)
#
# # Plot Polynomial and Breakpoint Fit.
# plt.plot(pol)
# plt.plot(pol1)
# plt.plot(x, alpha=0.5)
# plt.xlim(15000, 18000)
# plt.legend([f'Polynomial ({p})', f'Breakpoint ({breakpoints})', 'Original'])
# title = f'Polynomial ({p}) and Breakpoint Fit ({breakpoints})'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Plot Polynomial and Linear Breakpoint Detrends.
# plt.plot(x-pol, alpha=0.5)
# plt.plot(x[0:28800]-pol1, alpha=0.5)
# plt.legend([f'Polynomial ({p}) Detrended', f'Breakpoint ({breakpoints}) Detrended'])
# title = f'Polynomial ({p}) vs Breakpoint ({breakpoints}) Detrended'
# plt.title(title, x=0.5, y=1.0)
# plt.xlim(15000, 18000)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Moving Average Filter.
window = 92
ma = lf.rolling_window(x=x, window=window)
# plt.plot(ma, linestyle='--')
# plt.plot(x, alpha=0.5)
# plt.legend([f'MA ({window})', 'Original'])
# title = f'Moving Average ({window})'
# plt.title(title, x=0.5, y=1.0)
# plt.xlim(15000, 18000)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Differences of Logarithms (Increment each zero with 0.1).
# logx = []
# lx = x
# for i in range(0, len(lx)):
#     if lx[i] == 0:
#         lx[i] = lx[i] + 0.1
#     if lx[i] < 0:
#         logx.append(-np.log(abs(lx[i])))
#     else:
#         logx.append(np.log(lx[i]))
# fd = np.diff(logx)
#
# # MA vs Differences of Logarithms.
# ma = lf.rolling_window(x, window)
# plt.plot(x-ma, alpha=0.5)
# plt.plot(fd, alpha=0.5)
# plt.xlim(15000, 16000)
# title = f'Differences of Logarithms vs MA ({window})'
# plt.title(title, x=0.5, y=1.0)
# plt.legend([f'MA ({window}) Detrended', 'Differences of Logarithms Detrended'])
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# # Print Yearly Mean Average Temperature of detrended and not time series.
mas = x - ma
# mas_year = []
# years = 80
# days = 365
# for year in range(0, years):
#     k = 0
#     for day in range(1, days + 1):
#         k = k + mas[year * days + day]
#     mas_year.append(k/days)
# print("===============================================================================================================")
# print("Yearly Mean of Average Temperature Time Series:\n")
# for i in range(0, len(x_year), 9):
#     print(x_year[i])
# print("\nYearly Mean of Detrended Average Temperature Time Series:\n")
# for i in range(0, len(mas_year), 9):
#     print(mas_year[i])
#
# # Stabilize Variance.
# # Plot Yearly Variance of Average Temperature.
# split = np.array_split(x, 80)
# varis = []
# for i in range(0, len(split)):
#     varis.append(statistics.variance(split[i]))
# plt.plot(dates_year, varis, color='red', marker='x', linestyle='--', linewidth=1)
# plt.xlabel('Time (Years)')
# plt.ylabel('AvgTemp (°C)')
# title = 'Yearly Variance of Average Temperature'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()

# # Print Yearly Variance of Original, Detrended and Log of Detrended Average Temperature.
# split1 = np.array_split(mas, 80)
# varis1 = []
# for i in range(0, len(split1)):
#     varis1.append(statistics.variance(split1[i]))
# print("===============================================================================================================")
# print("Yearly Variance of Average Temperature Time Series:\n")
# for i in range(7, len(varis), 9):
#     print(varis[i])
# print("\nYearly Variance of Detrended Average Temperature Time Series:\n")
# for i in range(7, len(varis1), 9):
#     print(varis1[i])
fd = np.log(mas + abs(min(mas)) + 1)
fd = fd - fd.mean()
# plt.plot(fd, linestyle='--')
# plt.legend(['Log(X_Detrended+abs(min(X_Detrended)) + 1)-mean'])
# title = 'Logarithms of Detrended Average Temperature Time Series'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
# plt.plot(fd)
# plt.legend(['Log(X_Detrended+abs(min(X_Detrended)) + 1)-mean'])
# title = 'Logarithms of Detrended Time Series (Increased Resolution)'
# plt.title(title, x=0.5, y=1.0)
# plt.xlim(15000, 22000)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
# split2 = np.array_split(fd, 80)
# varis2 = []
# for i in range(0, len(split2)):
#     varis2.append(statistics.variance(split2[i]))
# print("\nYearly Variance of Logarithms of Detrended Average Temperature Time Series:\n")
# for i in range(7, len(varis2), 9):
#     print(varis2[i])
#
# # Print Yearly Mean Average Temperature of Logs of detrended time series.
# fd_year = []
# years = 80
# days = 365
# for year in range(0, years):
#     k = 0
#     for day in range(1, days + 1):
#         k = k + fd[year * days + day]
#     fd_year.append(k/days)
# print("===============================================================================================================")
# print("Yearly Mean of Logarithms of Detrended Average Temperature Time Series:\n")
# for i in range(0, len(fd_year), 9):
#     print(fd_year[i])

# # Remove Seasonality (There is no Seasonality).
#
# # Hypothesis test for white noise after Detrending with MA (92) and taking the logs.
# # Autocorrelation.
maxtau = 31
# acvf = lf.get_acf(fd, lags=maxtau)
# title = 'Autocorrelation for log(X_detrended)'
# plt.title(title, x=0.5, y=1.0)
# plt.savefig(f'{savepath}/{title}.png')
# plt.show()
#
# Model Adaption and Forecasting Single Step and Multistep.
# AR Model.
# Partial Autocorrelation Criterion for choosing model order.
fd = fd[15000:18000]
# pacvf = lf.get_pacf(fd, lags=maxtau)
# plt.show()

# Akaike Information Criterion (AIC) for choosing model order.
print("===============================================================================================================")
print("Exploring an AR Model for the Time Series:")
# best_aic_ar = np.inf
# best_p_ar = None
# for p in np.arange(1, 10, dtype=np.int):
#     try:
#         _, _, _, _, aic = lf.fit_arima_model(x=fd, p=p, q=0, d=0, show=False)
#     except ValueError as err:
#         print("--------------------------------------------------------------------------------------------------------"
#               "-------")
#         print(f'AR({p}) Error ---> {err}')
#         continue
#     print("------------------------------------------------------------------------------------------------------------"
#           "---")
#     print(f'AR({p}) AIC ---> {aic}')
#     if aic < best_aic_ar:
#         best_p_ar = p
#         best_aic_ar = aic
best_p_ar = 3
# best_aic_ar = -2649.3628420606137
# summary_ar, fittedvalues_ar, resid_ar, model_ar, aic_ar = lf.fit_arima_model(x=fd, p=best_p_ar, q=0, d=0, show=True)
# print("===============================================================================================================")
# print("Summary of chosen AR Model:\n")
# print(summary_ar)
# nrmseV_ar, predM_ar = lf.calculate_fitting_error(fd, model_ar, tmax=10, show=True)

# Out of sample predictions for time horizon Tmax.
prop = 0.7
split_point = int(prop*fd.shape[0])
train_fd, test_fd = fd[:split_point], fd[split_point:]
model_ar_train = pm.ARIMA(order=(best_p_ar, 0, 0))
model_ar_train.fit(train_fd)
return_conf_int = True
alpha = 0.05
Tmax = 70
preds_ar_train, conf_bounds_ar_train = \
    lf.predict_oos_multistep(model_ar_train, tmax=Tmax, return_conf_int=return_conf_int, alpha=alpha, show=False)
plt.figure()
plt.plot(np.arange(1, Tmax+1), preds_ar_train, label='predictions')
plt.plot(np.arange(1, Tmax+1), test_fd[:Tmax], label='original')
if return_conf_int:
    plt.fill_between(np.arange(1, Tmax+1), conf_bounds_ar_train[:, 0],
                     conf_bounds_ar_train[:, 1], color='green', alpha=0.3)
plt.legend()
plt.title(f'AR({best_p_ar}) oos predictions with horizon T={Tmax}')
plt.show()

# Rolling oos prediction.
preds = []
bounds = []
for i in test_fd:
    preds_ar_train_roll, conf_bounds_ar_train_roll = \
        model_ar_train.predict(n_periods=1, return_conf_int=return_conf_int, alpha=alpha)
    model_ar_train.update(i)
    preds.append(preds_ar_train_roll[0])
    bounds.append(conf_bounds_ar_train_roll[0])
plt.figure()
plt.plot(preds, label='predictions', linestyle='--', alpha=0.3)
plt.plot(test_fd, label='original', alpha=0.7)
if return_conf_int:
    bounds = np.array(bounds)
    plt.fill_between(np.arange(len(test_fd)), bounds[:, 0], bounds[:, 1], alpha=0.3, color='green')
plt.legend()
plt.title(f'AR({best_p_ar}) {Tmax} rolling oos predictions')
plt.show()

# # Portmanteau Test to see if the residuals are white noise.
# lf.portmanteau_test(resid_ar, maxtau, show=True)

# MA Model.
# Autocorrelation Criterion for choosing model order.
# Akaike Information Criterion (AIC) for choosing model order.
print("===============================================================================================================")
print("Exploring an MA Model for the Time Series:")
best_aic_ma = np.inf
best_q_ma = None
for q in np.arange(1, 10, dtype=np.int):
    try:
        _, _, _, _, aic = lf.fit_arima_model(x=fd, p=0, q=q, d=0, show=False)
    except ValueError as err:
        print("--------------------------------------------------------------------------------------------------------"
              "-------")
        print(f'MA({q}) Error ---> {err}')
        continue
    print("------------------------------------------------------------------------------------------------------------"
          "---")
    print(f'MA({q}) AIC ---> {aic}')
    if aic < best_aic_ma:
        best_q_ma = q
        best_aic_ma = aic
best_q_ma = 5
best_aic_ma = np.inf
summary_ma, fittedvalues_ma, resid_ma, model_ma, aic_ma = lf.fit_arima_model(x=fd, p=0, q=best_q_ma, d=0, show=True)
print("===============================================================================================================")
print("Summary of chosen MA Model:\n")
print(summary_ma)
nrmseV_ma, predM_ma = lf.calculate_fitting_error(fd, model_ma, tmax=10, show=True)

# Out of sample predictions for time horizon Tmax.
model_ma_train = pm.ARIMA(order=(0, best_q_ma, 0))
model_ma_train.fit(train_fd)
preds_ma_train, conf_bounds_ma_train = \
    lf.predict_oos_multistep(model_ma_train, tmax=Tmax, return_conf_int=return_conf_int, alpha=alpha, show=False)
plt.figure()
plt.plot(np.arange(1, Tmax+1), preds_ma_train, label='predictions')
plt.plot(np.arange(1, Tmax+1), test_fd[:Tmax], label='original')
if return_conf_int:
    plt.fill_between(np.arange(1, Tmax+1), conf_bounds_ma_train[:, 0],
                     conf_bounds_ma_train[:, 1], color='green', alpha=0.3)
plt.legend()
plt.title(f'MA({best_q_ma}) oos predictions with horizon T={Tmax}')
plt.show()

# Rolling oos prediction.
preds = []
bounds = []
for i in test_fd:
    preds_ma_train_roll, conf_bounds_ma_train_roll = \
        model_ma_train.predict(n_periods=1, return_conf_int=return_conf_int, alpha=alpha)
    model_ma_train.update(i)
    preds.append(preds_ma_train_roll[0])
    bounds.append(conf_bounds_ma_train_roll[0])
plt.figure()
plt.plot(preds, label='predictions', linestyle='--', alpha=0.3)
plt.plot(test_fd, label='original', alpha=0.7)
if return_conf_int:
    bounds = np.array(bounds)
    plt.fill_between(np.arange(len(test_fd)), bounds[:, 0], bounds[:, 1], alpha=0.3, color='green')
plt.legend()
plt.title(f'MA({best_q_ma}) {Tmax} rolling oos predictions')
plt.show()

# # Portmanteau Test to see if the residuals are white noise.
# lf.portmanteau_test(resid_ma, maxtau, show=True)

# ARMA Model.
# # Akaike Information Criterion (AIC) for choosing model order.
# best_aic = np.inf
# best_p = None
# best_q = None
# for p in np.arange(1, 10, dtype=np.int):
#     for q in np.arange(0, 10, dtype=np.int):
#         try:
#             _, _, _, _, aic = lf.fit_arima_model(x=fd, p=p, q=q, d=0, show=False)
#         except ValueError as err:
#             print(f'p:{p} - q:{q} - err:{err}')
#             continue
#         print(f'p:{p} - q:{q} - aic:{aic}')
#         if aic < best_aic:
#             best_p = p
#             best_q = q
#             best_aic = aic
# best_p = 1
# best_q = 3
# best_aic = -23921.22282779733
# print(f'AR order:{best_p}')
# print(f'MA order:{best_q}')
# print(f'Best AIC:{best_aic}')
# summary, fittedvalues, resid, model, aic = lf.fit_arima_model(x=fd, p=best_p, q=best_q, d=0, show=True)
# nrmseV, predM = lf.calculate_fitting_error(fd, model, tmax=10, show=True)
# lf.portmanteau_test(resid, maxtau, show=True)

# MA Model.
# Autocorrelation Criterion for choosing model order.
# Akaike Information Criterion (AIC) for choosing model order.
print("===============================================================================================================")
print("Exploring an MA Model for the Time Series:")
best_aic_arma = np.inf
best_p_arma = None
best_q_arma = None
for p in np.arange(1, 10, dtype=np.int):
    for q in np.arange(0, 10, dtype=np.int):
        try:
            _, _, _, _, aic = lf.fit_arima_model(x=fd, p=p, q=q, d=0, show=False)
        except ValueError as err:
            print("----------------------------------------------------------------------------------------------------"
                  "-----------")
            print(f'ARMA({p},{q}) Error ---> {err}')
            continue
        print("--------------------------------------------------------------------------------------------------------"
              "-------")
        print(f'ARMA({p},{q}) AIC ---> {aic}')
        if aic < best_aic_arma:
            best_p_arma = q
            best_q_arma = q
            best_aic_arma = aic
best_p_arma = 3
best_q_arma = 5
best_aic_arma = np.inf
summary_arma, fittedvalues_arma, resid_arma, model_arma, aic_arma = \
    lf.fit_arima_model(x=fd, p=best_p_arma, q=best_q_arma, d=0, show=True)
print("===============================================================================================================")
print("Summary of chosen ARMA Model:\n")
print(summary_arma)
nrmseV_arma, predM_arma = lf.calculate_fitting_error(fd, model_arma, tmax=10, show=True)

# Out of sample predictions for time horizon Tmax.
model_arma_train = pm.ARIMA(order=(best_p_arma, best_q_arma, 0))
model_arma_train.fit(train_fd)
preds_arma_train, conf_bounds_arma_train = \
    lf.predict_oos_multistep(model_arma_train, tmax=Tmax, return_conf_int=return_conf_int, alpha=alpha, show=False)
plt.figure()
plt.plot(np.arange(1, Tmax+1), preds_arma_train, label='predictions')
plt.plot(np.arange(1, Tmax+1), test_fd[:Tmax], label='original')
if return_conf_int:
    plt.fill_between(np.arange(1, Tmax+1), conf_bounds_arma_train[:, 0],
                     conf_bounds_arma_train[:, 1], color='green', alpha=0.3)
plt.legend()
plt.title(f'ARMA({best_p_arma},{best_q_arma}) oos predictions with horizon T={Tmax}')
plt.show()

# Rolling oos prediction.
preds = []
bounds = []
for i in test_fd:
    preds_arma_train_roll, conf_bounds_arma_train_roll = \
        model_arma_train.predict(n_periods=1, return_conf_int=return_conf_int, alpha=alpha)
    model_arma_train.update(i)
    preds.append(preds_arma_train_roll[0])
    bounds.append(conf_bounds_arma_train_roll[0])
plt.figure()
plt.plot(preds, label='predictions', linestyle='--', alpha=0.3)
plt.plot(test_fd, label='original', alpha=0.7)
if return_conf_int:
    bounds = np.array(bounds)
    plt.fill_between(np.arange(len(test_fd)), bounds[:, 0], bounds[:, 1], alpha=0.3, color='green')
plt.legend()
plt.title(f'ARMA({best_p_arma},{best_q_arma}) {Tmax} rolling oos predictions')
plt.show()

# # Portmanteau Test to see if the residuals are white noise.
# lf.portmanteau_test(resid_ma, maxtau, show=True)
