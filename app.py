from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import datetime
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash, check_password_hash
#from modelodatos import productosdb
from modelodatos import comentarios
import funciones
from models import *
from config import dev

global logueado
global idProducto
global user_logueado
idProducto = 0
logueado = False
#--------------------
#Activar modo debugger en powershell
#$env:FLASK_ENV = "development"

app = Flask(__name__)
app.config.from_object(dev)
db.init_app(app)

@app.route('/')
def index():
    global logueado
    print(logueado)
    return render_template('index.html', logueado=logueado)

@app.route('/soporte')
def soporte():
    global logueado
    return render_template('soporte.html',logueado = logueado)

@app.route('/productos')
def productos():
    global logueado
    product = Producto.select() #productosdb
    return render_template('productos.html',productos = product,logueado=logueado)


@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

#Página Login
@app.route('/login/',methods =['POST','GET'])
def login():
    global logueado
    global user_logueado
    pagina = "/login"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userdb = Usuario.get_or_none(username=username)
        p= generate_password_hash(password)
        print(p)
        p1 = check_password_hash(p, password)
        print(p1)
        #check_password_hash
        if(userdb == None):
            print("Usuario no existe...")
            pagina = "/login"
        elif(check_password_hash(userdb.clave, password)):#(userdb.clave==password):#
            print("Usuario y clave correctos")
            session['username'] = username
            user_logueado = userdb
            logueado = True
            pagina = "/admin"
        else:
            print("Clave incorrecta..")
            pagina = "/login"
        return redirect(pagina)        
    elif(request.method == 'GET'):
        return render_template('login.html')
    else:
        return "Método no definido"

@app.route('/logout')
def logout():
    global logueado
    logueado = False
    #eliminamos la sesión.
    session.pop('username')
    return redirect('/')

@app.route('/admin')
def admin():
    global logueado
    global user_logueado
    if logueado:
        #validamos el rol y devolvemos la vista que necesita.
        if (user_logueado.rol==1):
            #Si es un Administrador, mostrar la página del admin
            return render_template('useradmin.html',logueado=logueado,usuario=user_logueado)
        elif (user_logueado.rol==2):
            #Si es un Super Administrador, mostrar la página del superadmin
            return render_template('usersuper.html',logueado=logueado,usuario=user_logueado)
        else:
            #En caso contrario retornar la página del usuario
            return render_template('user.html',logueado=logueado,usuario=user_logueado)        
    else:
        return redirect('/login/')

#Página de Registro
@app.route('/registrarse',methods =['POST','GET'])
def registrarse():
    if request.method == 'GET':
        return render_template('registrarse.html')
    elif request.method == 'POST':
        #Tratar datos de entrada
        nombres = request.form.get('nombres') 
        direccion = request.form.get('direccion') 
        telefono = request.form.get('telefono')          
        usuario = request.form.get('username') #El usuario es el mismo correo
        password = request.form.get('password')
        clave = request.form.get('passwordv') 
        #valida datos
        if validaRegistro():
            #yag = yagmail.SMTP('inge.gerardoc@gmail.com','12345')
            #yag.send(to=mail, subject='Acticación cuenta exitosa',
            #contents='Bienvenido, usa el siguiente enlace')
            #flash('Revisa tu correo para activar tu cuenta.')
            Usuario.get_or_create(
                username=usuario, 
                nombre=nombres,
                rol=0,
                direccion=direccion,
                telefono=telefono,
                clave=generate_password_hash(password)
            )
            #usuarios.append([0,usuario,clave,nombres,telefono,direccion])
            return redirect('/login')
        else:
            return render_template('registrarse.html')
    else:
        return "Error --> Metodo no encontrado!"

def validaRegistro():
    return True

@app.route('/eliminarusuario',methods =['POST'])
def eliminarusuario():
    usuario = request.form.get('usuario')
    print(usuario)
    Usuario.get(Usuario.username == usuario).delete_instance()
    return redirect('/usuarios')

@app.route('/admproductos')
def admProductos():
    global logueado
    global user_logueado
    prod = Producto.select()
    return render_template ('admproductos.html', logueado=logueado,usuario=user_logueado, productos = prod)

@app.route('/producto',methods =['POST','GET'])
def eliminarProductos():
    global idProducto
    global user_logueado
    if request.method == 'GET':
        if(request.args.get('eliminarproducto') != None):
            id_producto = int(request.args.get('eliminarproducto'))
            #Validar de nuevo si tiene el rol para eliminar producto
            Producto.get(id_producto).delete_instance()
            return redirect('/admproductos')
        elif(request.args.get('editarproducto')!= None ):
            id_producto = int(request.args.get('editarproducto'))
            prod = Producto.get_or_none(id_producto)
            print(prod)
            idProducto = id_producto             
            return render_template('editarproducto.html', producto = prod, logueado=logueado,usuario=user_logueado)            
        elif(request.args.get('verproducto')!= None ):
            id_producto = int(request.args.get('verproducto'))
            aux2 =[]
            prod = Producto.get_or_none(id_producto)
            #coments = Comentario.select().where(producto_id==id_producto)
            for coms in comentarios:
                if(coms[0] == id_producto):
                    aux2.append(coms)            
            if(logueado==True):                
                return render_template('verproducto.html', producto = prod, logueado=logueado,usuario=user_logueado, opiniones = aux2)
            else:
                return render_template('verproducto.html', producto = prod, logueado=False,usuario="", opiniones = aux2)
    elif request.method == 'POST':
        id_producto = int(request.form.get('id_producto'))
        nombreproducto = request.form.get('nombreproducto') 
        precio = request.form.get('precio') 
        nameimage = Producto.get(id_producto).path_imagen
        #Si no se envía ninguna imagen, se deja la misma.
        try:
            imagen = request.files['imagen'] 
            ex = imagen.filename.rsplit(".")
            nameimage = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+ex[len(ex)-1]
            imagen.save("./static/img/"+secure_filename(nameimage))            
        except:
            nameimage = Producto.get(id_producto).path_imagen
        descripcion = request.form.get('descripcion') 
        descripciondet = request.form.get('descripciondet') 
        cantidad = int(request.form.get('cantidad'))
        p = Producto.update(
            nombre_producto = nombreproducto,
            precio = precio,
            descripcion = descripcion,
            descripcion_detallada = descripciondet,
            path_imagen = nameimage,
            cantidad = cantidad,
            unidad_medida = 'Unidades'
        )
        p.where(Producto.id_producto==id_producto).execute()
        return redirect('/admproductos')
    
@app.route('/agregarproducto', methods =['POST','GET'])
def agregarproducto():
    global logueado
    global user_logueado
    if request.method == 'GET':        
        return render_template('/agergarproducto.html',logueado=logueado,usuario=user_logueado)
    elif request.method == 'POST':
        #leer datos del producto y actualizar
        nombreproducto = request.form.get('nombreproducto') 
        precio = request.form.get('precio') 
        imagen = request.files['imagen'] 
        ex = imagen.filename.rsplit(".")
        print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        nameimage = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+ex[len(ex)-1]
        print(nameimage)
        imagen.save("./static/img/"+secure_filename(nameimage))
        descripcion = request.form.get('descripcion') 
        descripciondet = request.form.get('descripciondet') 
        cantidad = int(request.form.get('cantidad'))
        Producto.get_or_create(
            nombre_producto = nombreproducto,
            precio = precio,
            descripcion = descripcion,
            descripcion_detallada = descripciondet,
            path_imagen = nameimage,
            cantidad = cantidad,
            unidad_medida = 'Unidades'
        )
        return redirect('/admproductos')
        #return render_template('/agergarproducto.html',logueado=logueado,usuario=user_logueado)

@app.route('/perfil')
def perfil():
    global logueado
    global user_logueado
    return render_template('perfil.html',logueado=logueado,usuario=user_logueado)

@app.route('/comprados/comentar/', methods=['GET', 'POST'])
def comentar():
    global logueado
    global user_logueado
    global idProducto 
    if(request.method == 'GET'):
        global logueado
        global user_logueado
        return render_template('comentar.html', logueado=logueado, usuario=user_logueado)
    elif(request.method == 'POST'):
        coment = request.form.get('comtxt')
        coment2 = request.form.get('comtxt2')
        coment3 = request.form.get('comtxt3') #calificación
        #ids = 1#request.form.get('idP')
        #comentarios.append([0, user_logueado[1],coment2,float(coment3)])
        #print(comentarios)
        Comentario.get_or_create(
            usuario = user_logueado,
            producto = idProducto,
            comentario = coment,
            calificacion = int(coment3)
        )
        return redirect('/comprados')

@app.route('/comprados/')
def comprados():
    global logueado
    global user_logueado
    return render_template('comprados.html', logueado=logueado, usuario=user_logueado)

@app.route('/actualizardatos', methods=['POST'])
def actualizardatos():
    global logueado
    global user_logueado
    if request.method == 'POST': 
        nombres = request.form.get('nombres') 
        direccion = request.form.get('direccion') 
        telefono = request.form.get('telefono')          
        usuario = user_logueado.username
        password =  generate_password_hash(request.form.get('password'))
        #clave = request.form.get('passwordv') 
        us = Usuario.update(nombre=nombres,direccion=direccion,telefono=telefono,clave=password)
        us.where(Usuario.username==usuario).execute()
        user_logueado = Usuario.get(username=usuario)     
        return render_template('/perfil.html',logueado=logueado, usuario=user_logueado)
    else:
        return redirect('admin')

@app.route('/usuarios')
def usuariosact():
    global logueado
    global user_logueado
    if request.method == 'POST': 
        pass
    else:
        users = Usuario.select()
        return render_template('usuarios.html',logueado=logueado,usuario=user_logueado,usuarios=users)

@app.route('/usuarios/<usuario>/<rol>')
def usuariosact2(usuario,rol):
    Usuario.update(rol=int(rol)).where(Usuario.username==usuario).execute()
    return redirect('/usuarios')

@app.route('/comentar/comentara',methods=['GET', 'POST'])
def comentario():
    global logueado
    global user_logueado
    global idProducto 
    if(request.method == 'GET'):
        if(request.args.get('enviar')!= None ):
            id_producto = int(request.args.get('idP'))
            aux =[]
            if(request.args.get('comtxt2')!= ''):
                if(request.args.get('comint')!=''):
                    if(funciones.es_flotante(float(request.args.get('comint')))):
                        aux = [id_producto,user_logueado[0],request.args.get('comtxt2'), int(request.args.get('comint'))]
                        comentarios.append(aux)
                        return render_template('comprados.html', logueado=logueado, usuario=user_logueado)
        elif(request.args.get('cancelar')!= None ):
            return render_template('comprados.html', logueado=logueado, usuario=user_logueado)
    elif request.method == 'POST':
        coment = request.args.get('comtxt')
        coment2 = request.args.get('comtxt2')
        coment3 = request.args.get('comtxt3')
        #ids = request.args.get('idP')
        #print(ids,coment,coment2,coment3)
        #id = int(ids)
        #comentarios.append([id, user_logueado[0],coment2,float(coment3)])
        Comentario.get_or_create(
            usuario = user_logueado,
            producto = idProducto,
            comentario = coment,
            calificacion = int(coment3)
        )
        return render_template('comprados.html', logueado=logueado, usuario=user_logueado)

@app.route('/listadeseos', methods=['GET', 'POST'])
def listadeseos():
    global logueado
    global user_logueado
    if(request.method == 'GET'):        
        user = session['username']
        print(request.args.get('agregarroducto'))
        prods = []
        if request.args.get('agregarroducto') != None:              
            producto = int(request.args.get('agregarroducto'))    
            ListaDeseos.get_or_create(
                usuario = user,
                producto = producto
            )
        ps = list(ListaDeseos.select().where(ListaDeseos.usuario==user).execute())
        prods = []
        for p in ps:
            prods.append(model_to_dict(p.producto))
        return render_template('/listadeseos.html',productos = prods,logueado=logueado,usuario=user_logueado)
    elif(request.method == 'POST'):
        #procesar agregar/eliminar prod, lista deseos
        prodelim = request.form.get('eliminarprolista') 
        print(prodelim)
        #Producto.get(id_producto).delete_instance()
        ListaDeseos.get(ListaDeseos.producto==prodelim).delete_instance()
        return redirect('/listadeseos')

if __name__=="__main__":
    app.run()