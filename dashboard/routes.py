from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from .forms import TransactionForm
from . import main
from models import Transaction, db

@main.route("/dashboard")
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()

    total_income = sum(transaction.amount for transaction in transactions if transaction.type == "income")
    total_expense = sum(transaction.amount for transaction in transactions if transaction.type == "expense")
    balance = total_income - total_expense

    recent_transactions = transactions[:5]  # Get the 5 most recent transactions

    return render_template(
        "dashboard/dashboard.html",
        balance = balance,
        total_income=total_income, 
        total_expense=total_expense, 
        recent_transactions=recent_transactions
    )

@main.route("/add-transaction", methods=["GET", "POST"])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            title = form.title.data,
            amount = form.amount.data,
            type = form.type.data,
            category = form.category.data,
            description = form.description.data,
            user_id = current_user.id
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash("Transaction added successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("dashboard/add_transaction.html", form=form)



@main.route("/transactions")
@login_required
def all_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template("dashboard/transactions.html", transactions=transactions)


@main.route("/delete_transaction/<int:transaction_id>", methods=["POST"])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(transaction)
    db.session.commit()

    flash("Transaction deleted successfully.", "success")
    return redirect(url_for("main.all_transactions"))