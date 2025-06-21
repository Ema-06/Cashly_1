import csv
import os
from datetime import datetime
from tkinter import messagebox
from config import ARCHIVO_COMPRAS, ARCHIVO_STOCK

def registrar_compra(app):
    producto = app.compra_producto.get().strip()
    try:
        cantidad = int(app.compra_cantidad.get())
        costo_unitario = float(app.compra_costo.get())
    except ValueError:
        return messagebox.showerror("Error", "Cantidad y costo deben ser números")

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_COMPRAS, mode="a", newline="", encoding="utf-8") as archivo:
        csv.writer(archivo).writerow([fecha, producto, cantidad, f"{costo_unitario:.2f}"])

    stock = {}
    if os.path.exists(ARCHIVO_STOCK):
        with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
            for fila in csv.reader(archivo):
                stock[fila[0]] = [int(fila[1]), float(fila[2])]
    if producto in stock:
        stock[producto][0] += cantidad
        stock[producto][1] = costo_unitario
    else:
        stock[producto] = [cantidad, costo_unitario]

    with open(ARCHIVO_STOCK, mode="w", newline="", encoding="utf-8") as archivo:
        for prod, (cant, costo) in stock.items():
            csv.writer(archivo).writerow([prod, cant, f"{costo:.2f}"])

    messagebox.showinfo("Éxito", f"Compra de {producto} registrada")

    # Limpiar campos
    app.compra_producto.delete(0, 'end')
    app.compra_cantidad.delete(0, 'end')
    app.compra_costo.delete(0, 'end')

    app.ventana_compra.attributes('-topmost', True)
    app.ventana_compra.update()
    app.ventana_compra.attributes('-topmost', False)

def ver_stock(app):
    for i in app.tree_stock.get_children():
        app.tree_stock.delete(i)
    if not os.path.exists(ARCHIVO_STOCK):
        return
    with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
        for fila in csv.reader(archivo):
            app.tree_stock.insert("", "end", values=fila)
