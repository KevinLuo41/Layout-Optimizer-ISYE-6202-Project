from datetime import timedelta
import os
from flask import Flask, render_template, request, Response
from Simulator.simulator import Simulator
from Model import opt_model, assign_model
from ABC_Analysis.ABC import *

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)


def str_to_num(s):
    if s == "":
        return None
    elif "." in s:
        return float(s)
    else:
        return int(s)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/layout-in")
def layout_in():
    return render_template("layout_in.html")


# This doesn't work
@app.route('/layout', methods=['POST'])
def my_form_post():
    # smin
    # print(request.args)
    inputed_data = {}
    savings_min = str_to_num(request.form['smin'])
    num_locations = str_to_num(request.form['numloc'])
    cr = str_to_num(request.form['cr'])
    x_coord = str_to_num(request.form['xcoord'])
    y_coord = str_to_num(request.form['ycoord'])
    h_length = str_to_num(request.form['Hlength'])
    v_length = str_to_num(request.form['Vlength'])
    # inputed_data = {"s":savings_min,}
    # print(request.form)

    opt_model.run_opt_model(savings_min, cr, num_locations)

    sku_mapping = assign_model.run_assgin_model(c=(x_coord, y_coord), h=h_length, v=v_length)

    return render_template("layout_out.html", sku_mapping=sku_mapping)


@app.route("/forecast-in")
def forecast_in():
    return render_template("forecast_in.html")


@app.route('/forecast-out', methods=['POST'])
def forecast_out():
    global name
    Artikelno = int(str_to_num(request.form['Artikelno']))
    hist_periods = str_to_num(request.form['hist_periods'])
    freq = request.form['freq']
    fore_periods = int(str_to_num(request.form['fore_periods']))

    # print(Artikelno, hist_periods, freq, fore_periods)

    name, _, forecast = Simulator(artikelno=Artikelno, hist_periods=hist_periods, freq=freq, fore_periods=fore_periods)

    out_path = "../static/imgs/forecast_output/" + name + ".png"
    print(os.path.abspath(__file__))
    forecast.to_csv("../output/forecast_output/"+name+".csv",index=False)

    return render_template("forecast_out.html", img_path=out_path)

@app.route('/forecast-down', methods=['POST'])
def forecast_down():
    global name
    with open("../output/forecast_output/"+name+".csv") as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename="+name+".csv"})

@app.route("/about")
def about():
    return render_template("Contact.html")


@app.route("/abc_in")
def abc_in():
    return render_template("ABC_in.html")


@app.route("/abc_out", methods=['POST'])
def abc_out():
    method = request.form['methods']
    time = str_to_num(request.form['time'])
    valueA = str_to_num(request.form['valueA'])
    valueB = str_to_num(request.form['valueB'])
    valueC = str_to_num(request.form['valueC'])
    print(request.form)

    if method == "value":
        All, A, B, C = ABC(method, time, value=(valueA, valueB, valueC))
    else:
        All, A, B, C = ABC(method, time, ratio=(valueA, valueB, valueC))

    HistBox(All,"All")
    HistBox(A, "A")
    HistBox(B, "B")
    HistBox(C, "C")
    out_path = "../static/imgs/ABC_output/"

    Pie(A,B,C)

    return render_template("ABC_out.html",img_path = out_path, method = method,ratio = (A,B,C))


if __name__ == "__main__":
    app.run(debug=True)
