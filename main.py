import eventlet
eventlet.monkey_patch() 

from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_socketio import SocketIO
from sqlalchemy import desc, asc, and_

from database import db, Dispositivo, Lectura, Sensor, DetLectura
from arduino_manager import Duino_Manager
from dotenv import load_dotenv

import time
import random as r
import os
import pandas as pd

# - - - - - - - - - - - Flask-app Config - - - - - - - - - - - - >

load_dotenv()
username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
database = os.environ["DB_NAME"]
app_key = os.environ["APP_KEY"]

app = Flask(__name__)
app.config['SECRET_KEY'] = app_key
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost/{database}'

Bootstrap5(app)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

with app.app_context():
    db.create_all()

# - - - - - - - - - - - - Micro Connection - - - - - - - - - - - - >

duino = Duino_Manager()

# - - - - - - - - - - - - Background Task - - - - - - - - - - - - >

def retrieve_data():
    
    while True:
        with app.app_context():
        
            datos = {}
            lectura: Lectura = Lectura.query.order_by(desc(Lectura.timestamp)).first()
            
            if lectura:
                
                datos["TIMESTAMP"] = lectura.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                dets_lectura = DetLectura.query.filter(DetLectura.lectura_id == lectura.id).all()
                
                for det_lectura in dets_lectura:
                    datos[det_lectura.sensor.tipo_sensor] = det_lectura.valor
            
            socketio.emit('nuevos_datos', datos )
            
            # Delay
            time.sleep(0.4)
            

@socketio.on('connect')
def on_connect():
    socketio.start_background_task(retrieve_data)

# - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - >

@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/lecturas')
def lecturas():
    return render_template("readings.html",lecturas=Lectura.query.order_by(desc(Lectura.timestamp)).all())

if __name__ == "__main__":
    socketio.run(app)