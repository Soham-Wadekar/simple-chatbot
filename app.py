from flask import Flask, render_template, url_for, request, redirect
from forms import ChatForm
from model import ChatHistory
from config import app, db

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ChatForm()
    chat_history = ChatHistory.query.all()

    if form.validate_on_submit():
        user_input = form.message.data

        user_message = ChatHistory(sender='user', message=user_input)
        db.session.add(user_message)

        bot_response = f"Responding to: {user_input}"
        bot_message = ChatHistory(sender='bot', message=bot_response)
        db.session.add(bot_message)

        db.session.commit()

        form.message.data = ''

        return redirect(url_for('home'))

    return render_template('home.html', form=form, chat_history=chat_history, message='')

@app.route("/clear", methods=['POST'])
def clear_chat_history():
    try:

        ChatHistory.query.delete()
        db.session.commit()
        message = "Chat History cleared successfully!"
    except Exception as e:
        db.session.rollback()
        message = f"Error deleting chat history: {e}"

    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)