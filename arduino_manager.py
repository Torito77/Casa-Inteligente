import serial
from threading import Thread
import time
from database import db, register_readings

SERIAL_PORT = 'COM3'  
BAUD_RATE = 9600
RECONNECT_INTERVAL = 5
class Duino_Manager:
    
    def get_datos(self):
        return self.datos
    
    def __init__(self):
        self.arduino = None
        self.datos: dict 
        
        def connect_and_read():
            
            while True:
                if self.arduino is None or not self.arduino.is_open:
                    try:
                        self.arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                        print(f"Conectado exitosamente al puerto {SERIAL_PORT}")
                        
                    except serial.SerialException as e:
                        print(f"No se pudo conectar al puerto {SERIAL_PORT}: {e}")
                        self.arduino = None
                        time.sleep(RECONNECT_INTERVAL)
                        continue 

                try:
                    if self.arduino.in_waiting:
                        linea = self.arduino.readline().decode('utf-8').strip()
                        try:
                            self.datos = dict(item.split(":") for item in linea.split(","))
                            register_readings(self.datos)
                        except Exception as e:
                            print(f"Error procesando datos: {e}")
                            
                except (serial.SerialException, OSError) as e:
                    print(f"Conexión perdida: {e}")
                    self.arduino = None
                    time.sleep(RECONNECT_INTERVAL)

                time.sleep(1)
        
                Thread(target=connect_and_read, daemon=True).start()