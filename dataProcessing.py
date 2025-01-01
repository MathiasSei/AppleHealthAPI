import psycopg2
import sql_config

# Connection string
connection_string = sql_config.connection_string

def sql_connect_and_commit(query, params=None):
    # Connect to PostgreSQL
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    # Execute query
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    conn.commit()

    # Close connection
    cur.close()
    conn.close()

def clean_data(raw_data):
    # Round all values to integers
    for key, value in raw_data['drinks'].items():
        raw_data['drinks'][key] = int(float(value))
    return raw_data

def insert_data(data):
    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS drinks (
    user_id VARCHAR(255),
    datetime TIMESTAMP,
    amount INTEGER,
    PRIMARY KEY (user_id, datetime)
    );
    """
    sql_connect_and_commit(create_table_query)

    # Prepare data for bulk insertion
    values = [(data['user'], key, int(float(value))) for key, value in data['drinks'].items()]

    # Insert data into database with ON CONFLICT clause
    insert_query = """
    INSERT INTO drinks (user_id, datetime, amount)
    VALUES (%s, %s, %s)
    ON CONFLICT (user_id, datetime) DO UPDATE SET amount = EXCLUDED.amount
    """

    # Connect to PostgreSQL
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    # Execute the bulk insert
    cur.executemany(insert_query, values)
    conn.commit()

    # Close connection
    cur.close()
    conn.close()
    print("Data inserted successfully") 