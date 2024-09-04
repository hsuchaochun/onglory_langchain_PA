import mysql.connector
import config

# mysql db init
mydb = mysql.connector.connect(
    host=config.SQL_HOST,
    user=config.SQL_USR,
    password=config.SQL_PWD, 
    auth_plugin='mysql_native_password', 
    database=config.SQL_WP_DB
)
mycursor = mydb.cursor(buffered=True)