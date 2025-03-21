def generate_schema():
    import snowflake.connector

    # Define the connection parameters
    conn = snowflake.connector.connect(
        user='**',
        password='*****',
        account='****',
        #warehouse='my_warehouse',
        database='my_database',
        schema='my_schema'
    )

    # Create a cursor object to interact with Snowflake
    cursor = conn.cursor()

    # Set the current database and schema
    cursor.execute("USE DATABASE my_database;")
    cursor.execute("USE SCHEMA my_schema;")

    # Create the 'securities' table
    create_securities_table = """
    CREATE OR REPLACE TABLE securities (
        security_id STRING PRIMARY KEY,    -- Unique identifier for the security (UUID stored as STRING)
        security_name VARCHAR,            -- Name of the security
        security_type VARCHAR,            -- Type of the security (e.g., stock, bond, ETF, etc.)
        sector VARCHAR                    -- The sector the security belongs to (e.g., technology, finance)
    );
    """

    # Create the 'regions' table
    create_regions_table = """
    CREATE OR REPLACE TABLE regions (
        region_id STRING PRIMARY KEY,     -- Unique identifier for the region (UUID stored as STRING)
        region_name VARCHAR,              -- Name of the region (e.g., North America, Europe, APAC)
        country VARCHAR                   -- Country within the region (e.g., USA, Germany, Japan)
    );
    """

    # Create the 'transactions' table
    create_transactions_table = """
    CREATE OR REPLACE TABLE transactions (
        transaction_id STRING,             -- Unique identifier for the transaction (UUID stored as STRING)
        transaction_date TIMESTAMP_LTZ,    -- Date when the transaction occurred (valid time)
        security_id STRING,               -- Reference to the security (foreign key to Securities)
        region_id STRING,                 -- Reference to the region (foreign key to Regions)
        trade_volume DECIMAL(20, 5),      -- Number of units traded
        trade_value DECIMAL(20, 5),       -- Dollar value of the trade
        security_type VARCHAR,            -- Type of security (e.g., stock, bond, ETF, etc.)
        trade_type VARCHAR,               -- Type of trade (buy/sell)
        price_per_unit DECIMAL(20, 5),    -- Price per unit of the security
        valid_from TIMESTAMP_LTZ,         -- Timestamp indicating when this data record became valid (valid time)
        valid_to TIMESTAMP_LTZ,           -- Timestamp indicating when this data record was no longer valid (valid time)
        transaction_from TIMESTAMP_LTZ,   -- Timestamp when the data was entered into the system (transaction time)
        transaction_to TIMESTAMP_LTZ,     -- Timestamp when the data record was deleted or updated in the system (transaction time)
    
        -- Optional: Add foreign key constraints (assuming you have tables `Securities` and `Regions`)
        CONSTRAINT fk_security_id FOREIGN KEY (security_id) REFERENCES securities(security_id),
        CONSTRAINT fk_region_id FOREIGN KEY (region_id) REFERENCES regions(region_id)
    );
    """

    # Create the 'transaction_summary' table
    create_transaction_summary_table = """
    CREATE OR REPLACE TABLE transaction_summary (
        transaction_date DATE,              -- Date of the aggregated data
        security_type VARCHAR,              -- Type of security (e.g., stock, bond, ETF)
        region_name VARCHAR,                -- Name of the region
        total_trade_volume DECIMAL(20, 5),  -- Total number of units traded
        total_trade_value DECIMAL(20, 5)    -- Total dollar value of trades
    );
    """

    # Create the table 'historical_prices'
    create_historical_prices_table = """
    CREATE OR REPLACE TABLE historical_prices (
        security_id STRING,              -- Unique identifier for the security (UUID stored as STRING)
        date DATE,                       -- Date of the price record
        closing_price DECIMAL(20, 5),    -- Closing price of the security on that date
        open_price DECIMAL(20, 5),       -- Opening price of the security on that date
        high_price DECIMAL(20, 5),       -- Highest price of the security on that date
        low_price DECIMAL(20, 5)         -- Lowest price of the security on that date
    );
    """

    # Create the 'performance_metrics' table
    create_performance_metrics_table = """
    CREATE OR REPLACE TABLE performance_metrics (
        performance_id STRING,            -- Unique identifier for the performance record (UUID stored as STRING)
        security_id STRING,              -- Reference to the security (foreign key to Securities)
        start_date DATE,                 -- Start date of the performance calculation period (valid time)
        end_date DATE,                   -- End date of the performance calculation period (valid time)
        roi DECIMAL(20, 5),              -- Return on Investment over the period
        volatility DECIMAL(20, 5),       -- Volatility (standard deviation of returns) over the period
        sharpe_ratio DECIMAL(20, 5),     -- Sharpe ratio for the asset (optional)
        valid_from TIMESTAMP_LTZ,        -- Timestamp when the performance data was valid (valid time)
        valid_to TIMESTAMP_LTZ,          -- Timestamp when the performance data was no longer valid (valid time)
        transaction_from TIMESTAMP_LTZ,  -- Timestamp when the performance data was entered into the system (transaction time)
        transaction_to TIMESTAMP_LTZ,    -- Timestamp when the performance data was deleted or updated in the system (transaction time)
    
        -- Foreign key constraint (assuming the Securities table exists)
        CONSTRAINT fk_security_id FOREIGN KEY (security_id) REFERENCES securities(security_id)
    );
    """

    # Create the 'transaction_metrics' table
    create_transaction_metrics_table = """
    CREATE OR REPLACE TABLE transaction_metrics (
        security_id STRING,             -- Unique identifier for the security (UUID stored as STRING)
        region_id STRING,               -- Unique identifier for the region (UUID stored as STRING)
        date DATE,                      -- Date of the aggregated data
        average_trade_volume DECIMAL(20, 5),  -- Average trade volume per day for the security
        max_trade_volume DECIMAL(20, 5),      -- Maximum trade volume for the security on that day
        trade_volume_std_dev DECIMAL(20, 5)   -- Standard deviation of trade volume
    );
    """

    # Create the 'anomalies' table
    create_anomalies_table = """
    CREATE OR REPLACE TABLE anomalies (
        anomaly_id STRING,               -- Unique identifier for the anomaly record (UUID stored as STRING)
        security_id STRING,              -- Reference to the security (foreign key to Securities)
        region_id STRING,                -- Reference to the region (foreign key to Regions)
        date DATE,                       -- Date of the detected anomaly (valid time)
        anomaly_type VARCHAR,            -- Type of anomaly (e.g., high volume, price spike, etc.)
        anomaly_score DECIMAL(20, 5),    -- A score representing the severity of the anomaly
        description VARCHAR,             -- Description of the anomaly
        valid_from TIMESTAMP_LTZ,        -- Timestamp when the anomaly data was valid (valid time)
        valid_to TIMESTAMP_LTZ,          -- Timestamp when the anomaly data was no longer valid (valid time)
        transaction_from TIMESTAMP_LTZ,  -- Timestamp when the anomaly data was entered into the system (transaction time)
        transaction_to TIMESTAMP_LTZ,    -- Timestamp when the anomaly data was deleted or updated in the system (transaction time)
    
        -- Foreign key constraints (assuming the Securities and Regions tables exist)
        CONSTRAINT fk_security_id FOREIGN KEY (security_id) REFERENCES securities(security_id),
        CONSTRAINT fk_region_id FOREIGN KEY (region_id) REFERENCES regions(region_id)
    );
    """


    # Execute the SQL statements
    try:
        # Create 'securities' table
        cursor.execute(create_securities_table)
        print("Table 'securities' created successfully.")

        # Create 'regions' table
        cursor.execute(create_regions_table)
        print("Table 'regions' created successfully.")

        # Create 'transactions' table
        cursor.execute(create_transactions_table)
        print("Table 'transactions' created successfully.")

        # Create 'transaction_summary' table
        cursor.execute(create_transaction_summary_table)
        print("Table 'transaction_summary' created successfully.")

        # Create 'historical_prices' table
        cursor.execute(create_historical_prices_table)
        print("Table 'historical_prices' created successfully.")

        # Create 'performance_metrics' table
        cursor.execute(create_performance_metrics_table)
        print("Table 'performance_metrics' created successfully.")

        # Create 'transaction_metrics' table
        cursor.execute(create_transaction_metrics_table)
        print("Table 'transaction_metrics' created successfully.")

        # Create 'anomalies' table
        cursor.execute(create_anomalies_table)
        print("Table 'anomalies' created successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()