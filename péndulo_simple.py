#Importo las librerias
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math as mt

# Esta función hace euler-cromer para resolver el péndulo
def pendulo_simple(t0,tf,w0,h,th0,g,l):
    #declaro las listas
    lx = []
    ly = []
    lt = []
    la = []
    #metodo de euler -cromer
    #mientras el tiempo inicial llegue exactamente al tiempo final
    while t0 <= tf-h:
        #hace las ecuaciones
        w = w0 - h*th0*(g/l)
        th = th0 + h*w  
        x = l*mt.sin(th)
        y=-l*mt.cos(th)
        #guardar los datos en listas
        lx.append(x) 
        ly.append(y)
        lt.append(t0)
        la.append(th)
        #reinciar valores
        t0+=h
        w0 = w
        th0 = th
    return lx,ly,la

#mensaje de inicio
print("""                           
                                    Bienvenido.
Este programa realiza una animación del péndulo simple para el caso ideal y ángulos pequeños.
   Puedes ingresar el valor de la longitud de tu péndulo, el ángulo y tiempo que desees.""")
val1 = 0 # variable para ayudar al condicional
val2 = 0
#valores iniciales
#Para ingresar los valores no hay problema si la longitud cambia de muy grande a muy pequeña, solo si es cero
#sin embargo el programa solicitado requiere de la aproximación que el seno del angulo es igual al angulo
#pero al solo cumplirse en angulos pequeños, pongo un aviso que mostrará al usuario que la simulación solo
#puede ir a angulos pequeños (de aproximadamente -15° a 15°) y el usuario debe decidir si quiere coninuar o no.
while val1 == 0 or val2 == 0: 
    l = float(input("longitud (en metros): "))
    th0_i = float(input("Ingrese el ángulo inicial (en grados): "))
    tf  = float(input("Ingrese el tiempo en el que quiere ver el pendulo (segundos): "))
    if l <= 0 or tf<=0:
        print("\nIngresa un valor válido. La longitud y el tiempo tienen que ser mayores que cero.")
        val2 = 0
    else:
        val2=1
    if th0_i >= 15: 
        print("""
¡Cuidado! Estás ingresando un valor grande para el ángulo y este programa funciona para ángulos pequeños. Puedo mostrarte la animación de cualquier manera pero la animación no funcionará de manera correcta, o puedes cambiar el valor de tu ángulo inicial.""")
        des = input("¿Deseas continuar con el mismo ángulo? Indica 'si' o 'no': ")
        if des == "si" or des == "Si":
            val1 = 1
        elif des == "no" or des == "No":
            val1 = 0
        else:
            print("\ningresa un valor válido.")
    else:
        val1 = 1
        
t0  = 0 # tiempo inicial
m = 1 # masa del objeto (kg)
h = 0.01 #tamaño de paso 
w0 = 0 #despl. angular inicial
g = 9.8 #gravedad (m/s^2)
th0 = th0_i * mt.pi / 180 #convierte los ángulos
n = 10000 #número de iteraciones

# Calcula las posiciones y el angulo llamando a la funcion
posx = pendulo_simple(t0,tf,w0,h,th0,g,l)[0]
posy = pendulo_simple(t0,tf,w0,h,th0,g,l)[1]
ang = pendulo_simple(t0,tf,w0,h,th0,g,l)[2]

# Función para actualizar la animación en cada cuadro
def update(i):
    c,=ax.plot(posx,posy, linestyle="solid",color='black') #grafica la linea
    xy_1,=ax.plot(posx,posy,marker='o',color='black') #grafica el punto
    try:
        c.set_data([0, posx[i]], [0, posy[i]]) #grafica cada punto de la linea 
        xy_1.set_data([posx[i]],[posy[i]]) # = para el punto
        posx_i=str(round(posx[i],3)) #calcula posicion en x, y y el angulo en cada instante para mostrarlo en la gráfica
        posy_i=str(round(posy[i],3))     
        angulo=str(round(ang[i]*180/mt.pi,3))     
    except IndexError: #garantiza que el programa pueda continuar correctamente si llega al total de los datos en la lista
        c.set_data([0, posx[i-1]], [0, posy[i-1]])
        xy_1.set_data([posx[i-1]],[posy[i-1]])
        posx_i=str(round(posx[-1],3)) #guarda la ultima posicion 
        posy_i=str(round(posx[-1],3)) #y en cada uno redondea para mostrar los valores no tan grandes en el texto de la grafica
        angulo=str(round(ang[-1]*180/mt.pi,3))         
        pass    
    time_text.set_text(f'Tiempo: {i * h:.2f} s \n posición en x = {posx_i} m \n posición en y = {posy_i} m \n ángulo = {angulo}°'),
    return (xy_1,)+(c,)+(time_text,)
    
# Aspectos esteticos/ configuracion de la grafica 
fig, ax = plt.subplots() 
ax.set_xlabel("x(m)")  # Nombre del eje x 
ax.set_ylabel("y(m)")  # Nombre del eje y
ax.set_xlim(-l-l/2,l+l/2) #limites de la gráfica
fig.suptitle(f"Péndulo simple ideal a {tf} s") # Titulo de la gráfica
ax.set_ylim(-l-l/2,l+l/2) 
time_text = plt.text(1,0.7, '', transform=ax.transAxes, ha='right', va='top') #cuadro de texto para el tiempo
ax.grid()  #cuadriculas

# Configuración de la animación
ani = FuncAnimation(fig, update,  #esta funcion anima
                    blit=True, interval=0, repeat=False)
plt.show()