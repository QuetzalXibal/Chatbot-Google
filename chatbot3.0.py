import random
import tkinter as tk
import json
import os
from googleapiclient.discovery import build

API_KEY = "AIzaSyCrnO4aDB-4kiM79znil_ViQWQdawV0TXQ"
SEARCH_ENGINE_ID = "80c3fb2c6322b4772"

RESPUESTAS = {}

def aprender(clave):
    palabras = clave.split()
    for palabra in palabras:
        if palabra not in RESPUESTAS:
            RESPUESTAS[palabra] = []

def google_search(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    items = result.get("items", [])
    if items:
        return items[0]["snippet"]
    else:
        return "Lo siento, no encontré información relevante."

def dividir_respuesta(respuesta, longitud_linea=125):
    palabras = respuesta.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        if len(linea_actual + palabra) <= longitud_linea:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    lineas.append(linea_actual.strip())
    return lineas

def enviar_mensaje(event=None):
    mensaje_usuario = campo_texto.get()
    campo_texto.delete(0, tk.END)

    if mensaje_usuario.lower().startswith("quiero que aprendas"):
        aprender(mensaje_usuario[len("quiero que aprendas"):].strip())
        respuesta = "He aprendido algo nuevo y lo he guardado."
    else:
        respuesta = google_search(mensaje_usuario)

    chat.configure(state="normal")
    chat.insert(tk.END, f"Usuario: {mensaje_usuario}\n", "usuario")
    respuesta_lineas = dividir_respuesta(respuesta)
    for linea in respuesta_lineas:
        chat.insert(tk.END, f"ChatBot: {linea}\n", "chatbot")
    chat.configure(state="disabled")
    chat.yview(tk.END)

def mensaje_bienvenida():
    mensaje = "Hola, soy un chatbot para buscar información en Google."
    chat.insert(tk.END, f"ChatBot: {mensaje}\n")
    chat.yview(tk.END)

def cambiar_tema(tema):
    if tema == 'oscuro':
        chat.config(bg="#2c2c2c", fg="#ffffff")
        campo_texto.config(bg="#2c2c2c", fg="#ffffff", insertbackground="white")
        ventana.config(bg="#2c2c2c")
    elif tema == 'claro':
        chat.config(bg="#ffffff", fg="#000000")
        campo_texto.config(bg="#ffffff", fg="#000000", insertbackground="black")
        ventana.config(bg="#ffffff")

def ventana_opacidad():
    def ajustar_opacidad(opacidad):
        ventana.attributes("-alpha", float(opacidad))

    top = tk.Toplevel(ventana)
    top.title("Ajustar opacidad")
    top.geometry("250x100")
    scale = tk.Scale(top, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=ajustar_opacidad)
    scale.set(ventana.attributes("-alpha"))
    scale.pack(expand=True, fill=tk.BOTH)

ventana = tk.Tk()
ventana.title("ChatBot")
ventana.iconbitmap("C:/Users/Aleja/OneDrive/Programacion/Python/Fansite.ico")


# Crear el menú y las opciones de tema y opacidad
menu = tk.Menu(ventana)
ventana.config(menu=menu)

opciones_menu = tk.Menu(menu)
menu.add_cascade(label="Opciones", menu=opciones_menu)
opciones_menu.add_command(label="Tema oscuro", command=lambda: cambiar_tema('oscuro'))
opciones_menu.add_command(label="Tema claro", command=lambda: cambiar_tema('claro'))
opciones_menu.add_command(label="Ajustar opacidad", command=ventana_opacidad)

marco_chat = tk.Frame(ventana)
scrollbar_y = tk.Scrollbar(marco_chat)
scrollbar_x = tk.Scrollbar(marco_chat, orient=tk.HORIZONTAL)
chat = tk.Text(marco_chat, height=30, width=120, wrap=tk.WORD, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
chat.pack(side=tk.LEFT, fill=tk.BOTH)
chat.pack()
marco_chat.pack()

# Establecer colores fosforescentes para el usuario y el chatbot
chat.tag_configure("usuario", foreground="#00ff00")


campo_texto = tk.Entry(ventana)
campo_texto.bind("<Return>", enviar_mensaje)
campo_texto.pack()

boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack()

mensaje_bienvenida()

ventana.mainloop()
