# modelo/hotel.py

from sqlalchemy import Column, Integer, String
from modelo.database import Base, session

class Hotel(Base):
    __tablename__ = 'hoteles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    
    @classmethod
    def obtener_hotel_por_id(cls, hotel_id):
        return session.query(cls).filter_by(id=hotel_id).first()

# modelo/reserva.py

from sqlalchemy import Column, Integer, Date, ForeignKey
from modelo.database import Base, session

class Reserva(Base):
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    habitacion_id = Column(Integer, ForeignKey('habitaciones.id'), nullable=False)
    trabajador_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=False)
    
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    
    @classmethod
    def obtener_reserva_por_id(cls, reserva_id):
        return session.query(cls).filter_by(id=reserva_id).first()
