import great_expectations as ge
import pandas as pd
from uuid import uuid4
from datetime import datetime

# Initialize Great Expectations DataContext
context = ge.data_context.DataContext("/Users/shwetawani/Documents/XNode Project/XNode_project/great_expectations")

# Create an Expectation Suite if it doesn't exist
suite_name = "kafka_transaction_suite"
expectation_suite = context.create_expectation_suite(suite_name, overwrite_existing=True)


# Function to define expectations for the Kafka DataFrame
def define_expectations(df):
    batch = context.get_batch({
        "datasource_name": "transactions",  # Replace with your datasource
        "batch_kwargs": {
            "data_asset_name": "kafka_data",  # Name of your data
            "df": df  # This is your dataframe
        },
        "expectation_suite_name": suite_name
    })

    # Define column existence expectations
    batch.expect_column_to_exist("transaction_id")
    batch.expect_column_to_exist("transaction_date")
    batch.expect_column_to_exist("security_id")
    batch.expect_column_to_exist("trade_value")

    # Define data type expectations
    batch.expect_column_values_to_be_of_type("transaction_id", "uuid")
    batch.expect_column_values_to_be_of_type("transaction_date", "datetime")
    batch.expect_column_values_to_be_of_type("trade_value", "decimal")

    # Define more complex data validation checks
    batch.expect_column_values_to_be_unique("transaction_id")
    batch.expect_column_values_to_be_in_set("trade_type", ["buy", "sell"])

    # Validate the batch
    results = batch.validate()

    # Print the results
    print(results)

    # Optionally handle the results
    if not results["success"]:
        print("Some expectations failed.")
        for result in results["results"]:
            if not result["success"]:
                print(f"Expectation failed: {result['expectation_type']}")
                print(f"Details: {result['result']}")
                return False
    else:
        print("All expectations passed!")
        return True

