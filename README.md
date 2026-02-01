# 🛣️ Calculadora Presupuestos Vial SEACE/MTC 2026

Aplicación web interactiva para calcular presupuestos de proyectos viales con base de datos de 90+ partidas oficiales del MTC (Ministerio de Transportes y Comunicaciones) del Perú.

## ✨ Características

- **Base de datos completa**: 90+ partidas de construcción vial con precios actualizados 2026
- **Categorías organizadas**:
  - Trabajos Preliminares
  - Movimiento de Tierras
  - Pavimentos (asfalto, concreto, adoquines)
  - Drenaje (alcantarillas, cunetas, badenes)
  - Obras de Arte (muros, gaviones, geomallas)
  - Señalización (verticales, horizontales, guardavías)

- **Análisis de Precios Unitarios (APU)**: Desglose detallado por:
  - Mano de obra
  - Equipos
  - Materiales

- **Funcionalidades**:
  - Búsqueda inteligente con autocompletado
  - Filtrado por categorías
  - Cálculo automático de GG (10%) y Utilidad (8%)
  - Exportación a CSV
  - Visualización de costos en tiempo real

## 🚀 Despliegue en Streamlit Cloud

### Paso 1: Subir a GitHub

1. **Crear repositorio en GitHub**:
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit - Calculadora Vial SEACE"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/calculadora-vial-seace.git
   git push -u origin main
   ```

2. **Estructura del proyecto**:
   ```
   calculadora-vial-seace/
   ├── app.py              # Aplicación principal
   ├── requirements.txt    # Dependencias Python
   └── README.md          # Documentación
   ```

### Paso 2: Conectar con Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Click en **"New app"**
4. Selecciona:
   - **Repository**: `TU_USUARIO/calculadora-vial-seace`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click en **"Deploy!"**

### Paso 3: ¡Listo! 🎉

Tu app estará disponible en:
```
https://TU_USUARIO-calculadora-vial-seace.streamlit.app
```

## 💻 Ejecución Local

### Requisitos
- Python 3.8+
- pip

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/calculadora-vial-seace.git
cd calculadora-vial-seace

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📊 Uso de la Aplicación

### 1. Seleccionar Partidas
- **Opción A**: Filtrar por categoría en el menú desplegable
- **Opción B**: Buscar por nombre o código en el buscador

### 2. Ver Análisis Unitario
Al seleccionar una partida, verás el desglose de costos:
- Precio unitario total
- % y monto de mano de obra
- % y monto de equipos
- % y monto de materiales

### 3. Agregar al Presupuesto
1. Selecciona la partida
2. Ingresa el metrado (cantidad)
3. Click en "➕ Agregar al Presupuesto"

### 4. Revisar Totales
La aplicación calcula automáticamente:
- Costo Directo
- Gastos Generales (10%)
- Utilidad (8%)
- **TOTAL PRESUPUESTO**

### 5. Exportar
Click en "📥 Descargar CSV" para exportar tu presupuesto completo

## 🏗️ Ejemplos de Partidas

### Pavimentos
- Pavimento concreto asfáltico (MAC) e=5cm, 7.5cm, 10cm
- Base granular e=0.25m
- Sub-base granular e=0.20m
- Imprimación asfáltica
- Tratamientos superficiales

### Drenaje
- Alcantarillas TMC Ø36", Ø48"
- Cunetas triangulares (revestidas y sin revestir)
- Badenes de concreto
- Subdrenes

### Señalización
- Señales verticales reglamentarias y preventivas
- Marcas en pavimento (pintura y termoplástico)
- Guardavías metálico doble onda
- Tachas reflectivas

## 📝 Base de Datos

La base de datos incluye:
- **Código de partida**: Según especificaciones técnicas MTC
- **Descripción**: Nombre completo de la partida
- **Unidad de medida**: m³, m², m, und, glb, etc.
- **Precio unitario**: En soles (S/)
- **APU desglosado**: Mano de obra, equipos, materiales

Precios referenciales del mercado peruano 2026 (zona Costa Sur).

## 🔧 Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Backend**: Python 3.11+
- **Framework**: Streamlit 1.31.0
- **Deployment**: Streamlit Cloud

## 📄 Licencia

Proyecto de código abierto para análisis de presupuestos viales en Perú.

## 👤 Autor

Desarrollado para análisis de proyectos de infraestructura vial SEACE/MTC.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para cambios importantes:
1. Fork el proyecto
2. Crea tu branch (`git checkout -b feature/NuevaPartida`)
3. Commit tus cambios (`git commit -m 'Agregar nueva partida'`)
4. Push al branch (`git push origin feature/NuevaPartida`)
5. Abre un Pull Request

## 📮 Contacto

Si tienes preguntas o sugerencias sobre la aplicación, abre un issue en GitHub.

---

**Nota**: Los precios son referenciales y deben ser ajustados según ubicación del proyecto, condiciones del mercado y análisis de costos actualizado.
