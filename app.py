from collections import defaultdict
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-super-secret-key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)


class PhotographerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False)
    idPhotographer = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    like = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.JSON, nullable=False)
    authorOfComments = db.Column(db.JSON, nullable=False)


class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    secondName = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


testTwo = defaultdict(list)
testAuthorOfComments = defaultdict(list)

'''
@app.route("/login", methods=["POST"])
def login():
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity="example_user")
    set_access_cookies(response, access_token)
    return response


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
'''


@app.route('/posts', methods=['GET', 'POST'])
@jwt_required()
def getDataFromClient():
    currentUser = get_jwt_identity()
    print(currentUser," <-token|  /posts")
    if currentUser > 10:
        array = []
        if request.method == 'GET':
            model = PhotographerModel.query.order_by(PhotographerModel.date).all()
            for i in model:
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
                article = PhotographerModel(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                                            comments=testTwo, authorOfComments=testAuthorOfComments)
                db.session.add(article)
                db.session.commit()
                print("success")
                return "success"
            except Exception as e:
                return e
    else:
        return jsonify([{
            'idPhotographer': None,
            'author': None,
            'url': None,
            'theme': None,
            'like': None,
            'comments': None,
            'authorOfComments': None
        }])


@app.route('/posts/<int:id>')
@jwt_required()
def visibleByData(id):
    currentUser = get_jwt_identity()
    if currentUser > 10:
        arrayForVisibleData = []
        articles = PhotographerModel.query.order_by(PhotographerModel.date).all()
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
    else:
        return jsonify([{'idPhotographer': None,
                        'author': None,
                        'url': None,
                        'theme': None,
                        'like': None,
                        'comments': None,
                        'authorOfComments': None}])


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
        model = PhotographerModel(idPhotographer=idPhotographer, author=author, url=url, theme=theme, like=like,
                                  comments=testTwo, authorOfComments=testAuthorOfComments)
        db.session.add(model)
        db.session.commit()
        return redirect('posts')
    else:
        return render_template("create-article.html")


@app.route('/register', methods=['POST'])
def register_user():
    try:
        phoneNumber = int(request.form['phoneNumber'])
        name = str(request.form['name'])
        secondName = str(request.form['secondName'])
        password = str(request.form['password'])
        print(phoneNumber,name,secondName,password, "   /register")
        model = AuthModel.query.order_by(AuthModel.date).all()
        for i in model:
            if phoneNumber == int(i.phoneNumber):
                return jsonify([{'accessToken': None, 'refreshToken': None, 'successRegister': False}])
        accessToken = create_access_token(identity=phoneNumber, expires_delta=timedelta(minutes=1), fresh=True)
        refreshToken = create_refresh_token(identity=phoneNumber, expires_delta=timedelta(days=30))
        modelOfRegister = AuthModel(phoneNumber =phoneNumber, name=name, secondName=secondName, password=password)
        db.session.add(modelOfRegister)
        db.session.commit()
        return jsonify([{'accessToken': accessToken, 'refreshToken': refreshToken, 'successRegister': True}])
    except Exception as error:
        print(error)
        return error


#Login
@app.route('/authentication', methods=['POST'])
def login_user():
    try:
        phoneNumber = int(request.form['phoneNumber'])
        password = str(request.form['password'])
        model = AuthModel.query.order_by(AuthModel.date).all()
        print(phoneNumber,password,"   /authentication")
        for i in model:
            if password == str(i.password) and phoneNumber == int(i.phoneNumber):
                print("point 1")
                accessToken = create_access_token(identity=phoneNumber, expires_delta=timedelta(minutes=5), fresh=True)
                refreshToken = create_refresh_token(identity=phoneNumber, expires_delta=timedelta(days=30))
                print("return true")
                return jsonify([{'accessToken': accessToken, 'refreshToken': refreshToken, 'success': True}])
        else:
            print("return false")
            return jsonify([{'accessToken': None, 'refreshToken': None, 'success': False}])
    except Exception as error:
        print(error)
        return "some exeption"

#check if the token is valid
@app.route('/action-with-token', methods=['GET'])
@jwt_required()
def protected():
    currentUser = get_jwt_identity()
    if currentUser > 10:
        return jsonify([{'success': True, 'loggedInAs': currentUser}])
    return jsonify([{'success': None, 'loggedInAs': currentUser}])


@app.route('/token/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    accessToken = create_access_token(identity=identity)
    refreshToken = create_refresh_token(identity=identity)
    print(accessToken,refreshToken)
    return jsonify({'accessToken': accessToken, 'refreshToken': refreshToken,'success': True})


@app.route('/person_data/<int:id>')
@jwt_required()
def get_person_data(id):
    identity = get_jwt_identity()
    if identity > 10:
        try:
            model = AuthModel.query.order_by(AuthModel.date).all()
            arrayOfUserData = []
            for i in model:
                if id == i.phoneNumber:
                    arrayOfUserData.append({
                        'id': str(i.id),
                        'phoneNumber': int(i.phoneNumber),
                        'name': str(i.name),
                        'secondName': str(i.secondName)
                    })
            return jsonify(arrayOfUserData)
        except:
            return "Some exception"
    else:
        return jsonify([{'id': None,'phoneNumber' : None,'name': None,'secondName': None}])

@app.route('/splash')
@jwt_required()
def splash():
    currentUser = get_jwt_identity()
    if currentUser > 10:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



if __name__ == "__main__":
    app.run(debug=True)
