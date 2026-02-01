# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------
# Hardening: compatibilidad Cloud
# -----------------------------
rerun = getattr(st, "rerun", None) or st.experimental_rerun
cache_data = getattr(st, "cache_data", None) or st.cache

# -----------------------------
# Configuración página
# -----------------------------
st.set_page_config(page_title="Calculadora Vial SEACE", page_icon="🛣️", layout="wide")

# CSS personalizado (nota: Streamlit Cloud puede ignorar algunos selectores; no rompe)
st.markdown(
    """
    <style>
        .main {background-color: #0f172a; color: #f1f5f9;}
        .stMetric {background-color: #1e293b; padding: 1rem; border-radius: 8px;}
        h1, h2, h3 {color: #38bdf8 !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Base de datos (tu catálogo)
# -----------------------------
@cache_data
def cargar_partidas_completas() -> pd.DataFrame:
    return pd.DataFrame([
        # 01 - OBRAS PROVISIONALES, TRABAJOS PRELIMINARES, SEGURIDAD Y SALUD
        {'cat': 'preliminares', 'cod': '01.01.01.01', 'nombre': 'CARTEL DE ACTIVIDAD 4.80x3.60m (GIGANTOGRAFIA H=3.60m)', 'unidad': 'und', 'precio': 3500, 'mo': 800, 'mat': 2400, 'eq': 200, 'her': 100},
        {'cat': 'preliminares', 'cod': '01.01.01.02', 'nombre': 'ALQUILER DE BAÑOS PORTATILES', 'unidad': 'mes', 'precio': 450, 'mo': 100, 'mat': 300, 'eq': 30, 'her': 20},
        {'cat': 'preliminares', 'cod': '01.02.01', 'nombre': 'MOVILIZACION Y DESMOVILIZACION DE MAQUINARIAS, EQUIPO Y HERRAMIENTAS', 'unidad': 'glb', 'precio': 45000, 'mo': 5000, 'mat': 15000, 'eq': 25000, 'her': 0},
        {'cat': 'preliminares', 'cod': '01.02.02', 'nombre': 'TRAZO, NIVELES Y REPLANTEO', 'unidad': 'm2', 'precio': 2.85, 'mo': 1.20, 'mat': 0.45, 'eq': 1.10, 'her': 0.10},
        {'cat': 'preliminares', 'cod': '01.03.01', 'nombre': 'PLAN DE SEGURIDAD Y SALUD EN EL TRABAJO', 'unidad': 'glb', 'precio': 8500, 'mo': 5000, 'mat': 2500, 'eq': 800, 'her': 200},
        {'cat': 'preliminares', 'cod': '01.03.02', 'nombre': 'EQUIPOS DE PROTECCION PERSONAL (EPP)', 'unidad': 'glb', 'precio': 6500, 'mo': 0, 'mat': 6000, 'eq': 300, 'her': 200},
        {'cat': 'preliminares', 'cod': '01.03.03', 'nombre': 'EQUIPOS DE PROTECCION COLECTIVA', 'unidad': 'glb', 'precio': 4200, 'mo': 800, 'mat': 3000, 'eq': 300, 'her': 100},
        {'cat': 'preliminares', 'cod': '01.03.04', 'nombre': 'DESVIO TRANSITO Y SEÑALIZACION TEMPORAL DE SEGURIDAD EN OBRA', 'unidad': 'glb', 'precio': 12500, 'mo': 2500, 'mat': 8500, 'eq': 1200, 'her': 300},
        {'cat': 'preliminares', 'cod': '01.03.05', 'nombre': 'RECURSOS PARA RESPONDER ANTE EMERGENCIAS', 'unidad': 'glb', 'precio': 5800, 'mo': 1200, 'mat': 4000, 'eq': 400, 'her': 200},

        # 02 - REPOSICION DE PAVIMENTO
        # 02.01 - PARCHADO SUPERFICIAL
        {'cat': 'pavimentos', 'cod': '02.01.01', 'nombre': 'CORTE DE PAVIMENTO ASFALTICO EXISTENTE', 'unidad': 'm2', 'precio': 6.03, 'mo': 1.50, 'mat': 0.80, 'eq': 3.50, 'her': 0.23},
        {'cat': 'pavimentos', 'cod': '02.01.02', 'nombre': 'DEMOLICION DE CARPETA ASFALTICA CON EQUIPO', 'unidad': 'm2', 'precio': 6.03, 'mo': 1.20, 'mat': 0.50, 'eq': 4.10, 'her': 0.23},
        {'cat': 'pavimentos', 'cod': '02.01.03', 'nombre': 'ESCARIFICACIÓN Y COMPACTACION E=0.10m', 'unidad': 'm2', 'precio': 6.03, 'mo': 1.10, 'mat': 0.40, 'eq': 4.30, 'her': 0.23},
        {'cat': 'pavimentos', 'cod': '02.01.04', 'nombre': 'ACARREO DE MATERIAL EXCEDENTE Dm=100 M CON EQUIPO', 'unidad': 'm3', 'precio': 603.43, 'mo': 80.00, 'mat': 50.00, 'eq': 460.00, 'her': 13.43},
        {'cat': 'pavimentos', 'cod': '02.01.05', 'nombre': 'ELIMINACION DE MATERIAL EXCEDENTE Dm= 15Km', 'unidad': 'm3', 'precio': 603.43, 'mo': 85.00, 'mat': 45.00, 'eq': 460.00, 'her': 13.43},

        # 02.02 - PARCHADO PROFUNDO
        {'cat': 'pavimentos', 'cod': '02.02.01', 'nombre': 'CORTE DE PAVIMENTO ASFALTICO EXISTENTE', 'unidad': 'm2', 'precio': 26.41, 'mo': 6.50, 'mat': 3.20, 'eq': 15.80, 'her': 0.91},
        {'cat': 'pavimentos', 'cod': '02.02.02', 'nombre': 'DEMOLICION DE CARPETA ASFALTICA CON EQUIPO', 'unidad': 'm2', 'precio': 26.41, 'mo': 6.20, 'mat': 2.80, 'eq': 16.50, 'her': 0.91},
        {'cat': 'pavimentos', 'cod': '02.02.03', 'nombre': 'REMOCION DE BASE GRANULAR E=0.20m', 'unidad': 'm3', 'precio': 5.28, 'mo': 1.20, 'mat': 0.50, 'eq': 3.30, 'her': 0.28},
        {'cat': 'pavimentos', 'cod': '02.02.04', 'nombre': 'ACARREO DE MATERIAL EXCEDENTE Dm=100 M CON EQUIPO', 'unidad': 'm3', 'precio': 6.27, 'mo': 1.50, 'mat': 0.60, 'eq': 3.90, 'her': 0.27},
        {'cat': 'pavimentos', 'cod': '02.02.05', 'nombre': 'ELIMINACIÓN DE MATERIAL EXCEDENTE Dm= 15Km', 'unidad': 'm3', 'precio': 6.27, 'mo': 1.40, 'mat': 0.70, 'eq': 3.90, 'her': 0.27},
        {'cat': 'pavimentos', 'cod': '02.02.06', 'nombre': 'PERFILADO Y COMPACTADO', 'unidad': 'm2', 'precio': 26.41, 'mo': 6.00, 'mat': 2.50, 'eq': 17.00, 'her': 0.91},
        {'cat': 'pavimentos', 'cod': '02.02.07', 'nombre': 'CONFORMACIÓN Y COMPACTACIÓN DE BASE GRANULAR E=0.20m', 'unidad': 'm3', 'precio': 5.28, 'mo': 1.10, 'mat': 2.80, 'eq': 1.20, 'her': 0.18},

        # 02.03 - RECAPEO DE PAVIMENTO
        {'cat': 'pavimentos', 'cod': '02.03.01', 'nombre': 'RIEGO DE LIGA', 'unidad': 'm2', 'precio': 65.80, 'mo': 12.00, 'mat': 38.50, 'eq': 14.00, 'her': 1.30},
        {'cat': 'pavimentos', 'cod': '02.03.02', 'nombre': 'IMPRIMACIÓN ASFÁLTICA', 'unidad': 'm2', 'precio': 92.44, 'mo': 16.50, 'mat': 55.00, 'eq': 19.00, 'her': 1.94},
        {'cat': 'pavimentos', 'cod': '02.03.03', 'nombre': 'RECAPEO ASFALTICO COMPACTADO E=1.5"', 'unidad': 'm2', 'precio': 98.29, 'mo': 18.00, 'mat': 58.50, 'eq': 20.00, 'her': 1.79},

        # 03 - SEÑALIZACION
        {'cat': 'señalizacion', 'cod': '03.01', 'nombre': 'SEÑALIZACION HORIZONTAL', 'unidad': '', 'precio': 0, 'mo': 0, 'mat': 0, 'eq': 0, 'her': 0},
        {'cat': 'señalizacion', 'cod': '03.01.01', 'nombre': 'TRAZADO Y PINTADO DE MARCAS EN EL PAVIMENTO', 'unidad': 'm2', 'precio': 4.47, 'mo': 1.20, 'mat': 2.50, 'eq': 0.65, 'her': 0.12},
        {'cat': 'señalizacion', 'cod': '03.01.02', 'nombre': 'PINTADO DE PAVIMENTO - PASE PEATONAL', 'unidad': 'm2', 'precio': 2.93, 'mo': 0.80, 'mat': 1.70, 'eq': 0.35, 'her': 0.08},

        # 04 - PLAN DE MONITOREO AMBIENTAL
        {'cat': 'ambiental', 'cod': '04.01', 'nombre': 'ELABORACIÓN DE PLAN DE MONITOREO AMBIENTAL', 'unidad': 'glb', 'precio': 3500, 'mo': 2500, 'mat': 800, 'eq': 150, 'her': 50},
        {'cat': 'ambiental', 'cod': '04.02', 'nombre': 'RIEGO EN LA ZONA DE TRABAJO X', 'unidad': 'mes', 'precio': 2800, 'mo': 1200, 'mat': 1200, 'eq': 350, 'her': 50},
        {'cat': 'ambiental', 'cod': '04.03', 'nombre': 'MONITOREO DEL RUIDO Y CALIDAD DEL AIRE', 'unidad': 'glb', 'precio': 4500, 'mo': 2800, 'mat': 1200, 'eq': 400, 'her': 100},
        {'cat': 'ambiental', 'cod': '04.04', 'nombre': 'CONTENEDORES PLÁSTICOS 94lt (min.)', 'unidad': 'und', 'precio': 85, 'mo': 15, 'mat': 65, 'eq': 3, 'her': 2},

        # 05 - CONSIDERACIONES VARIAS
        {'cat': 'varios', 'cod': '05.01', 'nombre': 'LIMPIEZA FINAL DE OBRA', 'unidad': 'glb', 'precio': 2500, 'mo': 1800, 'mat': 500, 'eq': 150, 'her': 50},
        {'cat': 'varios', 'cod': '05.02', 'nombre': 'NIVELACION DE TECHO DE BUZONES', 'unidad': 'und', 'precio': 380, 'mo': 150, 'mat': 180, 'eq': 40, 'her': 10},

        # MOVIMIENTO DE TIERRAS adicionales
        {'cat': 'movimiento', 'cod': '201.01', 'nombre': 'DESBROCE Y LIMPIEZA', 'unidad': 'ha', 'precio': 8500, 'mo': 2500, 'mat': 500, 'eq': 5200, 'her': 300},
        {'cat': 'movimiento', 'cod': '202.01', 'nombre': 'EXCAVACIÓN NO CLASIFICADA', 'unidad': 'm3', 'precio': 18.50, 'mo': 4.20, 'mat': 0.80, 'eq': 13.00, 'her': 0.50},
        {'cat': 'movimiento', 'cod': '203.01', 'nombre': 'EXCAVACIÓN EN ROCA SUELTA', 'unidad': 'm3', 'precio': 38.20, 'mo': 8.50, 'mat': 3.20, 'eq': 25.50, 'her': 1.00},
        {'cat': 'movimiento', 'cod': '204.01', 'nombre': 'EXCAVACIÓN EN ROCA FIJA', 'unidad': 'm3', 'precio': 62.00, 'mo': 12.00, 'mat': 8.00, 'eq': 40.00, 'her': 2.00},
        {'cat': 'movimiento', 'cod': '205.01', 'nombre': 'CONFORMACIÓN TERRAPLENES', 'unidad': 'm3', 'precio': 22.40, 'mo': 5.00, 'mat': 1.20, 'eq': 15.50, 'her': 0.70},
        {'cat': 'movimiento', 'cod': '206.01', 'nombre': 'PERFILADO Y COMPACTADO SUBRASANTE', 'unidad': 'm2', 'precio': 3.80, 'mo': 0.80, 'mat': 0.20, 'eq': 2.70, 'her': 0.10},
        {'cat': 'movimiento', 'cod': '207.01', 'nombre': 'MEJORAMIENTO SUELOS CAL 3%', 'unidad': 'm3', 'precio': 85.00, 'mo': 12.00, 'mat': 45.00, 'eq': 26.00, 'her': 2.00},
        {'cat': 'movimiento', 'cod': '208.01', 'nombre': 'ELIMINACIÓN MATERIAL EXCEDENTE d<1km', 'unidad': 'm3', 'precio': 12.50, 'mo': 2.50, 'mat': 0.50, 'eq': 9.00, 'her': 0.50},

        # PAVIMENTOS adicionales
        {'cat': 'pavimentos', 'cod': '401.01', 'nombre': 'CAPA ANTICONTAMINANTE e=0.15m', 'unidad': 'm3', 'precio': 35.00, 'mo': 8.00, 'mat': 20.00, 'eq': 6.00, 'her': 1.00},
        {'cat': 'pavimentos', 'cod': '402.01', 'nombre': 'SUB-BASE GRANULAR e=0.20m', 'unidad': 'm3', 'precio': 72.50, 'mo': 14.00, 'mat': 42.00, 'eq': 15.00, 'her': 1.50},
        {'cat': 'pavimentos', 'cod': '403.01', 'nombre': 'BASE GRANULAR e=0.25m', 'unidad': 'm3', 'precio': 85.50, 'mo': 15.20, 'mat': 48.30, 'eq': 20.00, 'her': 2.00},
        {'cat': 'pavimentos', 'cod': '404.01', 'nombre': 'BASE ESTABILIZADA CEMENTO 3%', 'unidad': 'm3', 'precio': 165.00, 'mo': 28.00, 'mat': 95.00, 'eq': 38.00, 'her': 4.00},
        {'cat': 'pavimentos', 'cod': '405.01', 'nombre': 'BASE ASFÁLTICA e=0.10m', 'unidad': 'm3', 'precio': 320.00, 'mo': 45.00, 'mat': 195.00, 'eq': 72.00, 'her': 8.00},
        {'cat': 'pavimentos', 'cod': '406.01', 'nombre': 'IMPRIMACIÓN ASFÁLTICA', 'unidad': 'm2', 'precio': 4.80, 'mo': 0.80, 'mat': 2.50, 'eq': 1.30, 'her': 0.20},
        {'cat': 'pavimentos', 'cod': '407.01', 'nombre': 'RIEGO LIGA ASFALTO DILUIDO', 'unidad': 'm2', 'precio': 2.20, 'mo': 0.40, 'mat': 1.20, 'eq': 0.50, 'her': 0.10},
        {'cat': 'pavimentos', 'cod': '408.01', 'nombre': 'TRATAMIENTO SUPERFICIAL MONOCAPA', 'unidad': 'm2', 'precio': 18.50, 'mo': 3.50, 'mat': 11.00, 'eq': 3.50, 'her': 0.50},
        {'cat': 'pavimentos', 'cod': '416.01', 'nombre': 'PAVIMENTO CONCRETO ASFALTICO CALIENTE e=5cm', 'unidad': 'm3', 'precio': 920.00, 'mo': 120.00, 'mat': 580.00, 'eq': 200.00, 'her': 20.00},
        {'cat': 'pavimentos', 'cod': '416.03', 'nombre': 'PAVIMENTO CONCRETO ASFALTICO CALIENTE e=10cm', 'unidad': 'm3', 'precio': 920.00, 'mo': 120.00, 'mat': 580.00, 'eq': 200.00, 'her': 20.00},
        {'cat': 'pavimentos', 'cod': '422.01', 'nombre': 'PAVIMENTO CONCRETO HIDRÁULICO fc=280 e=0.20m', 'unidad': 'm3', 'precio': 450.00, 'mo': 85.00, 'mat': 280.00, 'eq': 75.00, 'her': 10.00},

        # DRENAJE
        {'cat': 'drenaje', 'cod': '504.01', 'nombre': 'ALCANTARILLA TMC Ø36" L=6m', 'unidad': 'm', 'precio': 380.00, 'mo': 65.00, 'mat': 250.00, 'eq': 55.00, 'her': 10.00},
        {'cat': 'drenaje', 'cod': '509.01', 'nombre': 'CUNETAS REVESTIDAS CONCRETO fc=175', 'unidad': 'm', 'precio': 42.00, 'mo': 12.00, 'mat': 22.00, 'eq': 6.50, 'her': 1.50},

        # SEÑALIZACION adicional
        {'cat': 'señalizacion', 'cod': '801.01', 'nombre': 'SEÑAL VERTICAL REGLAMENTARIA 0.60x0.60m', 'unidad': 'und', 'precio': 280.00, 'mo': 45.00, 'mat': 200.00, 'eq': 25.00, 'her': 10.00},
        {'cat': 'señalizacion', 'cod': '803.01', 'nombre': 'MARCAS PAVIMENTO PINTURA TRÁFICO CONTINUA 0.10m', 'unidad': 'm', 'precio': 1.80, 'mo': 0.35, 'mat': 1.10, 'eq': 0.30, 'her': 0.05},
    ])

# -----------------------------
# Inicializar sesión
# -----------------------------
if "presupuesto" not in st.session_state:
    st.session_state.presupuesto = []

# -----------------------------
# Header
# -----------------------------
st.title("🛣️ Calculadora Presupuestos Vial SEACE - Base Completa")
st.caption("📊 Catálogo de partidas + APUs (MO/Mat/Eq/Her) | Cotización rápida y análisis")

# Cargar DB
df_partidas = cargar_partidas_completas()

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📋 Presupuesto", "🔍 Ver APUs", "📊 Análisis"])

# -----------------------------
# TAB 1: Presupuesto
# -----------------------------
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Selección de Partidas")

        categorias = {
            "todas": "Todas las categorías",
            "preliminares": "01 - Trabajos Preliminares",
            "movimiento": "Movimiento Tierras",
            "pavimentos": "02 - Pavimentos / Reposición",
            "drenaje": "Drenaje",
            "señalizacion": "03 - Señalización",
            "ambiental": "04 - Plan Monitoreo Ambiental",
            "varios": "05 - Varios",
        }

        cat_sel = st.selectbox(
            "Categoría",
            options=list(categorias.keys()),
            format_func=lambda x: categorias[x],
        )

        if cat_sel != "todas":
            df_filtrado = df_partidas[df_partidas["cat"] == cat_sel].copy()
        else:
            df_filtrado = df_partidas.copy()

        busqueda = st.text_input("🔍 Buscar partida", placeholder="Código o nombre...")
        if busqueda:
            df_filtrado = df_filtrado[
                df_filtrado["nombre"].astype(str).str.contains(busqueda, case=False, na=False)
                | df_filtrado["cod"].astype(str).str.contains(busqueda, case=False, na=False)
            ]

        st.caption(f"📦 {len(df_filtrado)} partidas disponibles en esta categoría")

        if len(df_filtrado) > 0:
            # Arma un display seguro
            df_filtrado = df_filtrado.copy()
            df_filtrado["display"] = df_filtrado.apply(
                lambda x: f"{x['cod']} - {x['nombre']} ({x['unidad']}) - S/ {float(x['precio']):.2f}",
                axis=1
            )

            # Selectbox por código
            codigos = df_filtrado["cod"].tolist()
            partida_sel = st.selectbox(
                "Partida",
                options=codigos,
                format_func=lambda x: df_filtrado.loc[df_filtrado["cod"] == x, "display"].values[0]
                if (df_filtrado["cod"] == x).any() else x
            )

            if partida_sel and (df_filtrado["cod"] == partida_sel).any():
                partida_info = df_filtrado[df_filtrado["cod"] == partida_sel].iloc[0]

                with st.expander("🔍 Ver APU de esta partida"):
                    col_apu1, col_apu2, col_apu3, col_apu4 = st.columns(4)
                    precio = float(partida_info["precio"])
                    if precio > 0:
                        col_apu1.metric("Mano Obra", f"S/ {float(partida_info['mo']):.2f}", f"{(float(partida_info['mo'])/precio*100):.1f}%")
                        col_apu2.metric("Materiales", f"S/ {float(partida_info['mat']):.2f}", f"{(float(partida_info['mat'])/precio*100):.1f}%")
                        col_apu3.metric("Equipos", f"S/ {float(partida_info['eq']):.2f}", f"{(float(partida_info['eq'])/precio*100):.1f}%")
                        col_apu4.metric("Herramientas", f"S/ {float(partida_info['her']):.2f}", f"{(float(partida_info['her'])/precio*100):.1f}%")
                    else:
                        st.info("Esta es una partida cabecera (precio 0).")

            metrado = st.number_input("Metrado", min_value=0.0, step=0.01, value=0.0)

            if st.button("➕ Agregar al Presupuesto", type="primary"):
                if metrado > 0 and (df_filtrado["cod"] == partida_sel).any():
                    partida = df_filtrado[df_filtrado["cod"] == partida_sel].iloc[0]
                    st.session_state.presupuesto.append({
                        "cod": partida["cod"],
                        "nombre": partida["nombre"],
                        "unidad": partida["unidad"],
                        "metrado": float(metrado),
                        "precio": float(partida["precio"]),
                        "parcial": float(metrado) * float(partida["precio"]),
                        "mo": float(partida["mo"]) * float(metrado),
                        "mat": float(partida["mat"]) * float(metrado),
                        "eq": float(partida["eq"]) * float(metrado),
                        "her": float(partida["her"]) * float(metrado),
                    })
                    st.success(f"✅ Agregado: {partida['nombre']}")
                    rerun()
                else:
                    st.warning("⚠️ Ingresa metrado mayor a 0 y selecciona una partida válida.")
        else:
            st.info("No hay partidas en esta categoría o con ese criterio de búsqueda.")

    with col2:
        st.subheader("💰 Resumen")

        if st.session_state.presupuesto:
            directo = sum(p["parcial"] for p in st.session_state.presupuesto)
            total_mo = sum(p["mo"] for p in st.session_state.presupuesto)
            total_mat = sum(p["mat"] for p in st.session_state.presupuesto)
            total_eq = sum(p["eq"] for p in st.session_state.presupuesto)
            total_her = sum(p["her"] for p in st.session_state.presupuesto)

            gg = directo * 0.10
            util = directo * 0.08
            total = directo + gg + util
        else:
            directo = total_mo = total_mat = total_eq = total_her = gg = util = total = 0.0

        m1, m2, m3 = st.columns(3)
        m1.metric("Costo Directo", f"S/ {directo:,.0f}")
        m2.metric("GG+Util. (18%)", f"S/ {(gg + util):,.0f}")
        m3.metric("TOTAL", f"S/ {total:,.0f}")

        st.markdown("### 📊 Desglose Costo Directo")
        col_d1, col_d2 = st.columns(2)
        col_d1.metric("Mano de Obra", f"S/ {total_mo:,.0f}", f"{(total_mo/directo*100 if directo>0 else 0):.1f}%")
        col_d1.metric("Materiales", f"S/ {total_mat:,.0f}", f"{(total_mat/directo*100 if directo>0 else 0):.1f}%")
        col_d2.metric("Equipos", f"S/ {total_eq:,.0f}", f"{(total_eq/directo*100 if directo>0 else 0):.1f}%")
        col_d2.metric("Herramientas", f"S/ {total_her:,.0f}", f"{(total_her/directo*100 if directo>0 else 0):.1f}%")

        if directo > 0:
            fig_apu = px.pie(
                values=[total_mo, total_mat, total_eq, total_her],
                names=["Mano Obra", "Materiales", "Equipos", "Herramientas"],
                title="Composición Costo Directo"
            )
            st.plotly_chart(fig_apu, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Presupuesto Detallado")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("🗑️ Limpiar Todo"):
            st.session_state.presupuesto = []
            rerun()

    if st.session_state.presupuesto:
        df_pres = pd.DataFrame(st.session_state.presupuesto)

        # Dataframe sin Styler (más estable en Cloud)
        st.dataframe(
            df_pres[["cod", "nombre", "unidad", "metrado", "precio", "mo", "mat", "eq", "her", "parcial"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "metrado": st.column_config.NumberColumn("Metrado", format="%.2f"),
                "precio": st.column_config.NumberColumn("Precio", format="S/ %.2f"),
                "mo": st.column_config.NumberColumn("MO", format="S/ %.2f"),
                "mat": st.column_config.NumberColumn("Mat", format="S/ %.2f"),
                "eq": st.column_config.NumberColumn("Eq", format="S/ %.2f"),
                "her": st.column_config.NumberColumn("Her", format="S/ %.2f"),
                "parcial": st.column_config.NumberColumn("Parcial", format="S/ %.2f"),
            }
        )

        st.markdown("---")
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.write("**COSTO DIRECTO**")
            st.write("**Gastos Generales (10%)**")
            st.write("**Utilidad (8%)**")
            st.markdown("### **TOTAL PRESUPUESTO**")
        with col_t2:
            st.write(f"S/ {directo:,.2f}")
            st.write(f"S/ {gg:,.2f}")
            st.write(f"S/ {util:,.2f}")
            st.markdown(f"### **S/ {total:,.2f}**")

        with col_btn2:
            csv = df_pres.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 CSV con APUs",
                csv,
                file_name=f"presupuesto_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("👆 Agrega partidas para comenzar.")

# -----------------------------
# TAB 2: Ver APUs
# -----------------------------
with tab2:
    st.subheader("🔍 Análisis de Precios Unitarios (APUs)")

    cat_apu = st.selectbox(
        "Filtrar por categoría",
        options=["todas"] + list(categorias.keys())[1:],
        format_func=lambda x: categorias.get(x, x),
        key="cat_apu",
    )

    df_apu_view = df_partidas if cat_apu == "todas" else df_partidas[df_partidas["cat"] == cat_apu]
    st.caption(f"📦 Mostrando {len(df_apu_view)} partidas")

    # Para listas grandes, esto puede ser pesado en cloud; pero con tu tamaño actual va bien.
    for _, row in df_apu_view.iterrows():
        if float(row["precio"]) > 0:
            with st.expander(f"**{row['cod']}** - {row['nombre']} | S/ {float(row['precio']):.2f}/{row['unidad']}"):
                col1, col2, col3, col4, col5 = st.columns(5)
                precio = float(row["precio"])
                col1.metric("Precio Total", f"S/ {precio:.2f}")
                col2.metric("Mano Obra", f"S/ {float(row['mo']):.2f}", f"{(float(row['mo'])/precio*100):.1f}%")
                col3.metric("Materiales", f"S/ {float(row['mat']):.2f}", f"{(float(row['mat'])/precio*100):.1f}%")
                col4.metric("Equipos", f"S/ {float(row['eq']):.2f}", f"{(float(row['eq'])/precio*100):.1f}%")
                col5.metric("Herramientas", f"S/ {float(row['her']):.2f}", f"{(float(row['her'])/precio*100):.1f}%")

# -----------------------------
# TAB 3: Análisis
# -----------------------------
with tab3:
    st.subheader("📊 Análisis Comparativo")

    if st.session_state.presupuesto:
        df_analisis = pd.DataFrame(st.session_state.presupuesto)

        fig_bar = px.bar(
            df_analisis,
            x="cod",
            y="parcial",
            title="Costo por Partida",
            labels={"parcial": "Costo (S/)", "cod": "Código"},
            color="parcial",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(name="Mano Obra", x=df_analisis["cod"], y=df_analisis["mo"]))
        fig_stack.add_trace(go.Bar(name="Materiales", x=df_analisis["cod"], y=df_analisis["mat"]))
        fig_stack.add_trace(go.Bar(name="Equipos", x=df_analisis["cod"], y=df_analisis["eq"]))
        fig_stack.add_trace(go.Bar(name="Herramientas", x=df_analisis["cod"], y=df_analisis["her"]))
        fig_stack.update_layout(barmode="stack", title="Composición APU por Partida")
        st.plotly_chart(fig_stack, use_container_width=True)
    else:
        st.info("Agrega partidas al presupuesto.")

st.caption("🚀 Base de datos de partidas (APUs) | Despliegue robusto para Streamlit Cloud")
