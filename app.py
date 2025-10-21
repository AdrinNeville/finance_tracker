# from flask import Flask, render_template_string, request, jsonify, redirect, url_for
# from datetime import datetime
# import json
# import os

# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'

# # Data storage file
# DATA_FILE = 'finance_data.json'

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Data storage file
DATA_FILE = 'finance_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'transactions': [], 'budgets': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finance Tracker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .stat-card {
            text-align: center;
        }
        
        .stat-card h3 {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .stat-card .amount {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-card.income .amount {
            color: #10b981;
        }
        
        .stat-card.expense .amount {
            color: #ef4444;
        }
        
        .stat-card.balance .amount {
            color: #667eea;
        }
        
        .form-section {
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .transactions-list {
            margin-top: 20px;
        }
        
        .transaction-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
            transition: background-color 0.2s;
        }
        
        .transaction-item:hover {
            background-color: #f9fafb;
        }
        
        .transaction-info {
            flex: 1;
        }
        
        .transaction-category {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .category-food { background-color: #fef3c7; color: #92400e; }
        .category-transport { background-color: #dbeafe; color: #1e40af; }
        .category-shopping { background-color: #fce7f3; color: #9f1239; }
        .category-bills { background-color: #fee2e2; color: #991b1b; }
        .category-entertainment { background-color: #e0e7ff; color: #3730a3; }
        .category-salary { background-color: #d1fae5; color: #065f46; }
        .category-other { background-color: #f3f4f6; color: #374151; }
        
        .transaction-description {
            color: #666;
            font-size: 0.9em;
        }
        
        .transaction-date {
            color: #999;
            font-size: 0.85em;
        }
        
        .transaction-amount {
            font-size: 1.2em;
            font-weight: bold;
            margin-left: 20px;
        }
        
        .transaction-amount.income {
            color: #10b981;
        }
        
        .transaction-amount.expense {
            color: #ef4444;
        }
        
        .delete-btn {
            background: #ef4444;
            padding: 8px 15px;
            font-size: 0.9em;
            margin-left: 10px;
        }
        
        .delete-btn:hover {
            background: #dc2626;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 24px;
            background: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Finance Tracker</h1>
            <p>Manage your income and expenses</p>
        </div>
        
        <div class="dashboard">
            <div class="card stat-card income">
                <h3>Total Income</h3>
                <div class="amount">₹{{ "%.2f"|format(total_income) }}</div>
            </div>
            <div class="card stat-card expense">
                <h3>Total Expenses</h3>
                <div class="amount">₹{{ "%.2f"|format(total_expense) }}</div>
            </div>
            <div class="card stat-card balance">
                <h3>Balance</h3>
                <div class="amount">₹{{ "%.2f"|format(balance) }}</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('add-transaction')">Add Transaction</button>
            <button class="tab" onclick="showTab('view-transactions')">View Transactions</button>
        </div>
        
        <div id="add-transaction" class="tab-content active">
            <div class="card">
                <h2 style="margin-bottom: 20px;">Add New Transaction</h2>
                <form method="POST" action="/add_transaction">
                    <div class="form-group">
                        <label>Type</label>
                        <select name="type" required>
                            <option value="expense">Expense</option>
                            <option value="income">Income</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Category</label>
                        <select name="category" required>
                            <option value="food">Food</option>
                            <option value="transport">Transport</option>
                            <option value="shopping">Shopping</option>
                            <option value="bills">Bills</option>
                            <option value="entertainment">Entertainment</option>
                            <option value="salary">Salary</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Amount (₹)</label>
                        <input type="number" name="amount" step="0.01" required>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" name="description" required>
                    </div>
                    <div class="form-group">
                        <label>Date</label>
                        <input type="date" name="date" required value="{{ today }}">
                    </div>
                    <button type="submit">Add Transaction</button>
                </form>
            </div>
        </div>
        
        <div id="view-transactions" class="tab-content">
            <div class="card">
                <h2 style="margin-bottom: 20px;">Transaction History</h2>
                {% if transactions %}
                <div class="transactions-list">
                    {% for transaction in transactions|reverse %}
                    <div class="transaction-item">
                        <div class="transaction-info">
                            <span class="transaction-category category-{{ transaction.category }}">
                                {{ transaction.category|upper }}
                            </span>
                            <div class="transaction-description">{{ transaction.description }}</div>
                            <div class="transaction-date">{{ transaction.date }}</div>
                        </div>
                        <div style="display: flex; align-items: center;">
                            <div class="transaction-amount {{ transaction.type }}">
                                {{ '+' if transaction.type == 'income' else '-' }}₹{{ "%.2f"|format(transaction.amount) }}
                            </div>
                            <form method="POST" action="/delete_transaction/{{ loop.index0 }}" style="display: inline;">
                                <button type="submit" class="delete-btn" onclick="return confirm('Delete this transaction?')">Delete</button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="empty-state">
                    <p>No transactions yet. Add your first transaction!</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabId) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    data = load_data()
    transactions = data.get('transactions', [])
    
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense
    
    return render_template_string(
        HTML_TEMPLATE,
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        today=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = load_data()
    
    transaction = {
        'type': request.form['type'],
        'category': request.form['category'],
        'amount': float(request.form['amount']),
        'description': request.form['description'],
        'date': request.form['date'],
        'timestamp': datetime.now().isoformat()
    }
    
    data['transactions'].append(transaction)
    save_data(data)
    
    return redirect(url_for('index'))

@app.route('/delete_transaction/<int:index>', methods=['POST'])
def delete_transaction(index):
    data = load_data()
    
    if 0 <= index < len(data['transactions']):
        data['transactions'].pop(index)
        save_data(data)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)