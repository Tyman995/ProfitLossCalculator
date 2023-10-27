import sqlite3

#Test Creating a DB 

def createTable():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
        tid INTEGER PRIMARY KEY AUTOINCREMENT,
        t_type TEXT,
        note TEXT,
        date DATE,
        amount REAL)''')
    
    connector.commit()
    connector.close()

def insert_transaction(t, n, d, a):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        INSERT INTO Transactions(t_type, note, date, amount)
        VALUES(?, ?, ?, ?)''',(t,n,d,a)) 
    #ensure date gets passed as a string to prevent numeric type from doing calculations such as subtraction    
    connector.commit()
    connector.close()

def update_transaction(new_t_type, new_name, new_date, new_amount, tid):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''UPDATE Transactions SET t_type = ?, note = ?, date = ?, amount = ? WHERE tid = ?''', (new_t_type, new_name, new_date, new_amount, tid))
    connector.commit()
    connector.close()

def delete_transaction(tid):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''DELETE FROM Transactions WHERE tid = ?''', (tid,))
    connector.commit()
    connector.close()

def fetch_transactions():
    conn = sqlite3.connect('ProfitLoss.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

createTable()

#type, amt, date, op        <- For insert paramaters when ready
#VALUES({y}, {amt}, {date}, {op})''')