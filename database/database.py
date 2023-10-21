import sqlite3

#Test Creating a DB 

def createTable():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Test (
        tid TEXT PRIMARY KEY,
        tname TEXT,
        amount DOUBLE)''')
    connector.commit()
    connector.close()

createTable()