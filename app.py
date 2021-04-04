# app.py


import pandas as pd
import numpy as np

from flask import Flask, jsonify, request, make_response,redirect,url_for,render_template
import jwt
import datetime
from functools import wraps


df = pd.read_csv("AnketSonuclari01_20210401.csv")
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
    select = None
    df_answers = None
    df_question = None
    df_filtered = None
    question1=None
    question2=None
    my_dict={}




data = DataStore()



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
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

    data.select_box = data.select

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

    data.select_box = data.select
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
        link_=data.link_


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

@app.route("/detail_chart.",methods=['GET', 'POST'])
@token_required
def filtered_chart():
    data.token1 = request.args.get('token')
    data.url = "?token=" + data.token1
    df_question = pd.read_excel("DataStudy02mail.xlsx", sheet_name="questions")
    df_answers = pd.read_excel("DataStudy02mail.xlsx", sheet_name="Sheet4")
    data.my_dict["question_title"] = df_question["title"].tolist()
    data.question1 = request.form.get("one")
    data.question2 = request.form.get("ones")
    if (data.question1 == None):
        data.question1 = 'Ailenin aylık ortalama geliri nedir?'
        data.question2 = 'Pahalı ama çok beğendiğin bir ürün almak istediğinde hangi durum seni en iyi yansıtıyor?'

    selected_question1 = df_question[df_question["title"] == data.question1]["question_id"].tolist()[0]
    selected_question2 = df_question[df_question["title"] == data.question2]["question_id"].tolist()[0]
    filter1 = [i for i in df_answers.columns[2:] if (int(i.split("_")[1]) == selected_question1)]
    filter2 = [i for i in df_answers.columns[2:] if (int(i.split("_")[1]) == selected_question2)]
    filter3 = [i for i in df_answers.columns[2:] if (int(i.split("_")[1]) == selected_question1)]
    filter3.extend(filter2)
    df_filtered = df_answers.loc[:, filter3]
    df_groupby1 = df_filtered.groupby(filter1)[filter2].sum()
    df_groupb2 = df_groupby1.reset_index()
    df_groupb2["index"] = df_groupb2.index
    for i in filter1:
        for value in range(0, len(df_groupb2[i])):
            if df_groupb2[i][value] == 1.0:
                df_groupb2["index"][value] = i

    df_groupby1.index = df_groupb2["index"]
    df_groupby1.columns = [i.split("_")[2] for i in df_groupby1.columns]
    df_groupby1.index = [i.split("_")[2] for i in df_groupby1.index]
    df_groupb2["index"] = df_groupby1.index
    data.my_dict["df_groupby1_column"]=df_groupby1.columns
    data.my_dict["df_groupby1_index"] = list(df_groupby1.index)
    data.my_dict["question1"]=data.question1
    data.my_dict["question2"] = data.question2
    for i in df_groupby1.columns:
        data.my_dict[i]=list(df_groupby1[i])
    default_color_list = ['rgba(255, 99, 132, 0.4)',
                          'rgba(54, 162, 235, 0.4)',
                          'rgba(255, 206, 86, 0.4)',
                          'rgba(75, 192, 192, 0.4)',
                          'rgba(153, 102, 255, 0.4)',
                          'rgba(255, 159, 64, 0.4)',
                          "rgba(211, 36, 167, 0.4)",
                          "rgba(183, 2, 63, 0.4)",
                          " rgba(51, 171, 87, 0.4)",
                          "rgba(100, 160, 168, 0.4)",
                          "rgba(16, 150, 166, 0.4)",
                          "rgba(183, 100, 83, 4)",
                          "rgba(193, 18, 35, 4)",
                          "rgba(81, 24, 172, 0.4)",
                          "rgba(212, 122, 166, 0.4)"]
    default_color_list1 = ['rgba(255, 99, 132, 1)',
                          'rgba(54, 162, 235, 1)',
                          'rgba(255, 206, 86, 1)',
                          'rgba(75, 192, 192, 1)',
                          'rgba(153, 102, 255, 1)',
                          'rgba(255, 159, 64, 1)',
                          "rgba(211, 36, 167, 1)",
                          "rgba(183, 2, 63, 1)",
                          " rgba(51, 171, 87, 1)",
                          "rgba(100, 160, 168, 1)",
                          "rgba(16, 150, 166, 1)",
                          "rgba(183, 100, 83, 1)",
                          "rgba(193, 18, 35, 1)",
                          "rgba(81, 24, 172, 1)",
                          "rgba(212, 122, 166, 1)"]
    total_person = df_filtered.dropna().shape[0]
    data_color_dict = {}
    data_color_dict["col_name"]=df_groupby1.columns
    data_color_dict["df_groupby1_index"] = list(df_groupby1.index)
    data_color_dict["col_lenn"] = len(df_groupby1.columns)

    data_color_dict["color"] = default_color_list[0:data_color_dict["col_lenn"]]
    data_color_dict["color1"] = default_color_list1[0:data_color_dict["col_lenn"]]
    data_color_dict["column"]=[]
    for i in range(len(df_groupby1.columns)):
        data_color_dict["column"].append([round((i/total_person)*100,2) for i in list(df_groupby1.iloc[:,i])])
    my_cross_charts1 = {}
    my_cross_charts2 = {}
    count_first_chart = df_filtered[filter1].dropna().count()[0]
    count_second_chart = df_filtered[filter2].dropna().count()[0]
    df_filtered1 = df_filtered[filter1].dropna()
    df_filtered2 = df_filtered[filter2].dropna()
    for i in df_filtered1.columns:
        df_filtered1[i] = df_filtered1[i].sum()
    df_filtered1 = df_filtered1.reset_index(drop=True).iloc[0:1, :]
    for i in df_filtered2.columns:
        df_filtered2[i] = df_filtered2[i].sum()
    df_filtered2 = df_filtered2.reset_index(drop=True).iloc[0:1, :]
    df_filtered2.columns = [(i.split("_")[2]) for i in df_filtered2.columns]
    df_filtered1.columns = [(i.split("_")[2]) for i in df_filtered1.columns]
    my_cross_charts1["data1"] = []
    for i in range(len(df_filtered1.columns)):
        my_cross_charts1["data1"].append([round((i / count_first_chart) * 100, 2) for i in df_filtered1.iloc[:, i]])
        my_cross_charts2["data2"] = []
    for i in range(len(df_filtered2.columns)):
        my_cross_charts2["data2"].append([round((i / count_second_chart) * 100, 2) for i in df_filtered2.iloc[:, i]])
    my_cross_charts1["columns1"]=df_filtered1.columns
    my_cross_charts1["num1"]=len(df_filtered1.columns)
    my_cross_charts2["columns1"] = df_filtered2.columns
    my_cross_charts2["num1"] = len(df_filtered2.columns)
    my_cross_charts1["count_first_chart"]=count_first_chart
    my_cross_charts2["count_second_chart"] = count_second_chart

    my_cross_charts3={}
    df_groupbytable = df_groupby1.reset_index()
    my_cross_charts2["tablecolumns"]=df_groupbytable.columns
    my_cross_charts2["tableindexlen"]=df_groupby1.shape[0]
    my_table_list = []
    for i in range(df_groupbytable.shape[0]):
        for col in df_groupbytable.columns:
            my_table_list.append(df_groupbytable[col][i])
    my_table_list_len=len(my_table_list)
    for i in df_groupbytable.columns:
        my_cross_charts3[i]=df_groupbytable[i].tolist()

    return render_template("dashboard123.html",my_dict=data.my_dict,my_cross_charts3=my_cross_charts3,url=data.url,my_table_list_len=my_table_list_len,df_groupby1=df_groupby1,data_color_dict=data_color_dict,my_cross_charts2=my_cross_charts2,my_cross_charts1=my_cross_charts1,my_table_list=my_table_list)


if __name__=='__main__':
    app.run(debug=True)