from config import db

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)