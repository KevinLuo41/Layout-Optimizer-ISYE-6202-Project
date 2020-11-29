from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for
from Simulator.simulator import Simulator
from Model import opt_model,assign_model

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

  return render_template("layout_input.html")


#This doesn't work
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

  opt_model.run_opt_model(savings_min,cr,num_locations)

  sku_mapping = assign_model.run_assgin_model(c=(x_coord,y_coord),h=h_length,v=v_length)

  return render_template("skuVisualization.html", sku_mapping = sku_mapping)

@app.route("/forecast-in")
def forecast_in():
  return render_template("forecast_input.html")

@app.route('/forecast-out', methods=['POST'])
def forecast_out():

  Artikelno = int(str_to_num(request.form['Artikelno']))
  hist_periods = str_to_num(request.form['hist_periods'])
  freq = request.form['freq']
  fore_periods = int(str_to_num(request.form['fore_periods']))

  print(Artikelno, hist_periods, freq, fore_periods)

  fig_name,_,_ = Simulator(artikelno=Artikelno, hist_periods=hist_periods, freq=freq, fore_periods=fore_periods)

  out_path = "../static/imgs/forecast_ouput/"+fig_name
  print(out_path)
  return render_template("forecast_result.html", img_path = out_path)

@app.route("/about")
def about():
  return render_template("About.html")

if __name__ == "__main__":
  app.run(debug=True)