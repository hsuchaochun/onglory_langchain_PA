import mysql.connector
import config

# MySQL database initialization
def initialize_database():
    """Initialize and return MySQL database connection and cursor."""
    db_config = {
        'host': config.SQL_HOST,
        'user': config.SQL_USR,
        'password': config.SQL_PWD,
        'auth_plugin': 'mysql_native_password',
        'database': config.SQL_WP_DB
    }
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None, None

# Create database connection and cursor
mydb, mycursor = initialize_database()