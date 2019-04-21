import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename  
import pandas as pd       
import numpy as np

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/upload")
def upload_file():
   return render_template("upload.html")


@app.route("/results", methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))

      df = pd.read_csv(f.filename)
      print(df)


      df1 = pd.read_csv(f.filename, delimiter=',', names = ['map', 'hero', 'with', 'SR Before', 'SR After', 'Fill', 'Your team quit', 'Other team quit', 'Teams\'s SR', 'Other team\'s SR', 'Date', 'OT', 'win' ])
      df1 = df1.drop(df1.index[0])
      df1['win'] = 0
      df1 = df1.dropna(how='any',axis=0)


      df1["SR Before"] = pd.to_numeric(df1["SR Before"])
      df1["SR After"] = pd.to_numeric(df1["SR After"])
      df1["win"] = pd.to_numeric(df1["win"])


      for index, row in df1.iterrows():
         if row['SR Before'] < row['SR After']:
            df1.at[index, 'win'] = 1
         else:
            df1.at[index, 'win'] = 0    
            
      df2 = df1.loc[df1['win'] == 1]
      df3 = pd.Series(' '.join(df2['map']).lower().split()).value_counts()[:100]
      df3.head(1)
      map_result = str(df3.head(1))
      map_result = map_result.split(' ', 1)[0]
      # print("You did the best on " + map_result)


      return render_template("results.html", map_result = map_result)






if __name__ == "__main__":
    app.run(debug=True)