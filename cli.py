from app import *
import datetime

@app.cli.command("datos_default")
def datos_default():
    db.init_app(app)
    usuario = Usuario.get_or_create(
        username='user@rs.com', 
        nombre='Cliente Perez',
        rol=0,
        direccion='Calle 1A #25c-33',
        telefono='3133545648',
        clave='Pass123'
    )
    print(usuario)
    admin = Usuario.get_or_create(
        username='admin@rs.com', 
        nombre='Administrador Perez',
        rol=1,
        direccion='Calle 1A #25c-34',
        telefono='3133545648',
        clave='Pass123'
    )
    print(admin)
    super = Usuario.get_or_create(
        username='super@rs.com', 
        nombre='Super Administrador Perez',
        rol=2,
        direccion='Calle 1A #25c-33',
        telefono='3133545649',
        clave='Pass123'
    )
    print(super)
    producto1 = Producto.get_or_create(
        nombre_producto = 'Computador HP',
        precio = 2000000,
        descripcion = 'Producto en excelente estado con Intel Core I9',
        descripcion_detallada = 'Producto en excelente estado con Intel Core I9, 1000GB SSD, 16GB RAM',
        path_imagen = 'producto0.jpg',
        cantidad = 10,
        unidad_medida = 'Unidades'
    )
    print(producto1)
    producto2 = Producto.get_or_create(
        nombre_producto = 'Computador M1',
        precio = 1500000,
        descripcion = 'Producto en excelente estado con Intel Core I7',
        descripcion_detallada = 'Producto en excelente estado con Intel Core I7, 500GB SSD, 12GB RAM',
        path_imagen = 'producto1.jpg',
        cantidad = 20,
        unidad_medida = 'Unidades'
    )
    print(producto2)
    producto3 = Producto.get_or_create(
        nombre_producto = 'Computador M2',
        precio = 1400000,
        descripcion = 'Producto en excelente estado con Intel Core I5',
        descripcion_detallada = 'Producto en excelente estado con Intel Core I5, 500GB SSD, 12GB RAM',
        path_imagen = 'producto2.jpg',
        cantidad = 100,
        unidad_medida = 'Unidades'
    )
    print(producto3)
    producto4 = Producto.get_or_create(
        nombre_producto = 'Computador M3',
        precio = 1200000,
        descripcion = 'Producto en excelente estado con Intel Core I3',
        descripcion_detallada = 'Producto en excelente estado con Intel Core I3, 500GB SSD, 12GB RAM',
        path_imagen = 'producto3.jpg',
        cantidad = 98,
        unidad_medida = 'Unidades'
    )
    print(producto4)
    comentario1 = Comentario.get_or_create(
        usuario = 'user@rs.com',
        producto = 1,
        comentario = 'Excelente producto',
        calificacion = 5
    )
    print(comentario1)
    comentario2 = Comentario.get_or_create(
        usuario = 'user@rs.com',
        producto = 2,
        comentario = 'Me gustó producto',
        calificacion = 4
    )
    print(comentario2)
    compra1 = Compra.get_or_create(
        cliente = 'user@rs.com',
        total = 100000,
        fecha = datetime.datetime.now()
    )
    print(compra1)
    compra2 = Compra.get_or_create(
        cliente = 'user@rs.com',
        total = 200000,
        fecha = datetime.datetime.now()
    )
    print(compra2)
    detallecompra1 = DetalleCompra.get_or_create(
        compra = 1,
        producto = 1,
        costo = 15000
    )
    print(detallecompra1)
    detallecompra2 = DetalleCompra.get_or_create(
        compra = 1,
        producto = 2,
        costo = 15000
    )
    print(detallecompra2)
    detallecompra3 = DetalleCompra.get_or_create(
        compra = 2,
        producto = 3,
        costo = 50000
    )
    print(detallecompra3)
    listadeseos = ListaDeseos.get_or_create(
        usuario = 'user@rs.com',
        producto = 1
    )
    print(listadeseos)    
    
app.cli()