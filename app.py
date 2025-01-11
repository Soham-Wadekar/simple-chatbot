from flask import Flask, render_template, url_for, request
from forms import ChatForm
from config import app, db

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)