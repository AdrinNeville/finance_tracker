# finance/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Transaction
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_income = sum(t.amount for t in transactions if t.type == 'Income')
    total_expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = total_income - total_expense
    return render_template('dashboard.html', transactions=transactions, balance=balance)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        type = request.form['type']
        description = request.form['description']
        new_t = Transaction(amount=amount, category=category, type=type,
                            description=description, user_id=current_user.id)
        db.session.add(new_t)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_transaction.html')