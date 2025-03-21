import snowflake.connector
import uuid

# Define the connection parameters
conn = snowflake.connector.connect(
    user='**',
    password='****',
    account='******',
    #warehouse='my_warehouse',
    database='my_database',
    schema='my_schema'
)

def load_securities():

    # Create a cursor object to interact with Snowflake
    cursor = conn.cursor()

    # Set the current database and schema
    cursor.execute("USE DATABASE my_database;")
    cursor.execute("USE SCHEMA my_schema;")

    # Step 1: Delete existing data in the 'securities' table
    delete_query = "DELETE FROM securities;"
    cursor.execute(delete_query)
    print("Existing data in 'securities' table has been deleted.")

    # Step 2: Sample data to insert into the 'securities' table
    data = [
        ('Apple Inc.', 'stock', 'Technology'),
        ('Tesla Inc.', 'stock', 'Automotive'),
        ('Microsoft Corp.', 'stock', 'Technology'),
        ('Bonds US Treasury', 'bond', 'Finance'),
        ('SPDR S&P 500 ETF', 'ETF', 'Finance'),
        ('Amazon.com Inc.', 'stock', 'E-commerce')
    ]

    # Insert data into 'securities' table
    insert_securities_query = """
    INSERT INTO securities (security_id, security_name, security_type, sector)
    VALUES
    """

    # Generate UUIDs and prepare data for insertion
    values = []
    for row in data:
        security_id = str(uuid.uuid4())  # Generate a UUID for each row
        security_name, security_type, sector = row
        values.append(f"('{security_id}', '{security_name}', '{security_type}', '{sector}')")

    # Join all values into a single string to form the insert statement
    insert_securities_query += ",\n".join(values) + ";"



    # Step 3: Execute the insert query
    try:
        cursor.execute(insert_securities_query)
        print("Sample data inserted into 'securities' table successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        #conn.close()

def load_regions():

    # Create a cursor object to interact with Snowflake
    cursor = conn.cursor()

    # Set the current database and schema
    cursor.execute("USE DATABASE my_database;")
    cursor.execute("USE SCHEMA my_schema;")

    # ========================= Populate regions metadata table =========================

    # Step 1: Delete existing data in the 'regions' table
    delete_query = "DELETE FROM regions;"
    cursor.execute(delete_query)
    print("Existing data in 'regions' table has been deleted.")

    # Step 2: Sample data to insert into the 'regions' table
    data = [
        ('North America', 'United States'),
        ('North America', 'Canada'),
        ('Europe', 'Germany'),
        ('Europe', 'France'),
        ('Europe', 'United Kingdom'),
        ('APAC', 'China'),
        ('APAC', 'Japan'),
        ('APAC', 'India'),
        ('South America', 'Brazil'),
        ('Africa', 'South Africa')
    ]

    # Insert data into 'regions' table
    insert_regions_query = """
    INSERT INTO regions (region_id, region_name, country)
    VALUES
    """

    # Generate UUIDs and prepare data for insertion
    values = []
    for row in data:
        region_id = str(uuid.uuid4())  # Generate a UUID for each row
        region_name, country = row
        values.append(f"('{region_id}', '{region_name}', '{country}')")

    # Join all values into a single string to form the insert statement
    insert_regions_query += ",\n".join(values) + ";"


    # Step 3: Execute the insert query
    try:
        cursor.execute(insert_regions_query)
        print("Sample data inserted into 'regions' table successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()