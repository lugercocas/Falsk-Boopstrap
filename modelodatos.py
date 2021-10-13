#Modelo Usuarios:
#[rol, usuario/correo, clave, nombres, telefono, direccion]
#rol--> 0 = usuario, 1 = Admin y 2 = superadmin
usuarios = [
    [0,'user@rs.co','Pass123','Usuario Normal','31344324','Calle 1 #4-4'],
    [1,'admin@rs.co','Pass123','Usuario Admin','31344325','Calle 1 #4-5'],
    [2,'super@rs.co','Pass123','Usuario Superadmin','31344326','Calle 1 #4-6']
]

#Modelo Productos
#[IdProducto,NombreProducto,PrecioProducto,ImagenProducto,DescripcionCorta]
productosdb = [
    [0,'Computador HP',2500000,'producto0.jpg','Producto en excelente estado con Intel Core I9, 1000GB SSD, 16GB RAM'],
    [1,'Computador M1',1500000,'producto1.jpg','Producto en excelente estado con Intel Core I7, 500GB SSD, 12GB RAM'],
    [2,'Computador M2',1000000,'producto2.jpg','Producto en excelente estado con Intel Core I7, 400GB SSD, 12GB RAM'],
    [3,'Computador M3',1000000,'producto3.jpg','Producto en excelente estado con Intel Core I3, 200GB SSD, 12GB RAM']
]
#Modelo comentarios
#[IdProducto,usuario,comentario,calificación]
comentarios = [
    [0,'user@rs.co','Es un muy buen producto',5],
    [1,'user@rs.co','Es un muy buen producto',4]
]