from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import pandas as pd
import ast
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap


# Init app
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
Bootstrap(app)

upload_historical_transactions = {
  "counterparty limits": [],
  "recurring transactions": [],
  "recurring value": [],
  "window limit": [],
  "transaction group id": ()
}

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"TransactionMonitor(date = {date}, description = {description}, amount = {amount})"


transaction_put_args = reqparse.RequestParser()
transaction_put_args.add_argument("id", type=int, help="ID of the transaction is required", required=True)
transaction_put_args.add_argument("date", type=str, help="Date of the transaction is required", required=True)
transaction_put_args.add_argument("description", type=str, help="Description of the transaction", required=True)
transaction_put_args.add_argument("amount", type=float, help="Amount on the transaction", required=True)

transaction_update_args = reqparse.RequestParser()
transaction_update_args.add_argument("int", type=int, help="ID of the transaction is required")
transaction_update_args.add_argument("date", type=str, help="Date of the transaction is required")
transaction_update_args.add_argument("description", type=str, help="Description of the transaction")
transaction_update_args.add_argument("amount", type=float, help="Amount on the transaction")

resource_fields = {
    'id': fields.Integer,
    'date': fields.String,
    'description': fields.String,
    'amount': fields.Float
}


@app.route("/Base")
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/<name>")
def user(name):
    return f"hello {name}!"
 
@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

class TransactionMonitor(Resource):
    @marshal_with(resource_fields)
    def get(self, transaction_id):
        result = TransactionMonitor.query.filter_by(id=transaction_id).first()
        if not result:
            abort(404, message="Could not find transaction with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, transaction_id):
        args = transaction_put_args.parse_args()
        result = TransactionMonitor.query.filter_by(id=transaction_id).first()
        if result:
            abort(409, message="transaction id taken...")

        upload_historical_transactions = TransactionMonitor(id=transaction_id, date=args['date'], description=args['description'], amount=args['amount'])
        db.session.add(upload_historical_transactions)
        db.session.commit()
        return upload_historical_transactions, 201

    @marshal_with(resource_fields)
    def post(self, transaction_id):
        args = transaction_update_args.parse_args()
        result = TransactionMonitor.query.filter_by(id=transaction_id).first()
        if not result:
            abort(404, message="transaction doesn't exist, cannot update")

        if args['date']:
            result.date = args['date']
        if args['description']:
            result.description = args['description']
        if args['amount']:
            result.amount = args['amount']

        db.session.commit()

        return result


    def delete(self, transaction_id):
        abort_if_transaction_id_doesnt_exist(transaction_id)
        del transactions[transaction_id]
        return '', 204

    def recurrentTransactions(amount_tolerance: float=0.01, period_tolerance: int=6, n_days: int=30, client_col:str=None, time_col: str=None, amount_col: str=None, config: dict=None):
        
        if config is not None:
              id = config.account_id
              date = config.trans_date
              amount = config.trans_amount
        
    def rb(trans_data: pd.DataFrame):
        return
    
    
    
    


api.add_resource(Transactions, "/upload_historical_transactions/<string:transaction_id>")



# Run Server
if __name__ == "__main__":
    app.run(debug=True)