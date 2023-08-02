import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stocks_df = pd.read_csv("prices.csv",parse_dates=True)

def normalize_stocks(df):
    df_ = df.copy() # it is a good idea in general to make a copy
    for stock in df_.columns[1:]:
        df_[stock] = df_[stock] / df_.loc[0, stock]
    return df_

norm_stocks_df = normalize_stocks(stocks_df)


plt.figure()
norm_stocks_df.plot(figsize=(10,6))

stocks_daily_return = np.log(stocks_df[stocks_df.columns[1:]] / 
                             stocks_df[stocks_df.columns[1:]].shift(1))

stocks_daily_return.dropna(inplace=True)

plt.figure()
stocks_daily_return.boxplot(figsize=(12, 10), grid=False)
plt.title("Daily returns of the stocks")
plt.tight_layout()


beta,alpha = dict(), dict()
fig, axes = plt.subplots(5,2, dpi=150, figsize=(8,15))
axes = axes.flatten()
for idx, stock in enumerate(stocks_daily_return.columns):
    if stock != "date" and stock != "^GSPC":
        stocks_daily_return.plot(kind = "scatter", x = "^GSPC", y = stock, ax=axes[idx-1])
        b_, a_ = np.polyfit(stocks_daily_return[stock], stocks_daily_return["^GSPC"], 1)
        regression_line = b_ * stocks_daily_return["^GSPC"] + a_
        axes[idx-1].plot(stocks_daily_return["^GSPC"], regression_line, "-", color = "r")
        beta[stock] = b_
        alpha[stock] = a_

plt.suptitle("Beta estimation", size=20)
plt.tight_layout()

print('beta of stocks: ', beta)
print('alphas: ', alpha)