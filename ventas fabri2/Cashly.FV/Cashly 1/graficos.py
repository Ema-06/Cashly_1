import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from config import ARCHIVO_VENTAS

def graficar_ganancias():
    if not os.path.exists(ARCHIVO_VENTAS):
        return

    ganancias_semanal = defaultdict(float)
    ganancias_mensual = defaultdict(float)
    ganancias_anual = defaultdict(float)
    productos_semanal = Counter()
    productos_mensual = Counter()

    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_mes = datetime(hoy.year, hoy.month, 1)

    with open(ARCHIVO_VENTAS, newline='', encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            try:
                fecha = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S")
                dia = fecha.strftime("%A")  # Lunes, Martes...
                mes = fecha.strftime("%B")  # Enero, Febrero...
                anio = fecha.year
                ganancia = float(fila[7])
                producto = fila[2]
            except:
                continue

            # Acumular por semana, mes, año
            if fecha >= inicio_semana:
                ganancias_semanal[dia] += ganancia
                productos_semanal[producto] += int(fila[3])
            if fecha >= inicio_mes:
                productos_mensual[producto] += int(fila[3])
                ganancias_mensual[mes] += ganancia
            ganancias_anual[anio] += ganancia

    # Ordenar días de la semana
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    datos_semanal = [ganancias_semanal[dia] for dia in orden_dias]

    # --- Mostrar gráficas ---
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Análisis de Ganancias", fontsize=16)

    # Gráfico semanal
    axs[0, 0].bar(orden_dias, datos_semanal, color="skyblue")
    axs[0, 0].set_title("Ganancias por Día (Última Semana)")
    axs[0, 0].tick_params(axis='x', rotation=45)

    # Gráfico mensual
    meses = list(ganancias_mensual.keys())
    valores_mes = list(ganancias_mensual.values())
    axs[0, 1].bar(meses, valores_mes, color="orange")
    axs[0, 1].set_title("Ganancias Mensuales")
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Gráfico anual
    anios = list(map(str, ganancias_anual.keys()))
    valores_anio = list(ganancias_anual.values())
    axs[1, 0].bar(anios, valores_anio, color="green")
    axs[1, 0].set_title("Ganancias por Año")
    axs[1, 0].tick_params(axis='x', rotation=0)

    # Productos más vendidos
    mas_vendido_semana = productos_semanal.most_common(1)[0] if productos_semanal else ("Ninguno", 0)
    mas_vendido_mes = productos_mensual.most_common(1)[0] if productos_mensual else ("Ninguno", 0)

    texto = f"Más vendido esta semana: {mas_vendido_semana[0]} ({mas_vendido_semana[1]})\n" \
            f"Más vendido este mes: {mas_vendido_mes[0]} ({mas_vendido_mes[1]})"
    axs[1, 1].axis('off')
    axs[1, 1].text(0.1, 0.5, texto, fontsize=12, va="center")

    plt.tight_layout()
    plt.show()
