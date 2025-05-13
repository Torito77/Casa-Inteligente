import serial
from threading import Thread
import time
from database import db, register_readings

SERIAL_PORT = 'COM3'  
BAUD_RATE = 9600

class Duino_Manager:
    
    def get_datos(self):
        return self.datos
    
    def __init__(self):
        self.arduino = None
        self.datos: dict 
        
        def connect_to_arduino():
            while True:
                try:
                    self.arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                except serial.SerialException as e:
                    print(f"Error al abrir el puerto COM3: {e}")
                    self.arduino = None
                    time.sleep(1)
                else:
                    print("Connected succesfully")
                    break
        
        
        def read_arduino():
            while True:
                if self.arduino and self.arduino.in_waiting:
                    linea = self.arduino.readline().decode('utf-8').strip()
                    try:
                        self.datos = dict( item.split(":") for item in linea.split(",") )
                    except Exception as e:
                        print(f"Error procesando datos: {e}")
                    else:
                        register_readings(self.datos)
                
                # FIXME: This value may vary
                time.sleep(1)
    
        Thread(target=connect_to_arduino, daemon=True).start()
        Thread(target=read_arduino, daemon=True).start()