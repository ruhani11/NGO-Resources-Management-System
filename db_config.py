import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rmp26521**",
        database="ngo_dbms"
    )
