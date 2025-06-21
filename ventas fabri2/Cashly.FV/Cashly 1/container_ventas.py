import csv
import os
from tkinter import Toplevel, Label, Entry, Button
from tkinter import ttk
from config import ARCHIVO_STOCK
from ventas import *


def ventana_venta(app):
    app.ventana_venta = Toplevel(app.root)
    app.ventana_venta.title("Registrar Venta")
    app.ventana_venta.geometry("400x300+500+200")
    app.ventana_venta.configure(bg="#f5f5f5")
    app.ventana_venta.lift()

    Label(app.ventana_venta, text="Producto:", bg="#f5f5f5").pack()
    
    # Combobox para seleccionar producto desde stock
    productos = []
    if os.path.exists(ARCHIVO_STOCK):
        with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
            reader = csv.reader(archivo)
            productos = [fila[0] for fila in reader]
    
    app.venta_producto = ttk.Combobox(app.ventana_venta, values=productos, state="readonly")
    app.venta_producto.pack()

    Label(app.ventana_venta, text="Cantidad:", bg="#f5f5f5").pack()
    app.venta_cantidad = Entry(app.ventana_venta)
    app.venta_cantidad.pack()

    

    Label(app.ventana_venta, text="Día (opcional):", bg="#f5f5f5").pack()
    app.venta_dia = Entry(app.ventana_venta)
    app.venta_dia.pack()

    

    app.ventana_venta.attributes('-topmost', True)
    app.ventana_venta.update()
    app.ventana_venta.attributes('-topmost', False)

    Button(app.ventana_venta, text="Registrar", bg="#4CAF50", fg="white", command=lambda: registrar_venta(app)).pack(pady=10)
    Button(app.ventana_venta, text="Volver al menú", bg="#067CB3", fg="white", command=app.ventana_venta.destroy).pack()
