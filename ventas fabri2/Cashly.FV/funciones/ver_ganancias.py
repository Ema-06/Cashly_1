import csv
import os
from config import ARCHIVO_VENTAS

def ver_registro(app):
    total = 0.0
    for i in app.tree_ventas.get_children():
        app.tree_ventas.delete(i)
    if not os.path.exists(ARCHIVO_VENTAS):
        return
    with open(ARCHIVO_VENTAS, mode="r", encoding="utf-8") as archivo:
        for fila in csv.reader(archivo):
            app.tree_ventas.insert("", "end", values=fila)
            try:
                total += float(fila[6])
            except:
                pass
    app.label_total.config(text=f"Ganancia Total: ${total:.2f}")
