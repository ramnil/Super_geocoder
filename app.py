import os
from csv import DictReader, reader
from flask import Flask, render_template, request, redirect, send_file
from geopy.geocoders import ArcGIS
import pandas as pd

app=Flask(__name__)

app.config["IMAGE_UPLOADS"]="/Users/krzysztof/Desktop/programowanie_python/super_geocoder/uploads"

def geo_finder(file_csv):
    arc = ArcGIS()
    df = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], file_csv)) 
    coordinates = df["Address"].apply(arc.geocode)
    df['Latitude'] = coordinates.apply(lambda x: x.latitude if x != None else None)
    df['Longitude'] = coordinates.apply(lambda x: x.longitude if x != None else None)
    end_file = df.to_csv(os.path.join(app.config["IMAGE_UPLOADS"], file_csv), index=False, mode='w')
    print(df)
    return end_file

@app.route("/")
def index():
    
    return render_template("index.html")
  

@app.route("/success", methods=['GET', 'POST'])
def success():
    global path_csv
    if request.method == "POST":
        
        csv_file= request.files["file"] 
        if csv_file.filename == "" :
            print("CSV must have a file name")
            return redirect(request.url)

        path_csv = os.path.join(app.config["IMAGE_UPLOADS"], csv_file.filename)
        csv_file.save(path_csv)
        with open(path_csv, 'r') as f:
            f_col = DictReader(f)
            f_col = f_col.fieldnames
            if "Address" in f_col:
                geo_finder(csv_file.filename)
                data = []
                with open(path_csv) as file:
                    csv_table = reader(file)
                    for row in csv_table:
                        data.append(row)
                data = pd.DataFrame(data)    
                return render_template("success.html", data=data.to_html(header=False,  index=False))
            elif "address" in f_col:
                geo_finder(csv_file.filename)
                data = []
                with open(path_csv) as file:
                    csv_table = reader(file)
                    for row in csv_table:
                        data.append(row)
                data = pd.DataFrame(data)    
                return render_template("success.html", data=data.to_html(header=False,  index=False))
            else:
                
                return render_template("success.html", text= '** Please make sure there is "Address" or "address" in "Address" column **')
             

@app.route("/download")
def download_csv():
    return send_file(path_csv, attachment_filename="geolocation.csv", as_attachment=True)


if  __name__ == '__main__':
    app.debug=True
    app.run()









#    
