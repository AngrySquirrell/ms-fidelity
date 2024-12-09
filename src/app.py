import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données et des migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modèle d'articles
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)            # ID
    email = db.Column(db.String(120), nullable=False)       # Email
    name = db.Column(db.String(120), nullable=False)        # Name
    ticketIDs = db.Column(db.PickleType, nullable=False)    # TicketIDs
    fPoints = db.Column(db.Integer, nullable=False)         # Fidelity Points
    cardID = db.Column(db.String(120), nullable=False)      # CardID
    
    # Création de 5 utilisateurs fictifs
with app.app_context():
    db.create_all()
    if not Account.query.first():
        fake_users = [
            Account(email='user1@example.com', name='User One', ticketIDs=[], fPoints=100, cardID=str(uuid.uuid4())),
            Account(email='user2@example.com', name='User Two', ticketIDs=[], fPoints=100, cardID=str(uuid.uuid4())),
            Account(email='user3@example.com', name='User Three', ticketIDs=[], fPoints=100, cardID=str(uuid.uuid4())),
            Account(email='user4@example.com', name='User Four', ticketIDs=[], fPoints=100, cardID=str(uuid.uuid4())),
            Account(email='user5@example.com', name='User Five', ticketIDs=[], fPoints=100, cardID=str(uuid.uuid4()))
        ]
        db.session.bulk_save_objects(fake_users)
        db.session.commit()


@app.route('/accounts', methods=['GET'])
def get_accounts_data():
    accounts = Account.query.all()
    accounts_list = [{"id": account.id, "email": account.email, "name": account.name, "fPoints": account.fPoints, "cardID": account.cardID} for account in accounts]
    return jsonify(accounts_list)

@app.route('/account', methods=['GET'])
def get_account_data():
    id = request.args.get('id')
    account = Account.query.get(id)
    return jsonify({"id": account.id, "email": account.email, "name": account.name, "fPoints": account.fPoints, "cardID": account.cardID})

@app.route('/purchase', methods=['POST'])
def register_purchase():
    purchase_data = request.json
    id = purchase_data['id']
    account = Account.query.get(id)
    account.fPoints += purchase_data['fPoints']
    db.session.commit()
    return jsonify({"id": account.id, "email": account.email, "name": account.name}), 201

@app.route('/register', methods=['POST'])
def register_account():
    print(request.json)
    account_data = request.json
    account = Account(email=account_data['email'], name=account_data['name'], fPoints=100, cardID=str(uuid.uuid4()))
    db.session.add(account)
    db.session.commit()
    return jsonify({"id": account.id, "email": account.email, "name": account.name, "fPoints": account.fPoints, "cardID": account.cardID}), 201

@app.route('/use_points', methods=['GET'])
def use_points():
    id = request.args.get('id')
    amount = request.args.get('amount')
    account = Account.query.get(id)
    if account.fPoints < amount:
        return jsonify({"error": "Not enough fidelity points"}), 400
    account.fPoints -= amount
    db.session.commit()
    return jsonify({"id": account.id, "email": account.email, "name": account.name, "fPoints": account.fPoints, "cardID": account.cardID, "reductionDelivered": True}), 201




# Exécution de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)