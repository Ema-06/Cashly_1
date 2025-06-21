import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv
import os


DIAS_DE_LA_SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
ARCHIVO_VENTAS = "ganancias_del_local.csv"
ARCHIVO_COMPRAS = "compras_del_local.csv"
ARCHIVO_STOCK = "stock.csv"

# Validación de usuario
def validar_usuario():
    usuario = simpledialog.askstring("Validación", "Ingrese el nombre de su emprendimiento o negocio:")
    if usuario is None or usuario.strip().lower() != "cashly":
        messagebox.showerror("Error", "Usuario incorrecto. Finalizando el programa.")
        root.destroy()
    else:
        messagebox.showinfo("Bienvenido", "Bienvenido a Cashly, el registro de ventas más fácil y rápido.\n\n¡No olvides ingresar stock si recién comienzas!")

# Registrar Compra
def registrar_compra():
    try:
        producto = simpledialog.askstring("Compra", "Producto comprado:").strip()
        cantidad = int(simpledialog.askstring("Compra", "Cantidad comprada:"))
        costo_unitario = float(simpledialog.askstring("Compra", "Costo por unidad ($):"))
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar en compras
        with open(ARCHIVO_COMPRAS, mode="a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([fecha, producto, cantidad, f"{costo_unitario:.2f}"])

        # Actualizar stock
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

        messagebox.showinfo("Compra registrada", f"Se registró: {producto} x{cantidad} a ${costo_unitario:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Registrar Venta
def registrar_venta():
    try:
        producto = simpledialog.askstring("Venta", "Producto vendido:").strip()
        cantidad = int(simpledialog.askstring("Venta", "Cantidad vendida:"))

        # Leer stock
        stock = {}
        if os.path.exists(ARCHIVO_STOCK):
            with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
                for fila in csv.reader(archivo):
                    stock[fila[0]] = [int(fila[1]), float(fila[2])]

        if producto not in stock:
            messagebox.showwarning("Error", f"El producto '{producto}' no está en stock.")
            return

        stock_actual, costo_unitario = stock[producto]
        if cantidad > stock_actual:
            messagebox.showwarning("Error", f"Stock insuficiente. Disponible: {stock_actual}")
            return

        ganancia_pct = float(simpledialog.askstring("Venta", "Porcentaje de ganancia (ej: 30 para 30%):"))
        porcentaje = ganancia_pct / 100
        ganancia_unitaria = costo_unitario * porcentaje
        precio_venta = costo_unitario + ganancia_unitaria
        total_venta = precio_venta * cantidad
        ganancia_total = ganancia_unitaria * cantidad

        fecha = datetime.now()
        dia = simpledialog.askstring("Venta", "Día de la semana (dejar vacío para hoy):")
        dia = dia.strip().lower() if dia else DIAS_DE_LA_SEMANA[fecha.weekday()]
        if dia not in DIAS_DE_LA_SEMANA:
            messagebox.showerror("Error", "Día inválido. Usa: lunes, martes, etc.")
            return

        with open(ARCHIVO_VENTAS, mode="a", newline="", encoding="utf-8") as archivo:
            csv.writer(archivo).writerow([
                fecha.strftime("%Y-%m-%d %H:%M:%S"), dia, producto, cantidad,
                f"{costo_unitario:.2f}", f"{precio_venta:.2f}",
                f"{total_venta:.2f}", f"{ganancia_total:.2f}"
            ])

        stock[producto][0] -= cantidad
        with open(ARCHIVO_STOCK, mode="w", newline="", encoding="utf-8") as archivo:
            for prod, (cant, costo) in stock.items():
                csv.writer(archivo).writerow([prod, cant, f"{costo:.2f}"])

        messagebox.showinfo("Venta registrada", f"Venta: {producto} x{cantidad} = ${total_venta:.2f}\nGanancia: ${ganancia_total:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Ver Stock
def ver_stock():
    texto = ""
    if not os.path.exists(ARCHIVO_STOCK):
        texto = "No hay stock registrado aún."
    else:
        with open(ARCHIVO_STOCK, mode="r", encoding="utf-8") as archivo:
            for fila in csv.reader(archivo):
                texto += f"{fila[0]} | Cantidad: {fila[1]} | Costo: ${fila[2]}\n"
    messagebox.showinfo("Stock Actual", texto)

# Ver Ventas
def mostrar_registro():
    total_general = 0.0
    texto = ""
    try:
        with open(ARCHIVO_VENTAS, mode="r", encoding="utf-8") as archivo:
            for fila in csv.reader(archivo):
                texto += " | ".join(fila) + "\n"
                try:
                    total_general += float(fila[6])
                except:
                    continue
    except FileNotFoundError:
        texto = "No hay ventas registradas."
    texto += f"\nGANANCIA TOTAL: ${total_general:.2f}"
    messagebox.showinfo("Registro de Ventas", texto)

# Crear ventana principal
root = tk.Tk()
root.title("Cashly - Registro de Ventas")
root.geometry("400x400")

tk.Label(root, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Registrar Venta", width=30, command=registrar_venta).pack(pady=5)
tk.Button(root, text="Ver Registro de Ganancias", width=30, command=mostrar_registro).pack(pady=5)
tk.Button(root, text="Registrar Compra", width=30, command=registrar_compra).pack(pady=5)
tk.Button(root, text="Ver Stock Actual", width=30, command=ver_stock).pack(pady=5)
tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=20)

validar_usuario()
root.mainloop()