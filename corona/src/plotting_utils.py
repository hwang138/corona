import math
import warnings

import matplotlib.pyplot as plt

from corona.src import utils


warnings.filterwarnings("ignore")


def plot_time_series(data, x, y, ax_factor, fontsize):

    df = data
    y_list = utils.generate_list(y)

    factor_list = list(df.sort_values(by=y, ascending=False)[ax_factor].unique())

    max_col_count = 2
    if len(factor_list) <= max_col_count:
        max_col_count = len(factor_list)
        max_row_count = 1
    else:
        max_row_count = math.ceil(len(factor_list) / max_col_count)

    num = max_row_count * 100 + max_col_count * 10 + 1

    plt.figure(num=num, figsize=(20, 10), facecolor="w", edgecolor="k")

    for factor in factor_list:
        subset_df = df.query(f"{ax_factor} == @factor")

        for y in y_list:

            plt.subplot(num)
            plt.plot(subset_df[x], subset_df[y], "--+", label=y.replace("_", " "))
            plt.title(factor.replace("_", " "), fontsize=fontsize)
            plt.ylabel(y.replace("_", " "), fontsize=fontsize)
            plt.xticks(rotation=45)
            plt.legend(loc="upper left", fontsize=fontsize)
        num += 1
    plt.tight_layout(pad=3.0)

    # plt.suptitle(" & ".join(y_list).replace('_', ' ') + f" by {ax_factor.replace('_', ' ')}", fontsize=fontsize, verticalalignment="top")
    return plt.show()
