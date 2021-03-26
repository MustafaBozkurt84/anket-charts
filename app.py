# app.py


import pandas as pd
import numpy as np

from flask import Flask, jsonify, request, make_response,redirect,url_for,render_template
import jwt
import datetime
from functools import wraps


df = pd.read_csv("AnketSonuclari01_20210303.csv")
df["soru_"] = [i.replace(" ", "").replace("?", "").replace(":", "").replace(")", "").replace("(", "").replace(".", "").replace(",", "") for i in df["soru"]]

class DataStore():
    sorular = None
    select_box = None
    my_dict = None
    num = None
    anketsayisi = None
    kisisayisi = None
    cevapsecenek = None
    url = None
    token1 = None
    charts_url = None
    chartss = None
    token = None
    token1 = None
    token_create = None
    select_box =None
    link =None
    auth_dict=None
    aunth=None
    my_token=None
    my_chart = None
    label = None
    AnketeKatılanSayı  = None
    CevapYuzdesi  = None
    soru  = None
    chart_type=None
    link_=None
    select_box1=None
    select=None



data = DataStore()



app = Flask(__name__)

app.config['SECRET_KEY'] = 'analyticteam'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data.token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not data.token:
            return redirect(url_for('login'))

        try:
            dataa = jwt.decode(data.token, app.config['SECRET_KEY'])

        except:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated


@app.route("/",methods=['GET', 'POST'])
@token_required
def index():
    data.token1 = request.args.get('token')
    data.url = ".?token=" + data.token1
    data.anketsayisi = df["question"].max()
    data.kisisayisi = df["countAnswer"].sum()
    data.cevapsecenek = df["cevap"].value_counts().sum()
    data.sorular = list(df["soru"].unique())

    data.select_box1 = data.select_box
    try:
        if len(data.select_box) > 0:
            if request.method == "POST":
                data.select_box = request.form.getlist("skills")

    except:
        data.select_box = request.form.getlist("skills")
    if  len(data.select_box) == 0:
        data.select_box=data.select_box1





    try:
        data.num = len(data.select_box)
    except:
        data.select_box = data.sorular[0:9]
        data.num = len(data.select_box)
    data.my_dict = {"label": [], "AnketeKatılanSayı": [], "CevapYuzdesi": [], "soru": [], "chart": [], "chart_type": []}
    for i in range(0,len(data.select_box)):
         data.my_dict["label"].append(list(df[df["soru"] == data.select_box[i]]["cevap"]))
         data.my_dict["AnketeKatılanSayı"].append( df[df["soru"] == data.select_box[i]]["countAnswer"].sum())
         data.my_dict["CevapYuzdesi"].append( [round(i * 100, 2) for i in list(df[df["soru"] == data.select_box[i]]["percentage"])])
         data.my_dict["soru"].append(data.select_box[i])
         data.my_dict["chart"].append("myChart"+str(i))
         if len(data.my_dict["label"][i])>4:
             data.my_dict["chart_type"].append("bar")
         elif len(data.my_dict["label"][i])>3:
             data.my_dict["chart_type"].append('horizontalBar')
         elif len(data.my_dict["label"][i])>2:
             data.my_dict["chart_type"].append('pie')
         else:
             data.my_dict["chart_type"].append('doughnut')


    data.charts_url = "?token=" + data.token1





    data.select=data.select_box

    return render_template(
        'dashboard1.html',
        sorular=data.sorular,
        select_box=data.select_box,
        my_dict=data.my_dict,
        num=data.num,
        anketsayisi=data.anketsayisi,
        kisisayisi=data.kisisayisi,
        cevapsecenek=data.cevapsecenek,
         url=data.url,
         token1=data.token1,
        charts_url=data.charts_url,
        chartss=data.chartss)



@app.route(f"/<chartss>",methods=['GET', 'POST'])
@token_required
def chart(chartss):
    data.select_box1 = data.select_box
    try:
        if len(data.select_box) > 0:
            if request.method == "POST":
                data.select_box = request.form.getlist("skills")

    except:
        data.select_box = request.form.getlist("skills")
    if len(data.select_box) == 0:
        data.select_box = data.select_box1

    try:
        data.num = len(data.select_box)
    except:
        data.select_box = data.sorular[0:9]
        data.num = len(data.select_box)
    data.select_box=data.select
    data.token1 = request.args.get('token')
    data.link_ = df[df["soru_"] == chartss]["soru"].value_counts().index[0]

    link = df[df["soru_"] == chartss]["soru"].value_counts().index
    data.link = link[0]
    data.label = list(df[df["soru"] == data.link]["cevap"])
    data.AnketeKatılanSayı = df[df["soru"] == data.link]["countAnswer"].sum()
    data.CevapYuzdesi = [round(i * 100, 2) for i in list(df[df["soru"] == data.link]["percentage"])]
    data.soru = df[df["soru"] == data.link]["soru"].unique()[0]

    if len(data.label) > 4:
        data.chart_type = "bar"
    elif len(data.label) > 3:
        data.chart_type = 'horizontalBar'
    elif len(data.label) > 2:
        data.chart_type = 'pie'
    else:
        data.chart_type = 'doughnut'


    return render_template("dashboard122.html",
        sorular=data.sorular,
        select_box=data.select_box,
        my_dict=data.my_dict,
        num=data.num,
        anketsayisi=data.anketsayisi,
        kisisayisi=data.kisisayisi,
        cevapsecenek=data.cevapsecenek,
        url=data.url,
        token1=data.token1,
        charts_url=data.charts_url,
        chartss=data.chartss,
        my_chart = data.my_chart,
        label=data.label,
        AnketeKatılanSayı = data.AnketeKatılanSayı,
        CevapYuzdesi = data.CevapYuzdesi,
        soru = data.soru,
        chart_type=data.chart_type,
        link=data.link,
        link_=data.link_,

                           )



@app.route('/login', methods=["POST","GET"])

def login():
    data.auth_dict = {"atilla": "yardimci","mustafa":"bozkurt","analytic":"team"}
    data.auth = request.authorization
    if data.auth and data.auth.password == data.auth_dict[data.auth.username]:
            data.token_create = jwt.encode({'user': data.auth.username,"password": data.auth.password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)},app.config['SECRET_KEY'])
            data.my_token = {'token': data.token_create.decode('utf-8')}

            return redirect(".?token="+data.my_token["token"])



    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


if __name__=='__main__':
    app.run(debug=True)