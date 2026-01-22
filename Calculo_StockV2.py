import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Registro de Estándares", page_icon="🧪", layout="wide")

st.title("🧪 Sistema de Registro y Cálculo de Estándares")

# 2. Inicializar la "Base de Datos" en la memoria de la sesión
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=[
        "Fecha/Hora", "Compuesto", "CAS", "Lote", "Código Solución", 
        "m_ref (g)", "Pureza", "m_final (g)", "Wx(ref) (g/g)"
    ])

# 3. Formulario de entrada de datos
with st.expander("📝 Ingresar Datos del Estándar", expanded=True):
    col_text1, col_text2 = st.columns(2)
    
    with col_text1:
        nombre_compuesto = st.text_input("Nombre del Compuesto", placeholder="Ej: Chlorpyrifos")
        cas_no = st.text_input("Número CAS", placeholder="Ej: 58-08-2")
    
    with col_text2:
        lote = st.text_input("Lote del Estándar", placeholder="Ej: LOT123456")
        codigo_solucion = st.text_input("Código de la Solución", placeholder="Ej: SER-001A")

    st.divider()
    
    col_num1, col_num2, col_num3 = st.columns(3)
    with col_num1:
        m_ref = st.number_input("Masa ref ($m_{ref}$)", format="%.5f", step=0.00001)
    with col_num2:
        purity = st.number_input("Pureza ($P$)", value=1.0000, format="%.4f")
    with col_num3:
        m_final = st.number_input("Masa final ($m_{final}$)", format="%.5f", step=0.0001)

# 4. Lógica de cálculo y almacenamiento
if st.button("Calcular y Guardar en Histórico", use_container_width=True):
    if m_final > 0 and nombre_compuesto:
        # Cálculo
        w_xref = (((m_ref/1000) * (purity/100)) / m_final)*1000
        
        # Crear nueva fila
        nueva_fila = {
            "Fecha/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Compuesto": nombre_compuesto,
            "CAS": cas_no,
            "Lote": lote,
            "Código Solución": codigo_solucion,
            "m_ref (g)": m_ref,
            "Pureza": purity,
            "m_final (g)": m_final,
            "Wx(ref) (g/g)": round(w_xref, 6)
        }
        
        # Guardar en el DataFrame de la sesión
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([nueva_fila])], ignore_index=True)
        
        st.success(f"Cálculo completado: Wx(ref) = {w_xref:.6f} g/g")
    else:
        st.error("Por favor, asegúrate de ingresar el nombre del compuesto y que la masa final sea mayor a cero.")

# 5. Visualización del Histórico (Dataframe)
st.divider()
st.subheader("📊 Histórico de Cálculos Consultados")

if not st.session_state.historico.empty:
    # Mostrar la tabla
    st.dataframe(st.session_state.historico, use_container_width=True)
    
    # Botón para descargar el histórico en Excel/CSV
    csv = st.session_state.historico.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Histórico como CSV",
        data=csv,
        file_name=f"historico_estandares_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
    
    if st.button("Limpiar Histórico"):
        st.session_state.historico = pd.DataFrame(columns=st.session_state.historico.columns)
        st.rerun()
else:
    st.info("Aún no hay datos registrados en esta sesión.")
