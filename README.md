# Petrobras x Oil x FX Mini Analysis

## 1. Project Overview
This project investigates the relationships between Petrobras (PBR) stock returns, Brent crude oil prices, USD/BRL exchange rates, and the Bovespa index. The analysis focuses on identifying which factor most strongly influences Petrobras' performance, with a particular focus on the role of oil prices and currency movements.

**Key Question:** How do oil prices and FX rates influence Petrobras’ stock returns?

## 2. Skills Demonstrated
- **Web Scraping & Data Acquisition**: Downloading financial market data from Yahoo Finance using the `yfinance` library.
- **Python Data Analysis**: Using `pandas` for data manipulation and cleaning.
- **Data Cleaning**: Handling missing values, forward-filling gaps, and aligning time series.
- **Financial Transformations**: Calculating daily percentage returns and rebasing price series.
- **Statistical Analysis**: Creating correlation matrices and running multiple linear regressions (`statsmodels`).
- **Visualization**: Building time series plots, scatter plots, and rolling correlation charts with `matplotlib`.
- **Econometric Interpretation**: Understanding beta coefficients, p-values, and R² in financial contexts.

## 3. Methodology
1. **Data Source**: Yahoo Finance via `yfinance.download()` for:
   - `PBR`: Petrobras ADR (USD)
   - `BZ=F`: Brent crude oil futures (USD)
   - `BRL=X`: USD to Brazilian Real exchange rate
   - `^BVSP`: Bovespa Index (BRL)
2. **Data Cleaning**:
   - Keep only Adjusted Close prices.
   - Remove rows with all missing values.
   - Forward-fill small gaps.
3. **Analysis Steps**:
   - Calculate daily returns.
   - Compute correlations between all assets.
   - Run OLS regression: `PBR_ret ~ Brent_ret + USDBRL_ret`.
   - Create 3 visualizations: rebased prices, scatter plot, and rolling correlations.

## 4. Key Results

### Correlation Matrix (Daily Returns)
- **PBR vs Bovespa**: Highest positive correlation, indicating Petrobras moves closely with the Brazilian stock market.
- **PBR vs Brent**: Moderate positive correlation, showing oil prices influence Petrobras but less than Bovespa.
- **PBR vs USD/BRL**: Negative correlation, meaning Petrobras tends to rise when the Real strengthens vs USD.

### Regression Results (OLS)
- **Brent Returns**: Positive and statistically significant (p < 0.05), confirming oil prices are an important driver.
- **USD/BRL Returns**: Negative coefficient, sometimes insignificant, meaning FX effects are weaker than oil price effects.
- **R²**: Indicates how much of Petrobras’ daily return variation is explained by oil and FX.

## 5. Statistical Significance
- **p-value < 0.05**: Strong evidence the relationship is real, not due to chance.
- In this analysis, Brent's coefficient met this threshold, confirming its role as a primary driver.

## 6. Visualizations
1. **Rebased Prices** (`rebased_prices.png`):
   - Compares cumulative performance of PBR, Brent, and Bovespa since the start date.
2. **Scatter Plot** (`scatter_brent_pbr.png`):
   - Shows relationship between Brent and Petrobras daily returns with regression line.
3. **Rolling Correlations** (`rolling_correlations.png`):
   - Tracks 90-day moving correlations over time between Petrobras and each driver.

## 7. Conclusion
- Petrobras stock is **most correlated with the Bovespa index**.
- Oil prices (Brent) are the **most statistically significant external driver** of Petrobras returns.
- FX (USD/BRL) plays a smaller role compared to oil and the Brazilian market index.

---
*Author: Padraic Finan*
