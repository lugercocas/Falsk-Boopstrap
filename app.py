from flask import Flask, render_template, request, session, redirect
from modelodatos import usuarios
from modelodatos import productosdb
from modelodatos import comentarios


global logueado
global user_logueado
logueado = False


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    global logueado
    print(logueado)
    return render_template('index.html', logueado=logueado)

@app.route('/soporte')
def soporte():
    return render_template('soporte.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')


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
        print(user[1],user[2],usuario,clave)
        if (user[1] == usuario and user[2]==clave):
            global logueado
            global user_logueado
            session['username'] = usuario
            user_logueado = user
            logueado = True
            pagina = "/"
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
            return render_template('editarproducto.html', producto = aux, logueado=logueado,usuario=user_logueado)
        elif(request.args.get('verproducto')!= None ):
            return render_template('verproducto.html')
    elif request.method == 'POST':
        nombreproducto = request.form.get('nombreproducto') 
        precio = request.form.get('precio') 
        descripcion = request.form.get('descripcion') 
        nombreproducto = request.form.get('nombreproducto') 
        render_template('/admproductos')
    

    
