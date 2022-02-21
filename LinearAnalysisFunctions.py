from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


# Plot Time Series.
def plot_timeseries(x, value='', title='', savepath='', dates=None, zoomx=False, color='C0'):

    if dates is not None:
        plt.plot(dates, x, color=color, marker='x', linestyle='--', linewidth=1)
        plt.gcf().autofmt_xdate()
    else:
        plt.plot(x, color=color, marker='x', linestyle='--', linewidth=1)
        plt.xlabel('Time (Days)')
    plt.ylabel(value)
    if zoomx is True:
        left, right = plt.xlim()
        plt.xlim(right/2, right/2+right/3.5)
    if len(title) > 0:
        plt.title(title, x=0.5, y=1.0)
    if len(savepath) > 0:
        plt.savefig(f'{savepath}/{title} Time Series.png')


# Plot Histogram.
def plot_histogram(x, value, title='', savepath=''):

    plt.hist(x, alpha=0.8, rwidth=0.9)
    plt.xlabel(value)
    plt.ylabel('Frequency')
    plt.title('Histogram')
    if len(title) > 0:
        plt.title(title, x=0.5, y=1.0)
    if len(savepath) > 0:
        plt.savefig(f'{savepath}/{title}.png')


# Returns the Moving Average of a Time Series x with Length of Window.
def rolling_window(x, window):

    x = x.flatten()
    return np.convolve(x, np.ones(window) / window, mode='same')


# Fit to a given time series with a polynomial of a given order. x: vector of length 'n' of the time series
# p: the order of the polynomial to be fitted. return: vector of length 'n' of the fitted time series.
def polynomial_fit(x, p):

    n = x.shape[0]
    x = x[:]
    if p > 0:
        tv = np.arange(n)
        bv = np.polyfit(x=tv, y=x, deg=p)
        muv = np.polyval(p=bv, x=tv)
    else:
        muv = np.full(shape=n, fill_value=np.nan)
    return muv


# Calculate acf of timeseries xV to lag (lags) and show figure with confidence interval with (alpha).
def get_acf(x, lags=10, alpha=0.05, show=True):

    acfv = acf(x, nlags=lags)[1:]
    z_inv = norm.ppf(1 - alpha / 2)
    upperbound95 = z_inv / np.sqrt(x.shape[0])
    lowerbound95 = -upperbound95
    if show:
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.plot(np.arange(1, lags + 1), acfv, marker='o')
        ax.axhline(upperbound95, linestyle='--', color='red', label=f'Conf. Int {(1 - alpha) * 100}%')
        ax.axhline(lowerbound95, linestyle='--', color='red')
        ax.set_title('ACF')
        ax.set_xlabel('Lag')
        ax.set_xticks(np.arange(1, lags + 1))
        ax.grid(linestyle='--', linewidth=0.5, alpha=0.15)
        ax.legend()
    return acfv


# Calculate pacf of timeseries xV to lag (lags) and show figure with confidence interval with (alpha).
def get_pacf(xv, lags=10, alpha=0.05, show=True):

    pacfv = pacf(xv, nlags=lags)[1:]
    z_inv = norm.ppf(1 - alpha / 2)
    upperbound95 = z_inv / np.sqrt(xv.shape[0])
    lowerbound95 = -upperbound95
    if show:
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.plot(np.arange(1, lags + 1), pacfv, marker='o')
        ax.axhline(upperbound95, linestyle='--', color='red', label=f'Conf. Int {(1 - alpha) * 100}%')
        ax.axhline(lowerbound95, linestyle='--', color='red')
        ax.set_title('PACF')
        ax.set_xlabel('Lag')
        ax.set_xticks(np.arange(1, lags + 1))
        ax.grid(linestyle='--', linewidth=0.5, alpha=0.15)
        ax.legend()
    return pacfv


# # Computes the periodic time series comprised of repetetive patterns of seasonal components given a time series and
# # the season (period).
# def seasonal_components(x, period):
#
#     n = x.shape[0]
#     sv = np.full(shape=(n,), fill_value=np.nan)
#     monv = np.full(shape=(period,), fill_value=np.nan)
#     for i in np.arange(period):
#         monv[i] = np.mean(x[i:n:period])
#     monv = monv - np.mean(monv)
#     for i in np.arange(period):
#         sv[i:n:period] = monv[i] * np.ones(shape=len(np.arange(i, n, period)))
#     return sv


# PORTMANTEAULB hypothesis test (H0) for independence of time series: tests jointly that several autocorrelations
# are zero. It computes the Ljung-Box statistic of the modified sum of autocorrelations up to a maximum lag, for
# maximum lags 1,2,...,maxtau.
def portmanteau_test(xv, maxtau, show=False):

    ljung_val, ljung_pval = acorr_ljungbox(xv, lags=maxtau)
    if show:
        fig, ax = plt.subplots(1, 1)
        ax.scatter(np.arange(len(ljung_pval)), ljung_pval)
        ax.axhline(0.05, linestyle='--', color='r')
        ax.set_title('Ljung-Box Portmanteau test')
        ax.set_yticks(np.arange(0, 1.1))
        plt.show()
    return ljung_val, ljung_pval


# Fit ARIMA(p, d, q) in xv returns: summary (table), fittedvalues, residuals, model, AIC.
def fit_arima_model(x, p, q, d=0, show=False):

    model = ARIMA(x, order=(p, d, q)).fit()
    summary = model.summary()
    fittedvalues = model.fittedvalues
    fittedvalues = np.array(fittedvalues).reshape(-1, 1)
    resid = model.resid
    if show:
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.plot(x, label='Original', color='blue')
        ax.plot(fittedvalues, label='FittedValues', color='red', linestyle='--', alpha=0.9)
        ax.legend()
        ax.set_title(f'ARIMA({p}, {d}, {q})')
        fig, ax = plt.subplots(2, 1, figsize=(14, 8))
        ax[0].hist(resid, label='Residual')
        ax[1].scatter(np.arange(len(resid)), resid)
        plt.title('Residuals')
        plt.legend()
    return summary, fittedvalues, resid, model, model.aic


# Calculate fitting error with NRMSE for given model in timeseries xv till prediction horizon Tmax. Returns: nrmsev
# preds: for timesteps T=1, 2, 3.
def calculate_fitting_error(xv, model, tmax=20, show=False):

    nrmsev = np.full(shape=tmax, fill_value=np.nan)
    nobs = len(xv)
    xvstd = np.std(xv)
    # vartar = np.sum((xv - np.mean(xv)) ** 2)
    predm = []
    tmin = np.max(
        [len(model.arparams), len(model.maparams), 1])  # Start prediction after getting all lags needed from model.
    for T in np.arange(1, tmax):
        errors = []
        predv = np.full(shape=nobs, fill_value=np.nan)
        for t in np.arange(tmin, nobs - T):
            pred_ = model.predict(start=t, end=t + T - 1, dynamic=True)
            # predv.append(pred_[-1])
            ytrue = xv[t + T - 1]
            predv[t + T - 1] = pred_[-1]
            error = pred_[-1] - ytrue
            errors.append(error)
        predm.append(predv)
        errors = np.array(errors)
        mse = np.mean(np.power(errors, 2))
        rmse = np.sqrt(mse)
        nrmsev[T] = (rmse / xvstd)
        # nrmsev[T] = (np.sum(errors**2) / vartar)

    if show:
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.plot(np.arange(1, tmax), nrmsev[1:], marker='x', label='NRMSE')
        ax.axhline(1, color='red', linestyle='--')
        ax.set_title('Fitting Error')
        ax.legend()
        ax.set_xlabel('T')
        ax.set_xticks(np.arange(1, tmax))
        plt.show()
        # Plot multistep prediction for T=1, 2, 3
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.plot(xv, label='original')
        colors = ['red', 'green', 'black']
        for i, preds in enumerate(predm[:3]):
            ax.plot(preds, color=colors[i], linestyle='--', label=f'T={i + 1}', alpha=0.7)
        ax.legend(loc='best')
        plt.show()
    return nrmsev, predm
