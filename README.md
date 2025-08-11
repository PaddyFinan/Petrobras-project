Petrobras x Oil x FX Mini Analysis
1. Project Overview
This project looks at how Petrobras (PBR) stock returns move in relation to Brent crude oil prices, the USD/BRL exchange rate, and the Bovespa index. I wanted to see which factor had the strongest connection to Petrobras’ performance and whether oil or currency shifts played the bigger role.
The analysis uses real market data and focuses on the statistical relationships between these variables, backed up with visualizations and correlation matrices.

Main question:
Do Petrobras shares react more to changes in oil prices or to shifts in the Brazilian real’s exchange rate?

2. Skills Demonstrated
While building this, I:
Pulled real-world financial data with Python (using yfinance)
Cleaned and prepared time series data in pandas
Normalized price series to compare performance
Calculated returns and built correlation matrices
Created visualizations with matplotlib
Exported charts and statistical summaries for reporting
Used Git & GitHub for version control and project sharing
3. Results Summary
PBR vs. Bovespa Index: Strongest positive correlation (~0.91). Petrobras tends to move closely with the Brazilian stock market overall.
PBR vs. Brent Oil: Positive but weaker correlation (~0.62). Oil prices matter, but not as much as the general market index.
PBR vs. USD/BRL: Negative correlation (~-0.45). A stronger USD vs. BRL generally lines up with weaker Petrobras performance.
Oil vs. USD/BRL: Very small negative correlation (~-0.03), meaning currency changes don’t have much direct link to oil prices in this period.
Takeaway: Petrobras stock is most influenced by the Brazilian equity market, with oil prices playing a secondary role and currency fluctuations having a smaller but still noticeable effect.
4. How to Run
Clone the repository:
git clone https://github.com/PaddyFinan/Petrobras-project.git
cd Petrobras-project
Set up environment & install dependencies:
pip install -r requirements.txt
Run the analysis:
python pbr_mini_analysis.py
The charts and analysis outputs will be saved in the output/ folder.
5. Files in This Project
pbr_mini_analysis.py → Full Python analysis script
requirements.txt → Dependencies needed to run the script
output/ → Contains generated charts and results
README.md → Project overview and results summary
---
*Author: Padraic Finan*
