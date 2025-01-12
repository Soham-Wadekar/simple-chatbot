from config import app, db
from model import ChatHistory


def display_db(app=app, db=db):

    with app.app_context():
        db.create_all()
        print("Displaying chat messages:")
        chats = ChatHistory.query.all()
        for chat in chats:
            print(f"{chat.sender}: {chat.message}")
