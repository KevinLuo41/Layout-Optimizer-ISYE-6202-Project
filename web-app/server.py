from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from Model import opt_model,assign_model

app = Flask(__name__)

def str_to_int(s):
  if s == "":
    return None
  else:
    return float(s)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/layout")
def index():

  return render_template("layout_intput.html")


#This doesn't work
@app.route('/layout', methods=['POST'])
def my_form_post():
  # smin
  # print(request.args)
  inputed_data = {}
  savings_min = str_to_int(request.form['smin'])
  num_locations = str_to_int(request.form['numloc'])
  cr = str_to_int(request.form['cr'])
  x_coord = str_to_int(request.form['xcoord'])
  y_coord = str_to_int(request.form['ycoord'])
  h_length = str_to_int(request.form['Hlength'])
  v_length = str_to_int(request.form['Vlength'])
  # inputed_data = {"s":savings_min,}
  print(request.form)

  opt_model.run_opt_model(savings_min,cr,num_locations)

  sku_mapping = assign_model.run_assgin_model(c=(x_coord,y_coord),h=h_length,v=v_length)

  return render_template("skuVisualization.html", sku_mapping = sku_mapping)



if __name__ == "__main__":
  app.run()