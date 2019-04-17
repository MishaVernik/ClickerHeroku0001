from flask import Flask, request
import urllib.request
import requests
import time
from threading import Timer

 
app = Flask(__name__)

counter = 1
number_of_repeats = 0
sleeping_time = 0
link = ""

@app.route("/btn_find", methods=['POST'])
def get_ses():
    global link
    global sleeping_time
    global counter    
    global number_of_repeats
    global app

    couter = 1
    if number_of_repeats == 0:
        number_of_repeats = int(request.form['number'])
    if sleeping_time == 0:
        sleeping_time = float(request.form['sleeping'])
    if link == "":
        s = request.form['text']
        link = s
    
    #response = urllib.request.urlopen(request.form['text'])    
    while number_of_repeats > 0:
        if (sleeping_time*(counter+1) > 25):
            break
        counter +=1
        number_of_repeats -= 1  
        send_request(link)
        print('#'*40)
        print(number_of_repeats)
        print('#'*40)        
        time.sleep(sleeping_time)
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clicker chooser Online</title>
</head>
<body>
<h2 align="center">Welcome to the Clicker.online!</h2>
<form method="POST" action="">
    <h3>Link</h3>
    <p align="center">
        <input name="text" type="text" value="{link}">
    </p>
    <h3>Number of repeats</h3>
     <p align="center">
        <input name="number" type="text" value="{number_repeats}">
    </p>
    <h3>Sleeping time</h3>
     <p align="center">
        <input name="sleeping" type="text" value="{sleeping}">
    </p>
</form>
</body>
</html>
'''
    if number_of_repeats < 0:        
        return "Success"
    
    html = html.replace("{number_repeats}", str(number_of_repeats))
    html = html.replace("{link}", str(link))
    html = html.replace("{sleeping}", str(sleeping_time))
    t = Timer(5.0, app.run)
    t.start()
    #return html

        
def send_request(s):
    try:            
        r = requests.get(s)
        r.raise_for_status()
        print('#'*40)
        print("YES")
        print('#'*40)     
        if r.status_code == 200:        
            return 1           
    except requests.exceptions.HTTPError as err:        
        send_request(s)

 
    

@app.route('/')
def source():
    global link
    global sleeping_time
    global counter    
    global number_of_repeats
    if link != "":
        get_ses()        
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clicker chooser Online</title>
</head>
<body>
<h2 align="center">Welcome to the Clicker.online!</h2>
<form method="POST" action="/btn_find">
    <h3>Link</h3>
    <p align="center">
        <input name="text" type="text" value="">
    </p>
    <h3>Number of repeats</h3>
     <p align="center">
        <input name="number" type="text" value="">
    </p>
    <h3>Sleeping time</h3>
     <p align="center">
        <input name="sleeping" type="text" value="">
    </p>
    <p align="center">
        <input name="start" type="submit" value="Start">
    </p>
</form>
</body>
</html>
'''
    
    return html
