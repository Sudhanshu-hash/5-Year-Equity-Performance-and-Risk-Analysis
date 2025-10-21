-- select * from stock_analysis_db.daily_prices;
-- select * from stock_analysis_db.stock_summary;


-- 1. Summary Query: Top Performing Stocks
SELECT Name,ROUND(Cumulative_Return_Pct, 2) AS Cumulative_Return,Volatility,ROUND(avg_close, 2) AS Average_Closing_Price
FROM stock_summary ORDER BY Cumulative_Return_Pct DESC LIMIT 5;


-- 2. Daily Data Query: Highest Priced Stock on the Last Day
SELECT t1.Name,t1.date,t1.close AS Highest_Close_Price FROM daily_prices t1
INNER JOIN (
    -- Subquery finds the absolute latest date in the entire table
    SELECT MAX(date) AS latest_date FROM daily_prices)
t2 ON t1.date = t2.latest_date
ORDER BY t1.close DESC LIMIT 1;


-- 3. Combined (JOIN) Query: Latest Price for the Top Performers
SELECT d.Name,d.date AS Latest_Date, d.close AS Latest_Close_Price, s.Cumulative_Return_Pct
FROM daily_prices d INNER JOIN stock_summary s ON d.Name = s.Name
INNER JOIN (SELECT MAX(date) AS latest_date FROM daily_prices) -- Find the latest date
AS max_date ON d.date = max_date.latest_date
INNER JOIN (SELECT Name FROM stock_summary ORDER BY Cumulative_Return_Pct DESC LIMIT 3)--  Find the top 3 performing stock names
AS top_stocks ON d.Name = top_stocks.Name ORDER BY s.Cumulative_Return_Pct DESC;

-- 4. Comparison Query: Risk vs. Reward (Average Return and Volatility)
SELECT Name,ROUND(avg_percent_change, 4) AS Avg_Daily_Price_Change_Pct,Volatility,ROUND(avg_open, 2) AS Average_Open_Price
FROM stock_summary ORDER BY Avg_Daily_Price_Change_Pct DESC;

-- 5. Trend Query: Annual Performance of top 5 performing stocks(NVDA, NFLX, ALGN, EA, STZ)
SELECT Name, YEAR(date) AS Trading_Year,
    SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date ASC), ',', 1) AS Year_Start_Price,
    SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date DESC), ',', 1) AS Year_End_Price,
    (
        SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date DESC), ',', 1) - 
        SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date ASC), ',', 1)
    ) / SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date ASC), ',', 1) * 100 AS Annual_Return_Pct
FROM daily_prices WHERE Name IN ('NVDA', 'NFLX', 'ALGN', 'EA', 'STZ')
GROUP BY Name, Trading_Year ORDER BY Name, Trading_Year;

-- 6. Outlier Query: Top 10 Highest Volume Trading Days for top 5 performing stocks(NVDA, NFLX, ALGN, EA, STZ)
SELECT Name, date, Closing_Price, volume, volume_rank
FROM (
    SELECT Name,date, close AS Closing_Price,
	volume,ROW_NUMBER() OVER (PARTITION BY Name ORDER BY volume DESC) as volume_rank
FROM daily_prices WHERE Name IN ('NVDA', 'NFLX', 'ALGN', 'EA', 'STZ')
) AS ranked_days 
WHERE volume_rank <= 10 ORDER BY Name, volume DESC;