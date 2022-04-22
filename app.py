from collections import defaultdict
import flask_sqlalchemy
from sqlalchemy.dialects.sqlite import BLOB
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
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




testTwo = defaultdict(list)
testAuthorOfComments = defaultdict(list)


@app.route('/posts', methods=['GET', 'POST'])
def getDataFromCLient():
    array = []

    if request.method == 'GET':
        articles = Article.query.order_by(Article.date).all()
        for i in articles:
            array.append(
                {
                    'idPhotographer': int(i.idPhotographer),
                    'author': str(i.author),
                    'url': str(i.url),
                    'theme': str(i.theme),
                    'like': int(i.like),
                    'comments': i.comments[f'{i.idPhotographer}'],
                    'authorOfComments': i.authorOfComments[f'{i.idPhotographer}']
                }
            )
        try:
            for i in range(len(array) - 1):
                x = array[i]
                for j in range(i + 1, len(array)):
                    y = array[j]
                    if not x or not y:
                        continue
                    if x['idPhotographer'] == y['idPhotographer']:
                        a = x['like'] + y['like']

                        arrayOfCommentsOne = x['comments']
                        arrayOfCommentsTwo = y['comments']

                        arrayOfAuthorOfCommentsOne = x['authorOfComments']
                        arrayOfAuthorOfCommentsTwo = y['authorOfComments']

                        if len(arrayOfAuthorOfCommentsTwo) > len(arrayOfAuthorOfCommentsOne):
                            x['authorOfComments'] = arrayOfAuthorOfCommentsTwo
                        if len(arrayOfCommentsTwo) > len(arrayOfCommentsOne):
                            x['comments'] = arrayOfCommentsTwo
                        if a > 0 or a == 0:
                            x['like'] = a
                        else:
                            print("лайков слишком мало")
                        y.clear()
            array = [x for x in array if x]
        except Exception as error:
            print(error)
        return jsonify(array)
    if request.method == 'POST':
        print("post")
        try:
            idPhotographer = int(request.form['idPhotographer'])
            author = str(request.form['author'])
            url = str(request.form['url'])
            theme = str(request.form['theme'])
            like = int(request.form['like'])
            comments = request.form['comments']
            authorOfComments = request.form['authorOfComments']
            testTwo[idPhotographer].append(comments)
            testAuthorOfComments[idPhotographer].append(authorOfComments)
            article = Article(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                              comments=testTwo, authorOfComments=testAuthorOfComments)
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            return e


@app.route('/posts/<int:id>')
def visibleData(id):
    arrayForVisibleData = []
    articles = Article.query.order_by(Article.date).all()
    for i in articles:
        if id == i.idPhotographer:
            arrayForVisibleData.append(
                {
                    'idPhotographer': int(i.idPhotographer),
                    'author': str(i.author),
                    'url': str(i.url),
                    'theme': str(i.theme),
                    'like': int(i.like),
                    'comments': i.comments[f'{i.idPhotographer}'],
                    'authorOfComments': i.authorOfComments[f'{i.idPhotographer}']
                }
            )
    try:
        for i in range(len(arrayForVisibleData) - 1):
            x = arrayForVisibleData[i]
            for j in range(i + 1, len(arrayForVisibleData)):
                y = arrayForVisibleData[j]
                if not x or not y:
                    continue
                if x['idPhotographer'] == y['idPhotographer']:
                    a = x['like'] + y['like']

                    arrayOfCommentsOne = x['comments']
                    arrayOfCommentsTwo = y['comments']

                    arrayOfAuthorOfCommentsOne = x['authorOfComments']
                    arrayOfAuthorOfCommentsTwo = y['authorOfComments']

                    if len(arrayOfAuthorOfCommentsTwo) > len(arrayOfAuthorOfCommentsOne):
                        x['authorOfComments'] = arrayOfAuthorOfCommentsTwo
                    if len(arrayOfCommentsTwo) > len(arrayOfCommentsOne):
                        x['comments'] = arrayOfCommentsTwo
                    if a > 0 or a == 0:
                        x['like'] = a
                    else:
                        print("лайков слишком мало")
                    y.clear()
        arrayForVisibleData = [x for x in arrayForVisibleData if x]
    except Exception as error:
        print(error)
    return jsonify(arrayForVisibleData)


@app.route('/', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":

        idPhotographer = int(request.form['idPhotographer'])
        author = str(request.form['author'])
        url = str(request.form['url'])
        theme = str(request.form['theme'])
        like = int(request.form['like'])
        comments = request.form['comments']
        authorOfComments = request.form['authorOfComments']
        testTwo[idPhotographer].append(comments)
        testAuthorOfComments[idPhotographer].append(authorOfComments)
        article = Article(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                          comments=testTwo, authorOfComments=testAuthorOfComments)
        db.session.add(article)
        db.session.commit()
        return redirect('posts')
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)
