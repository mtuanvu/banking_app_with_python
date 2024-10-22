from flask import Flask, request, jsonify, render_template
from config import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/balance/<int:account_id>', methods = ['GET'])
def get_balance(account_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    
    cursor.execute("select balance from accounts where account_id = %s", (account_id,))
    account = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if account:
        return jsonify(account)
    return jsonify({"error":"account not found"}), 404

#API deposti (nap tien)
@app.route('/deposit', methods = ['POST'])
def deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    
    
    cursor.execute("update accounts set balance = balance + %s where account_id = %s", (amount, account_id))
    cursor.execute("insert into transactions (account_id, transaction_type, amount) values(%s, %s, %s)", (account_id, deposit, amount))
    
    #commit xac nhan hoan thanh mot transaction
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message" : "deposit successfully"})

#APi withdraw (rut tien)
@app.route('/withdraw', methods = ['POST'])
def withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    
    cursor.execute("select balance from accounts where account_id  = %s", (account_id))
    account = cursor.fetchone()
    
    if account and account[balance] >= amount:
        new_balance = account['balance'] - amount
        cursor.execute("update accounts set balance = %s where account_id = %s", (new_balance, account_id))
        cursor.execute("insert into transactions(account_id, transaction_type, amount) values (%s, %s, %s)", (account_id, 'withdraw', amount))
    
        conn.commit()
        cursor.close()
        conn.close()
    
        return jsonify({"message": "withdrwal successfully", "new_balance": new_balance})
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)