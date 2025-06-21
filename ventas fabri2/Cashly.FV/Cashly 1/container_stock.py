import tkinter as tk
from tkinter import ttk, messagebox, Label, Entry
from inventario import registrar_compra, ver_stock
import csv
import os
from config import ARCHIVO_STOCK

def ventana_stock(app):
    app.ventana_stock = tk.Toplevel(app.root)
    app.ventana_stock.title("Gestión de Stock")
    app.ventana_stock.geometry("300x180+620+250")

    app.ventana_stock.attributes('-topmost', True)
    app.ventana_stock.update()
    app.ventana_stock.attributes('-topmost', False)

    tk.Button(app.ventana_stock, text="Registrar Compra", bg="#4CAF50", fg="white",
              command=lambda: ventana_registrar_compra(app)).pack(pady=10)

    tk.Button(app.ventana_stock, text="Ver Stock", bg="#A17E08", fg="white",
              command=lambda: ventana_ver_stock(app)).pack(pady=10)

    tk.Button(app.ventana_stock, text="Volver al menú", bg="#067CB3", fg="white",
              command=app.ventana_stock.destroy).pack(pady=10)


def ventana_registrar_compra(app):
    app.ventana_compra = tk.Toplevel(app.root)
    app.ventana_compra.title("Registrar Compra")
    app.ventana_compra.geometry("400x250+520+220")
    app.ventana_compra.lift()
    app.ventana_compra.focus_force()

    Label(app.ventana_compra, text="Producto:").pack()
    app.compra_producto = tk.Entry(app.ventana_compra)
    app.compra_producto.pack()

    Label(app.ventana_compra, text="Cantidad:").pack()
    app.compra_cantidad = tk.Entry(app.ventana_compra)
    app.compra_cantidad.pack()

    Label(app.ventana_compra, text="Costo unitario:").pack()
    app.compra_costo = tk.Entry(app.ventana_compra)
    app.compra_costo.pack()

    Label(app.ventana_compra, text="Ganancia (%):", bg="#f5f5f5").pack()
    app.venta_porcentaje = Entry(app.ventana_compra)
    app.venta_porcentaje.pack()

    def registrar_y_levantar():
        registrar_compra(app)
        # Mantener ventana al frente tras registrar
        app.ventana_compra.attributes('-topmost', True)
        app.ventana_compra.update()
        app.ventana_compra.attributes('-topmost', False)

    tk.Button(app.ventana_compra, text="Registrar", bg="#4CAF50", fg="white", command=registrar_y_levantar).pack(pady=10)
    tk.Button(app.ventana_compra, text="Volver", bg="#067CB3", fg="white", command=app.ventana_compra.destroy).pack(pady=5)


def ventana_ver_stock(app):
    app.ventana_ver_stock = tk.Toplevel(app.root)
    app.ventana_ver_stock.title("Stock Actual")
    app.ventana_ver_stock.geometry("500x360+420+180")
    app.ventana_ver_stock.lift()
    app.ventana_ver_stock.focus_force()

    columns = ("Producto", "Cantidad", "Costo Unitario")
    tree = ttk.Treeview(app.ventana_ver_stock, columns=columns, show="headings", selectmode="browse")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    app.tree_stock = tree
    ver_stock(app)

    def eliminar_producto():
        selected = tree.selection()
        if not selected:
            return messagebox.showwarning("Atención", "Seleccioná un producto para eliminar.")
        valores = tree.item(selected[0], 'values')
        producto_a_eliminar = valores[0]

        if not os.path.exists(ARCHIVO_STOCK):
            return

        filas_actualizadas = []
        with open(ARCHIVO_STOCK, "r", encoding="utf-8") as f:
            for fila in csv.reader(f):
                if fila[0] != producto_a_eliminar:
                    filas_actualizadas.append(fila)

        with open(ARCHIVO_STOCK, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(filas_actualizadas)

        ver_stock(app)
        messagebox.showinfo("Eliminado", f"Producto '{producto_a_eliminar}' eliminado del stock.")

        # Mantener ventana al frente tras eliminar
        app.ventana_ver_stock.attributes('-topmost', True)
        app.ventana_ver_stock.update()
        app.ventana_ver_stock.attributes('-topmost', False)

    tk.Button(app.ventana_ver_stock, text="Eliminar producto", bg="#D9534F", fg="white", command=eliminar_producto).pack(pady=5)
    tk.Button(app.ventana_ver_stock, text="Volver", bg="#067CB3", fg="white", command=app.ventana_ver_stock.destroy).pack(pady=5)
