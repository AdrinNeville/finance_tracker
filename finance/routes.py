from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Transaction
from .forms import RegistrationForm, LoginForm, TransactionForm
from datetime import datetime
import csv
import io

bp = Blueprint('finance', __name__, template_folder='templates')



# Authentication routes
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


# Dashboard
@bp.route('/')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    total_income = sum(t.amount for t in transactions if t.type == 'Income')
    total_expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = total_income - total_expense

    # prepare data for chart: expenses by category
    expenses = [t for t in transactions if t.type == 'Expense']
    cat_map = {}
    for e in expenses:
        cat_map[e.category] = cat_map.get(e.category, 0) + e.amount
    categories = list(cat_map.keys())
    amounts = [cat_map[c] for c in categories]

    return render_template('dashboard.html', transactions=transactions,
                           balance=balance, total_income=total_income,
                           total_expense=total_expense, categories=categories,
                           amounts=amounts)


# Add transaction
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        t = Transaction(amount=form.amount.data,
                        category=form.category.data,
                        type=form.type.data,
                        date=form.date.data,
                        description=form.description.data,
                        user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
        flash('Transaction added.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_transaction.html', form=form)


# Edit transaction
@bp.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(tx_id):
    t = Transaction.query.get_or_404(tx_id)
    if t.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('main.dashboard'))
    form = TransactionForm(obj=t)
    if form.validate_on_submit():
        t.amount = form.amount.data
        t.category = form.category.data
        t.type = form.type.data
        t.date = form.date.data
        t.description = form.description.data
        db.session.commit()
        flash('Transaction updated.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('edit_transaction.html', form=form, transaction=t)


# Delete transaction
@bp.route('/delete/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    t = Transaction.query.get_or_404(tx_id)
    if t.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('main.dashboard'))
    db.session.delete(t)
    db.session.commit()
    flash('Transaction deleted.', 'info')
    return redirect(url_for('main.dashboard'))


# Export CSV
@bp.route('/export')
@login_required
def export_csv():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'date', 'type', 'category', 'amount', 'description'])
    for t in transactions:
        cw.writerow([t.id, t.date.isoformat(), t.type, t.category, t.amount, t.description or ''])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name='transactions.csv', as_attachment=True)
    # Register blueprint static and templates by reference — Flask auto-locates templates in templates/ folder in project