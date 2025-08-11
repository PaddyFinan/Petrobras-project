# --- Petrobras x Oil x FX: Beginner-Friendly Mini Analysis ---

# 1) Import the Python libraries we need
import os  # lets us create folders and work with file paths
import pandas as pd  # handles data tables and analysis
import matplotlib.pyplot as plt  # creates charts and graphs
import yfinance as yf  # downloads market data from Yahoo Finance
import statsmodels.api as sm  # runs statistical models like regression

# 2) Define settings for our analysis
TICKERS = ["PBR", "BZ=F", "BRL=X", "^BVSP"]  
# PBR = Petrobras ADR (in USD)
# BZ=F = Brent crude oil futures (in USD)
# BRL=X = USD to Brazilian Real exchange rate
# ^BVSP = Bovespa index (Brazil's stock market benchmark)

START = "2016-01-01"  # start date for our analysis
END = None  # None means "today"

OUTDIR = "output"  # folder to save charts
os.makedirs(OUTDIR, exist_ok=True)  # create the folder if it doesn't exist

# 3) Download price data from Yahoo Finance
data = yf.download(TICKERS, start=START, end=END, auto_adjust=True)

# --- robust price extractor: handles MultiIndex / missing fields ---
def extract_prices(df: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """
    Return a wide DataFrame of prices for the requested tickers.
    Works whether yfinance returns MultiIndex (Field, Ticker) or single-index columns.
    With auto_adjust=True, 'Close' is already adjusted; fall back to 'Adj Close' if present.
    """
    if isinstance(df.columns, pd.MultiIndex):
        level0 = df.columns.get_level_values(0)
        field = "Close" if "Close" in level0 else ("Adj Close" if "Adj Close" in level0 else None)
        if field is None:
            raise KeyError("Neither 'Close' nor 'Adj Close' found in downloaded data.")
        out = df[field].copy()  # -> columns are tickers
    else:
        # Sometimes yfinance already returns tickers as columns
        if "Close" in df.columns:
            out = df["Close"].copy()
        elif "Adj Close" in df.columns:
            out = df["Adj Close"].copy()
        else:
            out = df.copy()  # assume columns are already tickers

    # Keep only the tickers we asked for (ignore any extras)
    common = [t for t in tickers if t in out.columns]
    if not common:
        raise KeyError("None of the requested tickers found in the price table.")
    return out[common].sort_index()

# 4) Get the prices table using the robust extractor
prices = extract_prices(data, TICKERS)

# 5) Clean the data
prices = prices.dropna(how="all").ffill()

# 6) Calculate daily returns for each series
rets = prices.pct_change().dropna()
rets = rets.rename(columns={
    "PBR": "PBR_ret",
    "BZ=F": "Brent_ret",
    "BRL=X": "USDBRL_ret",
    "^BVSP": "Bovespa_ret"
})

# 7) Correlation matrix
corr_matrix = rets.corr()
print("\n=== Daily Return Correlations ===")
print(corr_matrix.round(3))

# 8) Rolling correlation over 90-day windows
roll_window = 90
rolling_corr_brent = rets["PBR_ret"].rolling(roll_window).corr(rets["Brent_ret"])
rolling_corr_fx = rets["PBR_ret"].rolling(roll_window).corr(rets["USDBRL_ret"])
rolling_corr_bvsp = rets["PBR_ret"].rolling(roll_window).corr(rets["Bovespa_ret"])

# 9) Regression: Petrobras returns explained by Brent oil and FX
Y = rets["PBR_ret"]  # dependent variable
X = rets[["Brent_ret", "USDBRL_ret"]]  # independent variables
X = sm.add_constant(X)  # adds intercept to the regression
model = sm.OLS(Y, X).fit()
print("\n=== OLS Regression: PBR_ret ~ Brent_ret + USDBRL_ret ===")
print(model.summary())

# 10) Plot: Rebased prices (100 = first valid price for each series)
def rebase_to_100(df: pd.DataFrame) -> pd.DataFrame:
    # divide each column by its own first non-NaN value, then *100
    first_vals = df.apply(lambda s: s.loc[s.first_valid_index()], axis=0)
    return df.divide(first_vals) * 100

rebased = rebase_to_100(prices)[["PBR", "BZ=F", "^BVSP"]].dropna(how="all")
ax = rebased.plot(figsize=(11, 6), title="Rebased Prices (100 = first valid day)")
ax.set_ylabel("Index Level")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "rebased_prices.png"), dpi=160)
plt.close()

# 11) Plot: Scatter of Petrobras vs Brent returns
plt.figure(figsize=(7, 6))
plt.scatter(rets["Brent_ret"], rets["PBR_ret"], s=8, alpha=0.5)
b = model.params
xline = pd.Series(sorted(rets["Brent_ret"].values))
yline = b["const"] + b["Brent_ret"] * xline
plt.plot(xline, yline, color="red", linewidth=2)
plt.title("Petrobras vs Brent Daily Returns")
plt.xlabel("Brent returns")
plt.ylabel("PBR returns")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "scatter_brent_pbr.png"), dpi=160)
plt.close()

# 12) Plot: Rolling correlations
plt.figure(figsize=(11, 6))
plt.plot(rolling_corr_brent, label="PBR ~ Brent")
plt.plot(rolling_corr_fx, label="PBR ~ USD/BRL")
plt.plot(rolling_corr_bvsp, label="PBR ~ Bovespa")
plt.axhline(0, linewidth=1, color="black")
plt.legend()
plt.title("Rolling 90-Day Correlations")
plt.ylabel("Correlation")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "rolling_correlations.png"), dpi=160)
plt.close()

# Save correlation matrix and OLS summary to files for the repo
corr_matrix.round(4).to_csv(os.path.join(OUTDIR, "correlations.csv"))

with open(os.path.join(OUTDIR, "ols_summary.txt"), "w") as f:
    f.write(str(model.summary()))

print(f"\nCharts saved in: {os.path.abspath(OUTDIR)}")