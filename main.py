# importaciones
from math import *
from sympy import *
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

class NoConvergenceError(Exception):
    pass

class InvalidFunctionError(Exception):
    pass

#! limpiar inputs
def clear_inputs():
    funcion_entry.delete(0, 'end')
    xl_entry.delete(0, 'end')                                                                           
    xu_entry.delete(0, 'end')
    porcentaje_entry.delete(0, 'end')
    clear_table()
              
#? graficar funcion
def plot_function(expression_str, result_data): #* expression_str: cadena con la funcion matemática ingresada  result_data: una lista con los resultados de las iteraciones
    x = np.linspace(float(xl_entry.get()), float(xu_entry.get()), 400)  #* toma los valores xl y xu directamente de los campos de entrada (Entry) de la interfaz gráfica
    y = lambdify(symbols('x'), sympify(expression_str))(x) #* sympify(expression_str): convierte la cadena a una expresión simbólica de SymPy. lambdify(symbols('x'), ...): convierte esa expresión simbólica en una función que puede trabajar numpy.

    plt.figure(figsize=(8, 6)) #* dimensiones de la grafica
    plt.plot(x, y, label=expression_str)  #* grafica de la curva con el nombre de la funcion

    roots_x = [float(row[2]) for row in result_data]  #* extre el valor de xr de cada iteracion para graficar   
    roots_y = [lambdify(symbols('x'), sympify(expression_str))(root) for root in roots_x]  #* evalua la fucion en cada xr para obtener y
    plt.scatter(roots_x, roots_y, color='red', label='Raíces encontradas', marker='o')  #* dibuja los puntos donde se encontraron las raices aproximadas

    plt.title("Gráfica de la Función y Raíces Encontradas") #* tilulo
    plt.xlabel("x") #* etiquetas de los ejes
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()  #* muestra el grafico en una ventana
    
#? limpiar tabla
def clear_table():
    for item in tree.get_children(): #* debuelve los ids de todas las fila de la tabla
        tree.delete(item)   #* elimina el cotenido de la fila correspondiente al id
        
#? declaramos funcion para determinar si es valida o no la funcion a manejar
def is_valid_function(funcion, valor): 
    x = symbols('x')
    try:
        func_expr = sympify(funcion)  #* convierte el string a una expresion simbolica con sympy
        lambdify(x, func_expr)(valor)  #* lambdify convierte la expresion simbolica en un funcion de python para evaluar con numeros
        return True
    except Exception:
        return False

#? evaluamos la funcion para encontrar los valores de la funcion evaluados
def evaluar(x):
    return round(eval(funcion_entry.get()),4)

def fala_posicion(error_relativo, xl, xu):
    
    if not is_valid_function(funcion_entry.get(), xl) or not is_valid_function(funcion_entry.get(), xu):
        raise InvalidFunctionError("La función no es válida en los puntos iniciales X_L y X_U.")
    
    #? declaramos arrays donde almacenaremos los valores encontrados 
    tabla=[]
    porcentaje_error=100;
    
    #? declaramos variable de conteo para saber el numero de iteraciones
    contador=0
    fin=100
    while(porcentaje_error>=error_relativo):

        #? hallamos los valores evaludos en la funcion y el valor de xr
        fxl=evaluar(xl)
        fxu=evaluar(xu)
    
        try:
            xr = round(xu - ((fxu * (xl - xu)) / (fxl - fxu)), 4)
        except ZeroDivisionError:
            messagebox.showerror("Error",str("El metodo no converge division entre cero en XR"))
            return tabla
        
        fxr=evaluar(xr)
        
        #? determinamos el error relativo porcentual y lo almacenamos en la tabla 
        if(contador == 0):
            porcentaje_error="####"
        else:
        
            try:
                porcentaje_error=abs(round(((xr-tabla[contador-1][2])/xr)*100,4))
            except ZeroDivisionError:
                porcentaje_error="error"
                messagebox.showerror("Error", str("division entre cero metodo no converge en hallar error relativo porcentual"))
                return tabla
                
        if(porcentaje_error=="####"):
            tabla.append([contador+1,xl,xr,xu,fxl,fxr,fxu,porcentaje_error])
            porcentaje_error=100
        else:
            tabla.append([contador+1,xl,xr,xu,fxl,fxr,fxu,porcentaje_error])
            
        #? determinamos nuevos intervalos
        if(fxl*fxu>=0):
            
            messagebox.showerror("Error",str(f"metodo no converge fxl*fxu > 0 => '{fxl*fxu}' ")) 
            return tabla
        else:
            if((fxl <= 0) and (fxr <= 0 )):
                xl=xr
            elif((fxu<=0) and (fxr<=0)):
                xu=xr
            elif((fxl>=0) and (fxr>=0)):
                xl=xr
            elif((fxu>=0) and (fxr>=0)):
                xu=xr
            else:
                messagebox.showerror("Error",str("todos los signos son iguales no es posible continuar "))
                return tabla
        contador+=1
        if(contador==fin):
            return tabla
    return tabla

#? mse crea el tablero de valores 
def tablero (error,XL,XU):
    
    try:
        error_relativo=float(error)
        xl=float(XL)
        xu=float(XU)
        result_data = fala_posicion(error_relativo,xl,xu)
        clear_table()
        for row_data in result_data:
            tree.insert('', 'end', values=row_data)
        plot_function(funcion_entry.get(),result_data)
    except (InvalidFunctionError, ValueError,NoConvergenceError) as e:
        messagebox.showerror("Error", str(e))
    
#? creamos interfazes

#? creamos interfaz de instrucciones 
def crear_ventana1():
    root = Tk()
    root.geometry("800x500")
    root.title("Método de Falsa Posición")
    root.config(bg="#2F4F4F")  

    # Título principal
    titulo = Label(root, text="Método de Falsa Posición", font=('Helvetica', 20, 'bold'),
                   bg="#2F4F4F", fg="white")
    titulo.pack(pady=10)

    # Subtítulo
    sub_titulo = Label(root, text="Instrucciones a seguir", font=('Helvetica', 12, 'bold'),
                       bg="#2F4F4F", fg="lightblue")
    sub_titulo.pack()

    # Contenedor desplazable
    contenedor = Frame(root, bg="#2F4F4F")
    contenedor.pack(expand=True, fill=BOTH, padx=20, pady=10)

    canvas = Canvas(contenedor, bg="#2F4F4F", highlightthickness=0)
    scrollbar = Scrollbar(contenedor, orient=VERTICAL, command=canvas.yview)
    frame_interno = Frame(canvas, bg="#2F4F4F")

    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Lista de instrucciones
    instrucciones = [
        "➤ Usa paréntesis para exponentes, por ejemplo: x^(2)",
        "➤ Solo se permite la variable 'x', no uses otras letras.",
        "➤ No ingreses letras en los campos numéricos.",
        "➤ Ingresa el porcentaje tal como está en el ejercicio, por ejemplo: 5%",
        "➤ Para logaritmo base 10 usa: log(x,10)",
        "➤ Para logaritmo natural puedes usar simplemente: log(x)",
        "➤ Los tableros solo modifican la caja de función. Otros campos deben llenarse manualmente.",
        "➤ Usa signos válidos: + (suma), - (resta), * (multiplicación), / (división)",
        "➤ Solo se permiten funciones compatibles con la interfaz.",
        "➤ Seguir correctamente los pasos te dará una buena respuesta."
    ]

    for instruccion in instrucciones:
        Label(frame_interno, text=instruccion, font=('Helvetica', 10), bg="#2F4F4F", fg="white", anchor="w", justify=LEFT).pack(anchor="w", pady=2)

    # Botón para iniciar
    iniciar = Button(root, text="Iniciar", font=('Helvetica', 12, 'bold'), bg="#4CAF50", fg="white",
                     activebackground="#45A049", width=20, height=2, bd=0, command=root.destroy)
    iniciar.pack(pady=15)

    root.mainloop()
    
crear_ventana1()

root2=Tk()
root2.geometry("950x650")
root2.config(bg="#2F4F4F")
root2.title("Pedir datos")

#? Título de sección VALORES DE ENTRADA 

Label(root2, text="Valores de Entrada", font=('Helvetica', 16, 'bold'), bg="#2F4F4F", fg="white").place(x=50, y=90)

estilo_etiqueta = {'font': ('Helvetica', 10, 'bold'), 'bg': "#2F4F4F", 'fg': "white"}

estilo_entry = {'width': 30}

Label(root2, text="Función", **estilo_etiqueta).place(x=20, y=140)
funcion_entry = ttk.Entry(root2, name="funcion", **estilo_entry)
funcion_entry.place(x=152, y=140)

Label(root2, text="XL (Límite Inferior)", **estilo_etiqueta).place(x=20, y=180)
xl_entry = ttk.Entry(root2, name="xl", **estilo_entry)
xl_entry.place(x=152, y=180)

Label(root2, text="XU (Límite Superior)", **estilo_etiqueta).place(x=20, y=220)
xu_entry = ttk.Entry(root2, name="xu", **estilo_entry)
xu_entry.place(x=152, y=220)

Label(root2, text="Error (%)", **estilo_etiqueta).place(x=20, y=260)
porcentaje_entry = ttk.Entry(root2, name="porcentaje", **estilo_entry)
porcentaje_entry.place(x=152, y=260)


#? enviar valores a caja de texto para la funcion
def enviar_numero(valor):
    
    posicion_cursor=funcion_entry.index(tk.INSERT)
    funcion_entry.insert(posicion_cursor,valor)
    
#? envio del '.' y '^'
def enviar_simbolos(simbolo):
    posicion_cursor=funcion_entry.index(tk.INSERT)
    
    if(simbolo=="^"):
        funcion_entry.insert(posicion_cursor,"**()")
    else:
        funcion_entry.insert(posicion_cursor,simbolo)
    
#? tablero numerico
Label(root2, text="Valores Numéricos", font=('Helvetica', 16, 'bold'), bg="#2F4F4F", fg="white").place(x=350, y=90)

#? Frame contenedor del tablero
tablero_numeros = Frame(root2, bg="#2F4F4F")
tablero_numeros.place(x=355, y=138)

#? Estilo común para botones
boton_style = {
    'width': 4,
    'height': 2,
    'bg': "#D3D3D3",
    'fg': "#000000",
    'font': ('Helvetica', 12, 'bold'),
    'bd': 2,
    'relief': 'raised'
}

#? Diccionario de botones para crear en bucle
botones = [
    ('1', 0, 0), ('2', 0, 1), ('3', 0, 2), ('4', 0, 3),
    ('5', 1, 0), ('6', 1, 1), ('7', 1, 2), ('8', 1, 3),
    ('9', 2, 0), ('0', 2, 1), ('.', 2, 2), ('^', 2, 3)
]

#? Funciones de mapeo
def accion(valor):
    if valor in '0123456789':
        enviar_numero(int(valor))
    else:
        enviar_simbolos(valor)

#? Crear botones dinámicamente
for texto, fila, col in botones:
    Button(
        tablero_numeros,
        text=texto,
        command=lambda val=texto: accion(val),
        **boton_style
    ).grid(row=fila, column=col, padx=5, pady=5)

#? creamos funcion para mandar los valores del tablero a la caja de texto de funcion
funcionVar=StringVar()
def funciones():
    
    if(funcion_entry.get()==""):
        
        funciones=["e","sen()","cos()","tan()","log()","sqrt()"]
        posicion_cursor=funcion_entry.index(tk.INSERT)
        for fun in range(0,len(funciones)):
            if(funcionVar.get()==funciones[fun]):
                if(funcionVar.get()=="sen()"):
                    funcion_entry.insert(posicion_cursor,"sin()")
                else:
                    funcion_entry.insert(posicion_cursor,funcionVar.get())
                
    else:
        funciones=["e","sen()","cos()","tan()","log()","sqrt()"]
        posicion_cursor=funcion_entry.index(tk.INSERT)
        for fun in range(0,len(funciones)):
            if(funcionVar.get()==funciones[fun]):
                if(funcionVar.get()=="sen()"):
                    funcion_entry.insert(posicion_cursor,"sin()")
                else:
                    funcion_entry.insert(posicion_cursor,funcionVar.get())
                
#? Tablero de Funciones  
Label(root2, text="Funciones", font=('Helvetica', 14, 'bold'), bg="#2F4F4F", fg="white").place(x=640, y=90)

#? Contenedor del tablero de funciones
tablero_funcion = ttk.Frame(root2)
tablero_funcion.place(x=620, y=140)

style = ttk.Style()
style.configure("TRadiobutton", font=("Helvetica", 10), padding=6)

#? Funciones matemáticas como opciones
botones = [
    ("e", "e", 0, 0),
    ("Log()", "log()", 0, 1),
    ("√", "sqrt()", 0, 2),
    ("sen()", "sen()", 1, 0),
    ("cos()", "cos()", 1, 1),
    ("tan()", "tan()", 1, 2)
]

for texto, valor, fila, col in botones:
    ttk.Radiobutton(
        tablero_funcion,
        text=texto,
        value=valor,
        variable=funcionVar,
        command=funciones,
        style="TRadiobutton"
    ).grid(row=fila, column=col, padx=10, pady=5)

#? Botón de calcular
bot = Button(
    root2,
    text="Calcular",
    bg="#4CAF50", fg="white",
    font=('Helvetica', 10, 'bold'),
    width=12, height=2,
    activebackground="#45A049",
    command=lambda: tablero(porcentaje_entry.get(), xl_entry.get(), xu_entry.get())
)
bot.place(x=620, y=240)

#? Botón para limpiar
clear_button = Button(
    root2,
    text="Borrar Datos",
    bg="#f44336", fg="white",
    font=('Helvetica', 10, 'bold'),
    width=12, height=2,
    activebackground="#e53935",
    command=clear_inputs
)
clear_button.place(x=740, y=240)

#? Botón de ayuda (instrucciones)
instrucciones = Button(
    root2,
    text="Instrucciones ",
    bg="#2196F3", fg="white",
    font=('Helvetica', 10, 'bold'),
    width=15, height=2,
    activebackground="#1976D2",
    command=crear_ventana1
)
instrucciones.place(x=620, y=300)

#? creamos tabla para la meustra de los valores
columns = ['Iteración', 'X_L', 'X_R', 'X_U', 'f(X_L)', 'f(X_R)', 'f(X_U)', '|e_a|']
tree = ttk.Treeview(root2, columns=columns, show='headings',height=13)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=110)
tree.place(x=30,y=350)

root2.mainloop()