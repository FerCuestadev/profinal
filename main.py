import os
import plotly.express as px
import pandas as pd
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')



@app.route("/cargarfuentedatos")
def cargarfuentedatos():
    with open("datos.csv", "r") as archivo:   # Abrir el archivo y preparar variables
        mitabla = "<table id='t_datos' class='table table-hover'>"
        mitabla += "<thead>"
        mitabla += "    <tr>"
        mitabla += "        <th>País</th>"
        mitabla += "        <th>Código</th>"
        mitabla += "        <th>Año</th>"
        mitabla += "        <th>Ahorro</th>"
        mitabla += "    </tr>"
        mitabla += "</thead>"
        mitabla += "<tbody>"
        paises = set()  # Usaremos un conjunto para evitar duplicados
        for linea in archivo:  # Leer línea por línea el archivo
            elemento = linea.split(",")  # Eliminar espacios y dividir por comas
            paises.add(elemento[0])  # Agregar país al conjunto
            mitabla += "<tr>"
            mitabla += "    <td>" + elemento[0] + "</td>"
            mitabla += "    <td>" + elemento[1] + "</td>"
            mitabla += "    <td>" + elemento[2] + "</td>"
            mitabla += "    <td>" + elemento[3] + "</td>"
            mitabla += "</tr>"
        mitabla += "</tbody></table>"


# Crear el <select> para los países únicos
    select_paises = "<select id='sl_paises' class='form-control'>"
    for pais in paises:  # Ordenar los países alfabéticamente
        select_paises =select_paises+ "<option value='" + pais + "'>" + pais + "</option>"
    select_paises =select_paises+ "</select>"
    
    select_grafico = "<select id='sl_grafico' class='form-control'>"
    select_grafico =select_grafico+ "<option value='Linea'>Linea</option>"
    select_grafico =select_grafico+ "<option value='Torta'>Torta</option>"
    select_grafico =select_grafico+ "<option value='Barras'>Barras</option>"
    select_grafico =select_grafico+ "<option value='Area'>Area</option>"
    select_grafico =select_grafico+ "</select>"
    
    todo="<div class='row'>"
    todo=todo+"<div class='col-md-7'>"+select_paises+"</div>"
    todo=todo+"<div class='col-md-3'>"+select_grafico+"</div>"
    todo=todo+"<div class='col-md-2'><button onclick='mostrarGrafico()' class='btn btn-success'>Graficar</button></div>"
    todo=todo+"</div>"

    return todo +"<hr>"+  mitabla 


@app.route('/graficar/<pais>/<grafico>')
def graficar(pais, grafico):
        df = pd.read_csv("datos.csv", header=None)     # Cargar el archivo en un DataFrame
        df.columns = ["País", "Código", "Año", "Ahorro"]  # Asegurar nombres de columnas

        # Filtrar los datos por el país proporcionado
        df_filtrado = df[df["País"] == pais]

        if df_filtrado.empty:
            return f"<h3>No hay datos disponibles para el país: {pais}</h3>"

        # Crear el gráfico según el tipo seleccionado
        if grafico == "Linea":
            fig = px.line(df_filtrado,
                          x="Año",
                          y="Ahorro",
                          title=f"Ahorro de energía en {pais} (Línea)",
                          markers=True)
        elif grafico == "Torta":
            # Para un gráfico de torta, usamos un único valor por categoría, ejemplo: total por año
            df_agg = df_filtrado.groupby("Año").sum().reset_index()
            fig = px.pie(df_agg,
                         names="Año",
                         values="Ahorro",
                         title=f"Ahorro de energía en {pais} (Torta)")
        elif grafico == "Barras":
            fig = px.bar(df_filtrado,
                         x="Año",
                         y="Ahorro",
                         title=f"Ahorro de energía en {pais} (Barras)",
                         text_auto=True)
        elif grafico == "Area":
            fig = px.area(df_filtrado,
                          x="Año",
                          y="Ahorro",
                          title=f"Ahorro de energía en {pais} (Área)")
        else:
            return f"<h3>Tipo de gráfico '{grafico}' no reconocido.</h3>"
        # Convertir el gráfico a HTML
        graph_html = fig.to_html(full_html=False)
        return graph_html




def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
