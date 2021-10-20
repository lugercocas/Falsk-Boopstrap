from peewee import *
from playhouse.flask_utils import FlaskDB

db = FlaskDB()

class Usuario(db.Model):
    username = TextField(primary_key=True)
    nombre = TextField()
    rol = IntegerField() #0=usuario,1=admin,2=superadmin
    direccion = TextField()
    telefono = TextField()
    clave = TextField()

class Producto(db.Model):
    id_producto = AutoField()
    nombre_producto = TextField()
    precio = IntegerField()
    descripcion = TextField()
    descripcion_detallada = TextField()
    path_imagen = TextField()
    cantidad = IntegerField()
    unidad_medida = TextField() #Ej: Unidades, Litros, Cajas, etc.

#Relación Muchos a Muchos
class Comentario(db.Model):
    id_comentario = AutoField()
    usuario = ForeignKeyField(Usuario,backref='comentarios')
    producto = ForeignKeyField(Producto,backref='comentarios')
    comentario = TextField()
    calificacion = IntegerField() #Máx 5

class Compra(db.Model):
    id_compra = AutoField()
    cliente = ForeignKeyField(Usuario,backref='compras') #qué compras ha hecho un cliente
    total = IntegerField()
    fecha = DateField()

class DetalleCompra(db.Model):
    compra = ForeignKeyField(Compra,backref='productos') #Qué productos pertenecen a una compra
    producto = ForeignKeyField(Producto, backref='historial') #El producto ha sido comprado X veces
    costo = IntegerField()

class ListaDeseos(db.Model):
    usuario = ForeignKeyField(Usuario,backref='productos') 
    producto = ForeignKeyField(Producto,backref='listadeseos')