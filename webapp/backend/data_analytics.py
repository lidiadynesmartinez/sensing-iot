import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima_model import ARIMA

from pylab import rcParams

import statsmodels.api as sm


def save_figure(xs, ys, filename, x_label="x", y_label="y"):
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(xs, ys)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)

    plt.savefig(f"static/img/{filename}", bbox_inches='tight')


def save_double_figure(xs, ys1, ys2, filename, x_label="x", y_label1="y1", y_label2="y2", title="title"):
    rcParams['figure.figsize'] = 7, 4
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(title)
    axis.set_xlabel(x_label)

    colour = "tab:red"
    axis.tick_params(axis='y', labelcolor=colour)
    axis.plot(xs, ys1, color=colour)
    axis.set_ylabel(y_label1, color=colour)

    twin = axis.twinx()
    colour = "tab:blue"
    twin.tick_params(axis='y', labelcolor=colour)
    twin.plot(xs, ys2, color=colour)
    twin.set_ylabel(y_label2, color=colour)

    fig.tight_layout()
    plt.savefig(f"static/img/{filename}", bbox_inches='tight')



# 1 year data: raw, trend, seasonal, residual
# 5 years data: raw, trend, seasonal, residual
# Correlation bar chart 1y5y
# Noise
# AR, MA, ARMA, ARIMA, VAR forecasting
# FFT


# 5 Years of data
weather = [10, 11, 7, 7, 5, 10, 9, 8, 7, 7, 11, 7, 5, 8, 6, 2, 10, 8, 9, 11, 13, 14, 21, 12, 18, 20, 20, 23, 24, 23, 21, 24, 27, 28, 26, 26, 28, 29, 24, 22, 21, 23, 22, 21, 18, 18, 18, 19, 17, 12, 11, 14, 12, 7, 12, 11, 7, 10, 9, 10, 8, 4, 6, 10, 10, 7, 8, 7, 7, 8, 9, 12, 12, 12, 14, 13, 12, 20, 19, 18, 19, 20, 23, 19, 21, 20, 22, 22, 26, 21, 22, 22, 21, 25, 22, 22, 23, 20, 17, 15, 14, 13, 15, 11, 9, 10, 9, 7, 11, 10, 9, 8, 7, 7, 5, 7, 9, 6, 12, 11, 9, 13, 13, 12, 16, 16, 13, 13, 13, 14, 16, 18, 24, 21, 19, 24, 25, 21, 26, 23, 22, 22, 23, 22, 24, 26, 23, 19, 17, 19, 19, 16, 18, 16, 16, 13, 10, 9, 9, 9, 7, 7, 8, 8, 11, 9, 13, 16, 12, 12, 18, 16, 16, 17, 17, 17, 21, 19, 18, 21, 23, 23, 22, 24, 23, 27, 27, 25, 24, 22, 20, 20, 24, 22, 23, 21, 19, 16, 18, 15, 17, 12, 13, 10, 9, 6, 7, 10, 8, 6, 10, 6, 6, 6, 5, 8, 8, 9, 11, 10, 11, 12, 11, 17, 16, 16, 14, 17, 16, 17, 16, 19, 20, 19, 23, 27, 23, 23, 20, 21, 24, 22, 22, 19, 17, 18, 17, 16, 16, 16, 13, 14, 17, 16, 13, 9, 9, 12, 11, 12, 12]
sunglasses = [17, 19, 18, 21, 18, 20, 21, 25, 28, 34, 49, 48, 44, 43, 43, 64, 51, 47, 50, 57, 64, 47, 50, 64, 56, 61, 59, 55, 55, 64, 57, 45, 35, 31, 27, 26, 26, 21, 20, 20, 17, 16, 15, 16, 15, 15, 14, 15, 17, 16, 16, 17, 19, 19, 20, 21, 21, 21, 23, 25, 24, 33, 37, 44, 40, 38, 62, 69, 68, 52, 47, 51, 52, 59, 60, 71, 59, 61, 79, 65, 54, 52, 45, 46, 41, 39, 34, 27, 26, 22, 22, 26, 20, 19, 17, 18, 17, 16, 15, 20, 17, 17, 16, 18, 22, 21, 22, 21, 23, 22, 27, 29, 30, 31, 34, 43, 39, 44, 45, 45, 58, 51, 69, 81, 63, 66, 72, 73, 49, 48, 51, 60, 55, 74, 58, 50, 51, 49, 47, 41, 29, 31, 25, 23, 23, 21, 20, 17, 16, 17, 18, 20, 21, 20, 17, 17, 22, 21, 22, 23, 24, 25, 23, 26, 27, 28, 36, 40, 42, 56, 67, 69, 52, 49, 52, 59, 52, 76, 72, 58, 70, 84, 60, 75, 66, 62, 47, 45, 41, 44, 39, 42, 31, 27, 24, 22, 21, 21, 19, 19, 18, 20, 19, 21, 20, 18, 18, 19, 21, 21, 24, 23, 24, 28, 27, 31, 33, 30, 32, 34, 39, 43, 42, 44, 87, 63, 61, 90, 76, 79, 76, 73, 71, 64, 100, 96, 81, 75, 71, 60, 56, 40, 34, 31, 30, 25, 24, 24, 21, 20, 20, 22, 19, 17, 18, 20, 19, 17, 18, 18, 19]
gloves = [30, 29, 29, 29, 32, 29, 30, 24, 24, 25, 22, 22, 23, 21, 19, 21, 20, 21, 20, 20, 20, 21, 20, 19, 20, 19, 20, 20, 19, 19, 19, 20, 20, 21, 21, 21, 23, 22, 25, 25, 32, 32, 29, 29, 40, 40, 43, 53, 62, 70, 55, 38, 40, 32, 36, 41, 34, 38, 30, 27, 28, 24, 25, 22, 24, 24, 21, 21, 22, 24, 24, 23, 22, 23, 20, 21, 22, 21, 18, 20, 20, 19, 21, 20, 20, 20, 21, 23, 25, 25, 26, 27, 27, 35, 34, 33, 33, 36, 48, 67, 58, 54, 51, 35, 29, 32, 43, 44, 29, 30, 30, 33, 30, 30, 30, 26, 26, 29, 28, 24, 23, 24, 22, 22, 25, 22, 23, 23, 23, 23, 21, 23, 23, 18, 21, 22, 21, 20, 20, 22, 25, 25, 26, 28, 34, 37, 38, 37, 45, 66, 55, 67, 79, 76, 58, 45, 41, 40, 37, 38, 43, 34, 36, 33, 30, 35, 29, 27, 25, 23, 24, 24, 25, 24, 25, 25, 23, 22, 23, 21, 23, 19, 21, 23, 24, 22, 23, 25, 23, 27, 28, 25, 29, 30, 32, 29, 33, 34, 32, 34, 44, 59, 62, 64, 90, 82, 100, 62, 46, 36, 42, 40, 36, 36, 42, 37, 36, 56, 37, 35, 36, 30, 28, 26, 24, 25, 25, 24, 23, 22, 22, 24, 24, 24, 23, 22, 22, 26, 23, 23, 23, 25, 25, 28, 29, 32, 34, 39, 38, 36, 40, 48, 68, 50, 47, 79, 74, 68, 82, 67, 43]
bitcoin = [5, 6, 6, 6, 6, 5, 6, 5, 9, 7, 4, 4, 4, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 4, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 3, 2, 4, 4, 3, 3, 2, 2, 2, 3, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 6, 4, 3, 3, 3, 3, 3, 4, 5, 5, 4, 4, 3, 3, 3, 3, 3, 5, 9, 8, 16, 10, 10, 11, 8, 8, 7, 8, 10, 9, 15, 14, 18, 14, 14, 16, 20, 14, 11, 11, 20, 22, 20, 29, 29, 30, 27, 66, 100, 81, 98, 54, 45, 43, 53, 37, 39, 49, 30, 23, 17, 18, 18, 16, 17, 18, 16, 15, 14, 12, 12, 11, 11, 10, 9, 12, 9, 10, 10, 9, 12, 12, 11, 11, 11, 10, 10, 11, 11, 10, 9, 8, 10, 9, 9, 8, 10, 11, 14, 14, 11, 11, 11, 10]


def save_fft_plot(data, filename, x_label="Frequency (Hz)", y_label="Amplitude", title="FFT"):
    rcParams['figure.figsize'] = 8, 4
    mean = np.mean(data)
    fft = np.fft.fft([x - mean for x in data])
    n = len(data)
    f = range(n)

    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.bar(f[:n//2], np.abs(fft)[:n//2] * 1/n)  # 1/n is a normalization factor
    fig.savefig(f"static/img/{filename}", bbox_inches='tight')


def save_tsr_plot(data, filename, title="Title"):
    rcParams['figure.figsize'] = 7, 7
    decomposed = sm.tsa.seasonal_decompose(data, freq=52)  # The frequency is weekly
    plot = decomposed.plot()
    plot.axes[0].set_title(title)
    plot.savefig(f"static/img/{filename}", bbox_inches='tight')


def calculate_correlation(xs, ys):
    return np.corrcoef(xs, ys)[0][1]


def calculate_ar(a1):
    model = ARIMA(a1, order=(15, 1, 5))
    model_fit = model.fit()
    print(model_fit.summary())
    # residuals = DataFrame(model_fit.resid)
    # residuals.plot()
    # plt.show()
    # residuals.plot(kind='kde')
    # plt.show()
    # print(residuals.describe())

    model_fit.plot_predict(start=260, end=265)
    plt.show()

