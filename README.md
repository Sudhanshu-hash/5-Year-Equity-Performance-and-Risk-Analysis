# 5-Year-Equity-Performance-and-Risk-Analysis
This project provides a comprehensive financial analysis of over 500 S&P 500 stocks from 2013 to 2018. It uses a robust Python-to-SQL data pipeline to clean historical price data and calculate key performance metrics (Cumulative Return, Volatility, etc.). The final, analyzed data is loaded into a MySQL database to power a detailed Power BI Dashboard focused on risk-adjusted returns and outlier detection.

***Category,Tool / Language Used***
1. Data Source: (all_stocks_5yr.csv).
2. Data Engineering: Python (pandas, numpy, sqlalchemy).
3. Database: MySQL.
4. Visualization: Power BI.

***(SQL Queries & Dashboard Content)***
The analysis focuses on answering critical investment questions using optimized SQL queries:
1. Top Performers : Ranking stocks by Cumulative Return and comparing them to Volatility.
2. Risk vs. Reward : Using a scatter plot to map Volatility against Average Daily Return .
3. Annual Trends: Year-over-year performance tracking for top stocks (e.g., NVDA, NFLX) to assess consistency.
4. Outlier Detection : Identifying the Top 10 Highest Volume Trading Days for key stocks to investigate major market events.





**🤝 Contribution**

*Feel free to suggest improvements, especially regarding:

*Adding the S&P 500 benchmark data for Beta and comparative analysis.

*Integrating Sector data for industry-specific comparison.

*Optimizing DAX measures for financial metrics like the Sharpe Ratio.
