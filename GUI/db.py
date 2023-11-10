import sqlite3
import pandas as pd
import re
#Test Creating a DB 

def createTable():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
        tid INTEGER PRIMARY KEY AUTOINCREMENT,
        t_type TEXT,
        check_id TEXT,
        note TEXT,
        date DATE,
        amount DECIMAL)''')
    
    connector.commit()
    connector.close()

def insert_transaction(t, c, n, d, a):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''
        INSERT INTO Transactions(t_type, check_id, note, date, amount)
        VALUES(?, ?, ?, ?, ?)''',(t, c, n, d, a)) 
    #ensure date gets passed as a string to prevent numeric type from doing calculations such as subtraction    
    connector.commit()
    connector.close()

def update_transaction(new_t_type, new_check_id, new_name, new_date, new_amount, tid):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''UPDATE Transactions SET t_type = ?, check_id = ?, note = ?, date = ?, amount = ? WHERE tid = ?''', (new_t_type, new_check_id, new_name, new_date, new_amount, tid))
    connector.commit()
    connector.close()

def delete_transaction(tid):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''DELETE FROM Transactions WHERE tid = ?''', (tid,))
    connector.commit()
    connector.close()

def fetch_transactions():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('SELECT * FROM Transactions')
    transactions = cursor.fetchall()
    connector.close()
    return transactions

def search_query(lookup_transaction):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute('''SELECT * FROM Transactions WHERE t_type LIKE ? or check_id LIKE ? or note LIKE '%' || ? || '%' or date LIKE ? or amount = ?''', (lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction))
    transactions = cursor.fetchall()
    connector.close()
    return transactions

def search_calc_total_expense(lookup_transaction):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE t_type = 'Expense' and (note LIKE '%' || ? || '%' or check_id LIKE ?  or date LIKE ? or amount = ? or t_type LIKE ?)",(lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction))
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

def search_calc_total_revenue(lookup_transaction):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE t_type = 'Revenue' and (note LIKE '%' || ? || '%' or check_id = ?  or date LIKE ? or amount = ? or t_type LIKE ?)",(lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction,))
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

def search_calc_total(lookup_transaction):
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE note LIKE '%' || ? || '%' or t_type LIKE ? or check_id = ? or date LIKE ? or amount = ?", (lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction, lookup_transaction,))
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

#--------------------------------------------------

def calc_total_expense():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE t_type = 'Expense'")
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

def calc_total_revenue():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE t_type = 'Revenue'")
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

def calc_total():
    connector = sqlite3.connect('ProfitLoss.db')
    cursor = connector.cursor()
    cursor.execute("SELECT SUM(amount) FROM Transactions")
    total_amount = cursor.fetchone()
    connector.commit()
    connector.close()
    return total_amount

def save_as_csv():
    connector = sqlite3.connect("ProfitLoss.db")
    df = pd.read_sql("SELECT * From Transactions", connector)
    df.to_csv("Output.csv", index=False)

createTable()