from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key ="supersecretkey"
# Db Connection 
def connect_db():
      return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banking_db")
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('index.html',customers=customers)

@app.route('/create_customer',methods=['GET','POST'])
def create_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        balance = float(request.form['balance'])
        
        conn = connect_db()
        cursor = conn.cursor()
        try:
            query  = "INSERT INTO Customer(name, email, balance) VALUES(%s,%s,%s)"
            cursor.execute(query,(name, email, balance))
            conn.commit()
            flash("Customer created successfully","successs")
            
        except mysql.connector.Error as err: 
            flash (f"Error:{err}", "danger" )
        
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))
    return render_template('create_customer.html')


@app.route('/transactions/<int:customer_id>', methods=['GET', 'POST'])
def transactions(customer_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']
        amount = float(request.form['amount'])
        
        try:
            # Update customer balance based on transaction type
            if transaction_type == 'deposit':
                cursor.execute("UPDATE Customer SET balance = balance + %s WHERE id = %s", (amount, customer_id))
            elif transaction_type == 'withdraw':
                cursor.execute("UPDATE Customer SET balance = balance - %s WHERE id = %s", (amount, customer_id))
            
            # Insert transaction record
            query = "INSERT INTO Transaction(customer_id, transaction_type, amount) VALUES(%s, %s, %s)"
            cursor.execute(query, (customer_id, transaction_type, amount))
            conn.commit()
            flash("Transaction recorded successfully", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    # Fetch transactions for the customer
    cursor.execute("SELECT * FROM Transaction WHERE customer_id = %s", (customer_id,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('transaction.html', transactions=transactions, customer_id=customer_id)

                   
        

# Chạy ứng dụng Flask 
if __name__ =='__main__':
    app.run(debug=True)