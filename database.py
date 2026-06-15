import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nethu@9697",
        database="fault_expert_system"
    )