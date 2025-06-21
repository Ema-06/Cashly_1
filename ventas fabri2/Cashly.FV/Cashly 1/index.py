import tkinter as tk
from tkinter import messagebox, simpledialog
from container_ventas import ventana_venta
from container_stock import ventana_stock
from container_ganancias import ventana_ganancias
from PIL import Image, ImageTk


# Validación de usuario
def validar_usuario():
    usuario = simpledialog.askstring("Validación", "Ingrese su Usuario:")
    if usuario is None or usuario.strip().lower() ==[]:
        messagebox.showerror("Error", "Usuario incorrecto. Finalizando el programa.")
        root.destroy()
    else:
        messagebox.showinfo(f"Bienvenido {usuario}", "Bienvenido a Cashly, el registro de ventas más fácil y rápido.\n\n¡No olvides ingresar stock si recién comienzas!")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cashly 1.0 - Menú Principal")
        self.root.resizable(False, False)
        self.root.geometry("800x400+380+150")
        self.root.configure(bg="#ffffff")  # color de fondo
        

        self.menu_frame = tk.Frame(root, bg="#ffffff")
        self.menu_frame.pack(side="right", padx=30, pady=20)

    

        # BOTONES DEL MENU  
        btn_ventas = tk.Button(self.menu_frame, text="Ventas", width=20, height=2,
                               bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                               command=lambda: ventana_venta(self))
        btn_ventas.pack(pady=10)


        # BOTON STOCK

        btn_stock = tk.Button(self.menu_frame, text="Stock", width=20, height=2,
                              bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                              command=lambda: ventana_stock(self))
        btn_stock.pack(pady=10)


        #BOTON GANANCIA
        
        btn_ganancias = tk.Button(self.menu_frame, text="Ganancias", width=20, height=2,
                                  bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                                  command=lambda: ventana_ganancias(self))
        btn_ganancias.pack(pady=10)


        #LOGO -- CASHLY
        self.logo_image = Image.open("imagenes/Cashly.png.jpeg")
        self.logo_image = self.logo_image.resize((500,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(root, image=self.logo_image)
        self.logo_label.place(x=30, y=100)

        # COPYRIGHT     
        copyright_label= tk.Label(root, text="© 2025 Cashly Code. Todos los derechos reservados", font= "Arial 10 bold", bg="white", fg="black")
        copyright_label.place(x=180, y=350)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    validar_usuario()
    root.mainloop()
