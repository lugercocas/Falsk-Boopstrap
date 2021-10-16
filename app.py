from flask import Flask, render_template, request, session, redirect
from modelodatos import usuarios
from modelodatos import productosdb
from modelodatos import comentarios
import funciones

global logueado
global idProducto
global user_logueado
idProducto = 0
logueado = False
#--------------------
#Activar modo debugger en powershell
#$env:FLASK_ENV = "development"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
    return render_template('productos.html',productos = productosdb,logueado=logueado)


@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

#Página Login
@app.route('/login/',methods =['POST','GET'])
def login():
    global logueado
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return redirect(validarInicioSesion(username,password))        
    elif(request.method == 'GET'):
        return render_template('login.html')
    else:
        return "Método no definido"

def validarInicioSesion(usuario,clave):
    pagina = ""
    for user in usuarios:
        #print(user[1],user[2],usuario,clave)
        if (user[1] == usuario and user[2]==clave):
            global logueado
            global user_logueado
            session['username'] = usuario
            user_logueado = user
            logueado = True
            pagina = "/admin"
            break
        else:
            pagina = "/login"
    return pagina

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
        if (user_logueado[0]==1):
            #Si es un Administrador, mostrar la página del admin
            return render_template('useradmin.html',logueado=logueado,usuario=user_logueado)
        elif (user_logueado[0]==2):
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
        print(nombres)
        print(direccion)
        print(telefono)
        print(usuario)
        print(password)
        #valida datos
        if validaRegistro():
            #yag = yagmail.SMTP('inge.gerardoc@gmail.com','12345')
            #yag.send(to=mail, subject='Acticación cuenta exitosa',
            #contents='Bienvenido, usa el siguiente enlace')
            #flash('Revisa tu correo para activar tu cuenta.')
            usuarios.append([0,usuario,clave,nombres,telefono,direccion])
            return redirect('/login')
        else:
            return render_template('registrarse.html')
    else:
        return "Error --> Metodo no encontrado!"

def validaRegistro():
    return True

@app.route('/admproductos')
def admProductos():
    global logueado
    global user_logueado
    return render_template ('admproductos.html', logueado=logueado,usuario=user_logueado, productos = productosdb)

@app.route('/producto',methods =['POST','GET'])
def eliminarProductos():
    global idProducto
    if request.method == 'GET':
        if(request.args.get('eliminarproducto') != None):
            id_producto = int(request.args.get('eliminarproducto'))
            i = 0
            for proc in productosdb:
                if(proc[0] == id_producto):
                    productosdb.pop(i)  
                    break       
                i = i+1
            return redirect('/admproductos')
        elif(request.args.get('editarproducto')!= None ):
            id_producto = int(request.args.get('editarproducto'))
            aux = []
            for proc in productosdb:
                if (proc[0] == id_producto):
                 aux = proc 
                 break 
            idProducto = id_producto    
            return render_template('editarproducto.html', producto = aux, logueado=logueado,usuario=user_logueado)
        elif(request.args.get('verproducto')!= None ):
            id_producto = int(request.args.get('verproducto'))
            aux = []
            aux2 =[]
            for proc in productosdb:
                if (proc[0] == id_producto):
                 aux = proc 
                 break 
            for coms in comentarios:
                if(coms[0] == id_producto):
                    aux2.append(coms)            
            return render_template('verproducto.html', producto = aux, logueado=logueado,usuario=user_logueado, opiniones = aux2)
    elif request.method == 'POST':
        nombreproducto = request.form.get('nombreproducto') 
        precio = request.form.get('precio') 
        #imagen = request.form.get('imagen')   
        descripcion = request.form.get('descripcion')         
        i = 0
        for p in productosdb:
            if p[0] == idProducto:
                productosdb[i][1] = nombreproducto
                productosdb[i][2] = precio
                #productosdb[i][3] = imagen
                productosdb[i][4] = descripcion
            i = i+1
        return redirect('/admproductos')
    
@app.route('/agregarproducto', methods =['POST','GET'])
def agregarproducto():
    global logueado
    global user_logueado
    if request.method == 'GET':        
        return render_template('/agergarproducto.html',logueado=logueado,usuario=user_logueado)
    elif request.method == 'POST':
        #leer datos del producto y actualizar
        id = len(productosdb) +1
        nombreproducto = request.form.get('nombreproducto') 
        precio = request.form.get('precio') 
        #imagen = request.form.get('imagen')   
        descripcion = request.form.get('descripcion') 
        print('Probando')
        print(productosdb)
        productosdb.append([id,nombreproducto,precio,'producto0.jpg',descripcion])
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
        comentarios.append([0, user_logueado[1],coment2,float(coment3)])
        print(comentarios)
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
        usuario = request.form.get('username') #El usuario es el mismo correo
        password = request.form.get('password')
        clave = request.form.get('passwordv') 
        j=0
        for us in usuarios:
            if us[0] == user_logueado[0]:
                usuarios[j]=[us[0],usuario,clave,nombres,telefono,direccion]
                user_logueado = [us[0],usuario,clave,nombres,telefono,direccion]
                break
            j = j+1        
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
        return render_template('usuarios.html',logueado=logueado,usuario=user_logueado,usuarios=usuarios)

@app.route('/usuarios/<usuario>/<rol>')
def usuariosact2(usuario,rol):
    l = 0
    global user_logueado
    for us in usuarios:
        if us[1]==usuario:
            #si el usuario ingresado es igual al usuario en BD, actualio el rol.
            usuarios[l][0] = rol
            user_logueado[0] = rol
            break
        l = l+1
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
        ids = request.args.get('idP')
        print(ids,coment,coment2,coment3)
        id = int(ids)
        comentarios.append([id, user_logueado[0],coment2,float(coment3)])
        redirect('/comprados')
