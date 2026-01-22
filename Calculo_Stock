import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora Wx(ref)", page_icon="🧪")

st.title("🧪 Calculadora de Concentración de Estándar")
st.markdown("Esta herramienta calcula la concentración $W_{x(ref)}$ basándose en la masa del estándar, su pureza y la masa final.")

# Mostrar la fórmula elegante
st.latex(r"W_{x(ref)} = \frac{m_{ref} \cdot P}{m_{final}}")

st.divider()

# Layout en columnas para que se vea más ordenado
col1, col2 = st.columns(2)

with col1:
    m_ref = st.number_input("Masa del estándar ($m_{ref}$) en mg", format="%.5f", step=0.00001)
    purity = st.number_input("Pureza ($P$) en porcentaje", value=1.0000, format="%.4f", step=0.0001)

with col2:
    m_final = st.number_input("Masa final ($m_{final}$) en g", format="%.5f", step=0.0001)

st.divider()

# Botón de cálculo
if st.button("Calcular Resultado", use_container_width=True):
    if m_final > 0:
        w_xref = (((m_ref/1000) * (purity/100)) / m_final)+1000
        st.balloons() # Un efecto visual divertido
        st.success(f"### Resultado: **{w_xref:.6f} mg/g**")
    else:
        st.error("La masa final debe ser mayor a cero para evitar división por cero.")

st.caption("Desarrollado con Python y Streamlit")
