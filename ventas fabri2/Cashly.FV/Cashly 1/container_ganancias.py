import tkinter as tk
from tkinter import ttk, Button
from ganancias import ver_ganancias
from graficos import graficar_ganancias

def ventana_ganancias(app):
    app.ventana_ganancias = tk.Toplevel(app.root)
    app.ventana_ganancias.title("Ver Ganancias")
    app.ventana_ganancias.resizable(True, True)
    app.ventana_ganancias.geometry("900x400+280+150")
    app.ventana_ganancias.lift()
    app.ventana_ganancias.focus_force()

    # Tabla
    tree = ttk.Treeview(app.ventana_ganancias, columns=("Fecha", "Día", "Producto", "Cantidad", "Costo", "Precio", "Total", "Ganancia"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.column("Fecha", width=120)
    tree.column("Día", width=80)
    tree.column("Producto", width=150)

    tree.pack(fill="both", expand=True)

    app.tree_ventas = tree

    # Total
    app.label_total = ttk.Label(app.ventana_ganancias, text="Ganancia Total: $0.00", font=('Arial', 12, 'bold'))
    app.label_total.pack(pady=10)

    # Botones
    Button(app.ventana_ganancias, text="Ver Ventas", bg="#4CAF50", fg="white", command=lambda: ver_ganancias(app)).pack(pady=5)
    Button(app.ventana_ganancias, text="Volver al menú", bg="#067CB3", fg="white", command=app.ventana_ganancias.destroy).pack(pady=5)
    Button(app.ventana_ganancias, text="Ver Gráfica", bg="#A17E08", fg="white", command=graficar_ganancias).pack(pady=5)
