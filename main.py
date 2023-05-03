import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 25
REPETICIONES = 0
CONTADOR_LOCAL = 0
temporizador = ""
temporizador_en_marcha = False  # variable de estado del temporizador

def resetear_temporizador():
    global temporizador_en_marcha  # actualiza la variable de estado
    window.after_cancel(temporizador)
    temporizador_en_marcha = False  # restablece la variable de estado a falso
    global REPETICIONES
    REPETICIONES = 0
    # Reiniciar tiempo
    canvas.itemconfig(texto_tiempo, text="00:00")
    # Restablecer texto
    texto_timer.config(text="Timer", fg=GREEN, highlightthickness=0, bg=YELLOW, font=(FONT_NAME, 55, "bold"))
    # Borrar marcas de completado
    texto_checkmark.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def mecanismo_tiempo():
    global REPETICIONES
    global temporizador_en_marcha  # actualiza la variable de estado
    if not temporizador_en_marcha:  # verifica si el temporizador ya está en marcha
        temporizador_en_marcha = True  # establece la variable de estado en verdadero
        REPETICIONES += 1
        segundos_trabajados = WORK_MIN * 60
        descanso_corto = SHORT_BREAK_MIN * 60
        descanso_largo = LONG_BREAK_MIN * 60

        if REPETICIONES % 8 == 0:
            # fijarse que pasa cuando llega al ultimo trabajo antes del descanso largo, repeticion numero 8
            cuenta_regresiva(descanso_largo)
            texto_timer.config(text="Break", fg=RED)

        elif REPETICIONES % 2 == 0:
            # fijarse cuantas repeticiones lleva entre descansos cortos, repeticiones 2, 4, 6
            cuenta_regresiva(descanso_corto)
            texto_timer.config(text="Break", fg=PINK)

        else:
            # fijarse cuantas repeticiones lleva entre trabajo, repeticiones 1, 3, 5, 7
            cuenta_regresiva(segundos_trabajados)
            texto_timer.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# con esta funcion logramos inicializar un contador, cuenta atras cada 1 seg = 1000 milisegundos
def cuenta_regresiva(contador):
    contador_minutos = math.floor(contador / 60)  # resultado de dividir los minutos por 60
    contador_segundos = contador % 60  # resultado de los segundos pasados a enteros con solo 2 unidades de posicion

    if contador_segundos == 0:  # esto es para marcar siempre "00:" en segundos cuando estan en 0 los segundos
        contador_segundos = "0"

    if int(contador_segundos) < 10:
        contador_segundos = f"0{contador_segundos}"

    if contador_minutos < 10:
        contador_minutos = f"0{contador_minutos}"

    canvas.itemconfig(texto_tiempo, text=f"{contador_minutos}:{contador_segundos}")
    if contador > 0:
        global temporizador
        temporizador = window.after(1000, cuenta_regresiva, contador - 1)

    else:
        mecanismo_tiempo()
        if REPETICIONES % 2 == 0:
            global CONTADOR_LOCAL
            CONTADOR_LOCAL += 1
            texto_checkmark.config(text="✔" * CONTADOR_LOCAL)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=100, bg=YELLOW)  # Bg = Background color

# Tamaño de la ventana a crear, usaremos el tamaño de la imagen, highlight... es para la linea de limite de la imagen
canvas = Canvas(width=250, height=254, bg=YELLOW, highlightthickness=0)
imagen_tomate = PhotoImage(file="tomato.png")  # Con PhotoImage vamos a ubicar el archivo/foto a usar
canvas.create_image(120, 120, image=imagen_tomate)  # Ubicar la imagen en el centro.
canvas.grid(column=1, row=1, padx=5, pady=5)

# En canvas.create_text vamos a poder modificar datos del texto. Tamaño, ubicacion, color, etc.
texto_tiempo = canvas.create_text(125, 140, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1, padx=5, pady=5)  # Ya empaquetamos nuestro lienzo para mostrarlo

# Texto Timer
texto_timer = Label(text="Timer", fg=GREEN, highlightthickness=0, bg=YELLOW, font=(FONT_NAME, 55, "bold"))
texto_timer.grid(column=1, row=0, padx=5, pady=5)

# Boton Start


boton = Button(text="Start", command=mecanismo_tiempo, height=2, width=15)
boton.grid(column=0, row=2, padx=5, pady=5)

# Boton Reset

boton = Button(text="Reset", command=resetear_temporizador, height=2, width=15)
boton.grid(column=2, row=2, padx=5, pady=5)

# Texto CheckMarck
texto_checkmark = Label(fg=GREEN, highlightthickness=0, bg=YELLOW, font=(FONT_NAME, 24, "bold"))
texto_checkmark.grid(column=1, row=3, padx=5, pady=5)

window.mainloop()
