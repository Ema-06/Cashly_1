import csv
import os
from datetime import datetime
from tkinter import messagebox
from config import ARCHIVO_VENTAS, ARCHIVO_STOCK, DIAS_DE_LA_SEMANA

def registrar_venta(app):
    producto = app.venta_producto.get().strip()
    dia = app.venta_dia.get().strip().lower()
    try:
        cantidad = int(app.venta_cantidad.get())
        ganancia_pct = float(app.venta_porcentaje.get())
    except ValueError:
        return messagebox.showerror("Error", "Cantidad y ganancia deben ser números")

    if not os.path.exists(ARCHIVO_STOCK):
        return messagebox.showerror("Error", "No hay stock registrado")

    stock = {}
    with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            stock[fila[0]] = [int(fila[1]), float(fila[2])]

    if producto not in stock:
        return messagebox.showerror("Error", f"Producto '{producto}' no está en stock")

    if cantidad > stock[producto][0]:
        return messagebox.showwarning("Error de Venta", f"Stock Insuficiente! \n {stock[producto][0]} disponibles")

    costo_unitario = stock[producto][1]
    porcentaje = ganancia_pct / 100
    ganancia_unitaria = costo_unitario * porcentaje
    precio_venta = costo_unitario + ganancia_unitaria
    total_venta = precio_venta * cantidad
    ganancia_total = ganancia_unitaria * cantidad
    fecha = datetime.now()
    if not dia:
        dia = DIAS_DE_LA_SEMANA[fecha.weekday()]

    with open(ARCHIVO_VENTAS, mode="a", newline="", encoding="utf-8") as archivo:
        csv.writer(archivo).writerow([
            fecha.strftime("%Y-%m-%d %H:%M:%S"), dia, producto, cantidad,
            f"{costo_unitario:.2f}", f"{precio_venta:.2f}", f"{total_venta:.2f}", f"{ganancia_total:.2f}"
        ])

    stock[producto][0] -= cantidad
    
    with open(ARCHIVO_STOCK, mode="w", newline="", encoding="utf-8") as archivo:
        for prod, (cant, costo) in stock.items():
            csv.writer(archivo).writerow([prod, cant, f"{costo:.2f}"])

    messagebox.showinfo("Venta con Éxito", f"Venta de {producto} registrada \n Quedan {stock[producto][0]} unidades disponibles")

    # Limpiar campos
    app.venta_producto.delete(0, 'end')
    app.venta_cantidad.delete(0, 'end')
    app.venta_porcentaje.delete(0, 'end')
    app.venta_dia.delete(0, 'end')

    # Mantener ventana visible y activa
    app.ventana_venta.attributes('-topmost', True)
    app.ventana_venta.update()
    app.ventana_venta.attributes('-topmost', False)


    
    
    



   




