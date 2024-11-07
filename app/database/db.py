import mysql.connector 
import os
from mysql.connector import Error 


def create_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
            )               
        print('coneccion exitosa a la base de datos')
    except Error as e:
        print('no fue posible conectarse a la base de datos ', e)
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        connection.commit()
        
        print('se ejecuto correctamente')
    except Error as e:
        print('no fue posible ejecutarse')
    
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print('no fue posible ejecutarse')
    
        
        
    