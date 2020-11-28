from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
  sku_mapping = pd.read_csv("data/sku_mock.csv").to_numpy()
  return render_template("index.html", sku_mapping = sku_mapping)


#This doesn't work
# @app.route('/', methods=['POST'])
# def my_form_post():
#   inputed_data = {}
#   savings_min = request.form['smin']
#   num_locations = request.form['numloc']
#   x_coord = request.form['xcoord']
#   y_coord = request.form['ycoord']
#   h_length = request.form['Hlength']
#   v_length = request.form['Vlength']
#   print(savings_min)
#   return
    

if __name__ == "__main__":
  app.run()