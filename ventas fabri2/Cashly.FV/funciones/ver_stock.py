import csv
import os
from config import ARCHIVO_STOCK

def ver_stock(app):
    for i in app.tree_stock.get_children():
        app.tree_stock.delete(i)
    if not os.path.exists(ARCHIVO_STOCK):
        return
    with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
        for fila in csv.reader(archivo):
            app.tree_stock.insert("", "end", values=fila)
