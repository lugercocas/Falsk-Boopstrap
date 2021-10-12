from flask import Flask, render_template, request, session, redirect
from modelodatos import usuarios

global logueado
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
            session['username'] = usuario
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
    return redirect('/')

@app.route('/admin')
def admin():
    global logueado
    if logueado:
        return render_template('admin.html',logueado=logueado)
    else:
        return render_template('/',logueado=logueado)

#Página de Registro
#@app.route('/registrarse')
#def registrarse():
#    return render_template('registrarse.html')

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
            return redirect('/login')
        else:
            return render_template('registrarse.html')
    else:
        return "Error --> Metodo no encontrado!"

def validaRegistro():
    return True
