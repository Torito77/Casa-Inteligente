from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Enum, UniqueConstraint, Text

import enum
from datetime import datetime
from typing import List, Optional

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class TipoDispositivo(db.Model):
    __tablename__="tipos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    
    dispositivos: Mapped[List["Dispositivo"]] = relationship("Dispositivo", back_populates="tipo", cascade="all, delete-orphan")
    
class Cuarto(db.Model):
    __tablename__="cuartos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationship to Dispositivo
    dispositivos: Mapped[List["Dispositivo"]] = relationship("Dispositivo", back_populates="cuarto", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cuarto {self.nombre}>"

class Dispositivo(db.Model):
    __tablename__ = "dispositivos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_instalacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # Relacion pa normalizar
    tipo_id: Mapped[int] = mapped_column(ForeignKey("tipos.id"))
    tipo: Mapped["TipoDispositivo"] = relationship("TipoDispositivo", back_populates="dispositivos")
    
    # Relaciones
    cuarto_id: Mapped[int] = mapped_column(ForeignKey("cuartos.id"))
    cuarto: Mapped["Cuarto"] = relationship("Cuarto", back_populates="dispositivos")
    
    # Relaciones polimórficas - un dispositivo puede ser o un sensor o un actuador
    sensor: Mapped[Optional["Sensor"]] = relationship("Sensor", back_populates="dispositivo", uselist=False, cascade="all, delete-orphan")
    actuador: Mapped[Optional["Actuador"]] = relationship("Actuador", back_populates="dispositivo", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dispositivo {self.nombre} ({self.tipo.tipo})>"

class Actuador(db.Model):
    __tablename__ = "actuadores"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_actuador: Mapped[str] = mapped_column(String(50), nullable=False)  # interruptor, válvula, motor, etc.
    voltaje: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    amperaje: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Relaciones
    dispositivo_id: Mapped[int] = mapped_column(ForeignKey("dispositivos.id"), unique=True)
    dispositivo: Mapped["Dispositivo"] = relationship("Dispositivo", back_populates="actuador")
    
    def __repr__(self):
        return f"<Actuador {self.dispositivo.nombre} - {self.tipo_actuador}>"

class Sensor(db.Model):
    __tablename__ = "sensores"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_sensor: Mapped[str] = mapped_column(String(50), nullable=False)  # temperatura, humedad, movimiento, etc.
    unidad_medida: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # °C, %, lux, etc.
    precision: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    frecuencia_lectura: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Relaciones
    dispositivo_id: Mapped[int] = mapped_column(ForeignKey("dispositivos.id"), unique=True)
    dispositivo: Mapped["Dispositivo"] = relationship("Dispositivo", back_populates="sensor")
    
    det_lecturas: Mapped[List["DetLectura"]] = relationship("DetLectura", back_populates="sensor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Sensor {self.tipo_sensor}>"


class Lectura(db.Model):
    __tablename__= "lecturas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    det_lecturas: Mapped[List["DetLectura"]] = relationship("DetLectura", back_populates="lectura", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lectura {self.id}: {self.timestamp}>"


class DetLectura(db.Model):
    __tablename__="det_lecturas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Relationship to Lectura
    lectura_id: Mapped[int] = mapped_column(ForeignKey("lecturas.id"))
    lectura = relationship("Lectura", back_populates="det_lecturas")
    
    # Relationship to Sensor
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensores.id"))
    sensor = relationship("Sensor", back_populates="det_lecturas")
    

def register_readings( sensor_readings: dict ):
    
    nueva_lectura = Lectura()
    db.session.add(nueva_lectura)
    
    db.session.flush()
    
    for sensor_type, valor in sensor_readings.items():
        
        sensor = db.session.query(Sensor).filter_by(tipo_sensor=sensor_type).first()
        
        if sensor:
            
            det_lectura = DetLectura(
                lectura_id=nueva_lectura.id,
                sensor_id=sensor.id,
                valor=valor
            )
            db.session.add(det_lectura)
        
        
        db.commit()
        return nueva_lectura