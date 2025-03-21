# main.py
from snowflake.generate_schema import generate_schema
from snowflake.load_metadata_tables import load_securities, load_regions


def main():
    # Call metadata loading functions to load the data
    generate_schema()
    print("Snowflake schema generated successfully!")

    load_securities()
    load_regions()

    print("Metadata loaded successfully!")

if __name__ == "__main__":
    main()
