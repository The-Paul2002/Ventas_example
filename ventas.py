#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date, timedelta


# In[9]:


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date

st.set_page_config(layout='wide')

st.title("📊 Dashboard de Ventas por Departamento")

# -------------------------------
# 🧪 Simular datos ficticios
# -------------------------------

# Lista ampliada de departamentos
departamentos = [
    'Lima', 'Arequipa', 'Cusco', 'La Libertad', 'Piura', 'Junín', 'Lambayeque', 
    'Ancash', 'Callao', 'Puno', 'Ica', 'Cajamarca', 'Loreto', 'Ayacucho', 
    'San Martín', 'Tacna', 'Moquegua', 'Ucayali', 'Huánuco', 'Pasco'
]

fechas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

# Crear dataset ficticio
np.random.seed(42)
data = pd.DataFrame({
    'Fecha': np.random.choice(fechas, 1000),
    'Departamento': np.random.choice(departamentos, 1000),
    'Ventas': np.random.randint(1000, 15000, 1000)
})

# -------------------------------
# 🎛 Filtros
# -------------------------------
st.sidebar.header("Filtros")

dep_seleccionado = st.sidebar.selectbox("Departamento:", ['Todos'] + departamentos)
fecha_inicio = st.sidebar.date_input("Desde", date(2024, 1, 1))
fecha_fin = st.sidebar.date_input("Hasta", date(2024, 12, 31))

df = data.copy()

# Filtros
if dep_seleccionado != 'Todos':
    df = df[df['Departamento'] == dep_seleccionado]

df = df[(df['Fecha'] >= pd.to_datetime(fecha_inicio)) & (df['Fecha'] <= pd.to_datetime(fecha_fin))]

# -------------------------------
# 🔢 KPIs
# -------------------------------
st.subheader("📌 Métricas clave")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas totales", f"S/ {df['Ventas'].sum():,.0f}")
col2.metric("📊 Promedio de ventas", f"S/ {df['Ventas'].mean():,.0f}")
col3.metric("📅 Días registrados", df['Fecha'].nunique())

# -------------------------------
# 📈 Gráfico de línea (ventas por fecha)
# -------------------------------
st.subheader("📅 Ventas acumuladas por fecha")

ventas_fecha = df.groupby('Fecha')['Ventas'].sum().reset_index()

line_chart = alt.Chart(ventas_fecha).mark_line(point=True).encode(
    x='Fecha:T',
    y='Ventas:Q',
    tooltip=['Fecha:T', 'Ventas:Q']
).properties(width=700, height=300).interactive()

st.altair_chart(line_chart)

# -------------------------------
# 📊 Histograma de ventas
# -------------------------------
st.subheader("📊 Distribución de ventas (Histograma)")

st.write("Esta gráfica muestra cómo se distribuyen los montos de venta individuales.")

hist_chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
    alt.X('Ventas:Q', bin=alt.Bin(maxbins=30), title='Monto de venta (S/)'),
    y='count()',
    tooltip=['count()']
).properties(width=700, height=300)

st.altair_chart(hist_chart)

# -------------------------------
# 📋 Detalles de la data
# -------------------------------
st.subheader("📄 Tabla de datos filtrados")
st.dataframe(df.sort_values('Fecha'))


# In[ ]:


#get_ipython().system('jupyter nbconvert --to script ventas.ipynb')


# In[ ]:





# In[ ]:




