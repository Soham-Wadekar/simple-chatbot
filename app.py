from flask import render_template, url_for, redirect
from forms import ChatForm
from model import ChatHistory
from config import app, db

from transformers import pipeline
import warnings

# import getpass
# import os

# if not os.environ.get("OPENAI_API_KEY"):
#   os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# from langchain_openai import ChatOpenAI

# model = ChatOpenAI(model="gpt-4o-mini")

def warn(*args, **kwargs):
    pass
warnings.warn = warn
generator = pipeline("text-generation", model="gpt2")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ChatForm()
    chat_history = ChatHistory.query.all()

    if form.validate_on_submit():
        user_input = form.message.data

        user_message = ChatHistory(sender="user", message=user_input)
        db.session.add(user_message)

        bot_response = generator(user_input)[0]["generated_text"]
        # bot_response = model.invoke(user_input)
        bot_message = ChatHistory(sender="bot", message=bot_response)
        db.session.add(bot_message)

        db.session.commit()

        form.message.data = ""

        return redirect(url_for("home"))

    return render_template("home.html", form=form, chat_history=chat_history)


@app.route("/clear", methods=["POST"])
def clear_chat_history():
    try:

        ChatHistory.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
