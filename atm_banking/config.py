import mysql_connector
def get_db_connection():
    connection = mysql_connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = "atm_banking"
    )
    
    return connection