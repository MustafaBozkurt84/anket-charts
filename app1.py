from flask import Flask,jsonify,request,make_response
import jwt
import datetime



app  = Flask(__name__)


@app.route("/")
def protected():
    if request.authorization and request.authorization.username=="username" and request.authorization.password=="password":


    return " You ARE lOGGED IN"



if __name__=="__main__":
    app.run(debug=True)