from collections import defaultdict
import flask_sqlalchemy
from sqlalchemy.dialects.sqlite import BLOB
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    idPhotographer = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    like = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.JSON, nullable=False)
    authorOfComments = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/registration', methods=['GET', 'POST'])
def registrationUser():
    return jsonify("test")


if __name__ == "__main__":
    app.run(debug=True)
