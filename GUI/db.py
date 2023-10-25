import sqlite3

#Test Creating a DB 

def createTable():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
        tid INTEGER PRIMARY KEY AUTOINCREMENT,
        t_type TEXT,
        amount REAL,
        date DATE,
        note TEXT)''')
    
    connector.commit()
    connector.close()

def insertValues(type, amt, date, op):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        INSERT INTO Transactions(t_type, amount, date, note)
        VALUES('Revanue', 95.23, 2023-02-02, 'test2')''')
    connector.commit()
    connector.close()
createTable()
insertValues()
                   
#VALUES({y}, {amt}, {date}, {op})''')