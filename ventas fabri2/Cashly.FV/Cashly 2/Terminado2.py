import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# Archivos
ARCHIVO_VENTAS = "ganancias_del_local.csv"
ARCHIVO_COMPRAS = "compras_del_local.csv"
ARCHIVO_STOCK = "stock.csv"

DIAS_DE_LA_SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

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
        ttk.Button(frame, text="Registrar Venta", command=self.registrar_venta).grid(row=4, column=1, pady=10)

    def registrar_venta(self):
        producto = self.venta_producto.get().strip()
        dia = self.venta_dia.get().strip().lower()
        try:
            cantidad = int(self.venta_cantidad.get())
            ganancia_pct = float(self.venta_porcentaje.get())
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
            return messagebox.showwarning("Stock insuficiente", f"Sólo hay {stock[producto][0]} disponibles")

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
            escritor = csv.writer(archivo)
            escritor.writerow([
                fecha.strftime("%Y-%m-%d %H:%M:%S"), dia, producto, cantidad,
                f"{costo_unitario:.2f}", f"{precio_venta:.2f}", f"{total_venta:.2f}", f"{ganancia_total:.2f}"
            ])

        stock[producto][0] -= cantidad
        with open(ARCHIVO_STOCK, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            for prod, (cant, costo) in stock.items():
                escritor.writerow([prod, cant, f"{costo:.2f}"])

        messagebox.showinfo("Éxito", f"Venta de {producto} registrada")

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
        ttk.Button(frame, text="Registrar Compra", command=self.registrar_compra).grid(row=3, column=1, pady=10)

    def registrar_compra(self):
        producto = self.compra_producto.get().strip()
        try:
            cantidad = int(self.compra_cantidad.get())
            costo_unitario = float(self.compra_costo.get())
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

    def build_stock_tab(self):
        frame = self.tabs["Ver Stock"]
        self.tree_stock = ttk.Treeview(frame, columns=("Producto", "Cantidad", "Costo"), show="headings")
        for col in self.tree_stock["columns"]:
            self.tree_stock.heading(col, text=col)
        self.tree_stock.pack(fill="both", expand=True)
        ttk.Button(frame, text="Actualizar Stock", command=self.ver_stock).pack(pady=10)

    def ver_stock(self):
        for i in self.tree_stock.get_children():
            self.tree_stock.delete(i)
        if not os.path.exists(ARCHIVO_STOCK):
            return
        with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
            for fila in csv.reader(archivo):
                self.tree_stock.insert("", "end", values=fila)

    def build_ganancias_tab(self):
        frame = self.tabs["Ver Ganancias"]
        self.tree_ventas = ttk.Treeview(frame, columns=("Fecha", "Día", "Producto", "Cantidad", "Costo", "Precio", "Total", "Ganancia"), show="headings")
        for col in self.tree_ventas["columns"]:
            self.tree_ventas.heading(col, text=col)
        self.tree_ventas.pack(fill="both", expand=True)
        ttk.Button(frame, text="Ver Ventas", command=self.ver_registro).pack(pady=10)
        self.label_total = ttk.Label(frame, text="Ganancia Total: $0.00", font=('Arial', 12, 'bold'))
        self.label_total.pack()

    def ver_registro(self):
        total = 0.0
        for i in self.tree_ventas.get_children():
            self.tree_ventas.delete(i)
        if not os.path.exists(ARCHIVO_VENTAS):
            return
        with open(ARCHIVO_VENTAS, mode="r", encoding="utf-8") as archivo:
            for fila in csv.reader(archivo):
                self.tree_ventas.insert("", "end", values=fila)
                try:
                    total += float(fila[6])
                except:
                    pass
        self.label_total.config(text=f"Ganancia Total: ${total:.2f}")

if __name__ == "__main__":
    app = CashlyApp()
    app.mainloop()