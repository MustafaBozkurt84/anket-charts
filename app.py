# app.py


import pandas as pd
import numpy as np
from flask import Flask, flash, redirect, render_template, \
     request, url_for



df=pd.read_csv("AnketSonuclari01_20210303.csv")
sorular=list(df["soru"].unique())






app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():

    select_box = request.form.getlist("skills")
    if len(select_box[0])==0:
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
    num=num)



if __name__=='__main__':
    app.run(debug=True)