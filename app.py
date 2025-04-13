import streamlit as st
import pandas as pd
import re
from io import BytesIO
st.title("Bot para limpiar y organizar leads")
st.write("Sube tu archivo excel con leads y limpiaremos los datos automáticamente.")
archivo_subido = st.file_uploader("Sube un archivo .xlsx", type= "xlsx")

if archivo_subido is not None:
    try:
        archivo = pd.read_excel(archivo_subido)
        st.subheader("Vista previa del archivo original:")
        st.dataframe(archivo)
        try:
            #Limpiar espacios y normalizar textos
            archivo["Nombre"] = archivo["Nombre"].str.strip().str.lower()
            archivo["Email"] = archivo["Email"].str.strip().str.lower()

            #Orden alfabético
            archivo = archivo.sort_values("Nombre")
            archivo = archivo.reset_index(drop= True)

            #Validar email
            filtro_email = archivo["Email"].str.contains("@", na=False) & archivo["Email"].str.contains(".com", case= False,  na= False)

            #Validar teléfono: exactamente 9 dígitos
            filtro_telefono = archivo["Teléfono"].astype(str).str.match(r"^\d{9}$", na= False)

            #Combinar filtros

            datos_limpios = archivo[filtro_email & filtro_telefono].copy()

            #Formatear nombres para presentación

            datos_limpios.loc[:,"Nombre"] = datos_limpios["Nombre"].str.title()

            #Eliminar duplicados
            datos_limpios=datos_limpios.drop_duplicates(subset = "Email")

            st.subheader("Datos limpios:")
            st.dataframe(datos_limpios)
            output = BytesIO()
            datos_limpios.to_excel(output, index= False, engine= "openpyxl")
            output.seek(0)

            #Botón de descarga
            st.download_button(
                label= "Descargar archivo limpio",
                data = output,
                file_name="leads_limpios.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
            )
        except KeyError as e:
            st.error(f"Faltan columnas necesarias: {e}")

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")    


