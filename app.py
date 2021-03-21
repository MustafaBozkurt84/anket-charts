# app.py


import pandas as pd
import numpy as np

from flask import Flask, jsonify, request, make_response,redirect,url_for,render_template
import jwt
import datetime
from functools import wraps


df=pd.read_csv("AnketSonuclari01_20210303.csv")





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


@app.route("/",methods=['GET', 'POST'])
@token_required
def index():
    token = request.args.get('token')
    url = ".?token=" + token
    sorular = list(df["soru"].unique())
    select_box = request.form.getlist("skills")
    if len(select_box)==0:
        select_box=sorular[0:9]
    my_dict = {"label": [], "AnketeKatılanSayı": [], "CevapYuzdesi": [],"soru":[],"chart":[],"chart_type":[]}
    num=len(select_box)
    for i in range(0,len(select_box)):
         my_dict["label"].append(list(df[df["soru"] == select_box[i]]["cevap"]))
         my_dict["AnketeKatılanSayı"].append( df[df["soru"] == select_box[i]]["countAnswer"].sum())
         my_dict["CevapYuzdesi"].append( [round(i * 100, 2) for i in list(df[df["soru"] == select_box[i]]["percentage"])])
         my_dict["soru"].append(select_box[i])
         my_dict["chart"].append("myChart"+str(i))
         if len(my_dict["label"][i])>4:
             my_dict["chart_type"].append("bar")
         elif len(my_dict["label"][i])>3:
             my_dict["chart_type"].append('horizontalBar')
         elif len(my_dict["label"][i])>2:
             my_dict["chart_type"].append('pie')
         else:
             my_dict["chart_type"].append('doughnut')

    return render_template(
        'dashboard.html',
        sorular=sorular,
        select_box=select_box,
        my_dict=my_dict,
        num=num,
         url=url)

@app.route('/login', methods=["POST","GET"])
def login():
    auth_dict = {"atilla": "yardimci","mustafa":"bozkurtt","analytic":"team"}
    auth = request.authorization
    try:
        if auth and auth.password == auth_dict[auth.username]:
            token = jwt.encode({'user': auth.username,"password": auth.password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)},app.config['SECRET_KEY'])
            my_token = {'token': token.decode('UTF-8')}
            url=".?token="+my_token["token"]
            return redirect(".?token="+my_token["token"])
    except:
        pass


    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
try:
   url=".?token="+my_token["token"]
except:
    pass
if __name__=='__main__':
    app.run(debug=True)