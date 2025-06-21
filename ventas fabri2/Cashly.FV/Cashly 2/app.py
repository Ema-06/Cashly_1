# cashly/app.py
import tkinter as tk
from tkinter import ttk
from registrar_venta import registrar_venta
from registrar_compra import registrar_compra
from ver_stock import ver_stock
from ver_ganancias import ver_registro

class CashlyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cashly - Registro de Ventas")
        self.geometry("850x550")
        self.configure(bg="#f804cf")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=('Arial', 12, 'bold'), padding=[10, 10])
        style.configure("TButton", font=('Arial', 11), background="#2a9d8f", foreground="white")
        style.map("TButton", background=[("active", "#33fa97")])
        style.configure("Treeview", font=('Arial', 10))
        style.configure("TLabel", font=('Arial', 11))

        self.notebook = ttk.Notebook(self)
        self.tabs = {}
        for name in ["Registrar Venta", "Registrar Compra", "Ver Stock", "Ver Ganancias"]:
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=name)
            self.tabs[name] = frame
        self.notebook.pack(expand=1, fill="both")

        self.build_venta_tab()
        self.build_compra_tab()
        self.build_stock_tab()
        self.build_ganancias_tab()

    def build_venta_tab(self):
        frame = self.tabs["Registrar Venta"]

        self.venta_producto = ttk.Entry(frame, width=30)
        self.venta_cantidad = ttk.Entry(frame, width=10)
        self.venta_porcentaje = ttk.Entry(frame, width=10)
        self.venta_dia = ttk.Entry(frame, width=15)

        ttk.Label(frame, text="Producto:").grid(row=0, column=0, sticky="e")
        self.venta_producto.grid(row=0, column=1)
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky="e")
        self.venta_cantidad.grid(row=1, column=1)
        ttk.Label(frame, text="Ganancia %:").grid(row=2, column=0, sticky="e")
        self.venta_porcentaje.grid(row=2, column=1)
        ttk.Label(frame, text="Día (opcional):").grid(row=3, column=0, sticky="e")
        self.venta_dia.grid(row=3, column=1)
        ttk.Button(frame, text="Registrar Venta", command=lambda: registrar_venta(self)).grid(row=4, column=1, pady=10)

    def build_compra_tab(self):
        frame = self.tabs["Registrar Compra"]

        self.compra_producto = ttk.Entry(frame, width=30)
        self.compra_cantidad = ttk.Entry(frame, width=10)
        self.compra_costo = ttk.Entry(frame, width=10)

        ttk.Label(frame, text="Producto:").grid(row=0, column=0, sticky="e")
        self.compra_producto.grid(row=0, column=1)
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky="e")
        self.compra_cantidad.grid(row=1, column=1)
        ttk.Label(frame, text="Costo unitario $:").grid(row=2, column=0, sticky="e")
        self.compra_costo.grid(row=2, column=1)
        ttk.Button(frame, text="Registrar Compra", command=lambda: registrar_compra(self)).grid(row=3, column=1, pady=10)

    def build_stock_tab(self):
        frame = self.tabs["Ver Stock"]
        self.tree_stock = ttk.Treeview(frame, columns=("Producto", "Cantidad", "Costo"), show="headings")
        for col in self.tree_stock["columns"]:
            self.tree_stock.heading(col, text=col)
        self.tree_stock.pack(fill="both", expand=True)
        ttk.Button(frame, text="Actualizar Stock", command=lambda: ver_stock(self)).pack(pady=10)

    def build_ganancias_tab(self):
        frame = self.tabs["Ver Ganancias"]
        self.tree_ventas = ttk.Treeview(frame, columns=("Fecha", "Día", "Producto", "Cantidad", "Costo", "Precio", "Total", "Ganancia"), show="headings")
        for col in self.tree_ventas["columns"]:
            self.tree_ventas.heading(col, text=col)
        self.tree_ventas.pack(fill="both", expand=True)
        ttk.Button(frame, text="Ver Ventas", command=lambda: ver_registro(self)).pack(pady=10)
        self.label_total = ttk.Label(frame, text="Ganancia Total: $0.00", font=('Arial', 12, 'bold'))
        self.label_total.pack()

if __name__ == "__main__":
    app = CashlyApp()
    app.mainloop()

