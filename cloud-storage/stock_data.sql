-- File: stock_data.sql (cloud deployment)
-- Author: Ty Rawls
-- Date: 2024-03-07
-- Description: Create tables to store the company information and daily stock price data. 
-- This procedure is initialized by 'db_init.sh'.

CREATE TABLE IF NOT EXISTS company_info(
	ticker VARCHAR(4) PRIMARY KEY,
	company_name VARCHAR(100),
	exchange VARCHAR(10),
	ceo VARCHAR(100),
	sector VARCHAR(100),
	industry VARCHAR(100),
    market_cap BIGINT,
	ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Audit column
);

CREATE TABLE IF NOT EXISTS daily_stock_data (
	date DATE,
	ticker VARCHAR(4),
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume INT,
	ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Audit column
	CONSTRAINT fk_ticker                              -- Set foreign key
    	FOREIGN KEY(ticker) 
    		REFERENCES company_info(ticker)
			ON DELETE CASCADE
);