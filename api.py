from flask import Flask, jsonify, request, make_response,redirect,url_for
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'analyticteam'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return redirect(url_for('login'))

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login', methods=["POST","GET"])
def login():
    auth_dict = {"atilla": "yardimci","mustafa":"bozkurt","analytic":"team"}
    auth = request.authorization

    if auth and auth.password == auth_dict[auth.username]:
        token = jwt.encode({'user': auth.username,"password": auth.password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)},app.config['SECRET_KEY'])
        my_token = {'token': token.decode('UTF-8')}
        return redirect(".?token="+my_token["token"])


    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)