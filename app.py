import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Calculadora Vial SEACE",
    page_icon="🛣️",
    layout="wide"
)

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Vial SEACE - MTC 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #141b34;
            --bg-card: #1a2238;
            --bg-hover: #252e48;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --accent-orange: #f59e0b;
            --accent-red: #ef4444;
            --border-color: #2d3548;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-accent: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 2rem;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        /* Header */
        .header {
            background: var(--gradient-primary);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,0 C300,100 900,20 1200,80 L1200,120 L0,120 Z" fill="rgba(255,255,255,0.05)"/></svg>') bottom;
            background-size: cover;
            opacity: 0.5;
        }

        .header-content {
            position: relative;
            z-index: 1;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: rgba(255,255,255,0.9);
            font-weight: 500;
        }

        /* Grid Layout */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 450px;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1.75rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
        }

        .card-icon {
            font-size: 1.5rem;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        /* Form Elements */
        select, input[type="text"], input[type="number"] {
            width: 100%;
            padding: 0.875rem 1rem;
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }

        select:focus, input:focus {
            outline: none;
            border-color: var(--accent-blue);
            background: var(--bg-hover);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        select:hover, input:hover {
            border-color: var(--accent-cyan);
        }

        /* Buttons */
        button {
            background: var(--gradient-accent);
            color: white;
            padding: 0.875rem 1.5rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        button:active {
            transform: translateY(0);
        }

        .btn-danger {
            background: var(--accent-red);
        }

        .btn-success {
            background: var(--accent-green);
        }

        .btn-warning {
            background: var(--accent-orange);
        }

        /* Metrics */
        .metrics-grid {
            display: grid;
            gap: 1rem;
        }

        .metric-card {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            background: var(--bg-hover);
            transform: translateX(5px);
        }

        .metric-label {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            background: var(--gradient-accent);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Search Box */
        .search-box {
            position: relative;
            margin-bottom: 1rem;
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        .search-box input {
            padding-left: 2.75rem;
        }

        .autocomplete {
            position: absolute;
            top: calc(100% + 0.5rem);
            left: 0;
            right: 0;
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            max-height: 350px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: var(--shadow-lg);
        }

        .autocomplete-item {
            padding: 0.875rem 1rem;
            cursor: pointer;
            border-bottom: 1px solid var(--border-color);
            transition: all 0.15s ease;
            font-size: 0.9rem;
        }

        .autocomplete-item:last-child {
            border-bottom: none;
        }

        .autocomplete-item:hover {
            background: var(--bg-hover);
            padding-left: 1.5rem;
        }

        /* Table */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 1.5rem 0;
            border-radius: 8px;
            overflow: hidden;
        }

        th {
            background: var(--bg-secondary);
            color: var(--text-primary);
            padding: 1rem;
            text-align: left;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.9rem;
        }

        tbody tr {
            background: var(--bg-card);
            transition: all 0.2s ease;
        }

        tbody tr:hover {
            background: var(--bg-hover);
        }

        tfoot tr {
            background: var(--bg-secondary);
            font-weight: 600;
        }

        tfoot tr:last-child {
            background: var(--gradient-accent);
            color: white;
            font-weight: 700;
        }

        /* APU Panel */
        .apu-panel {
            animation: slideInRight 0.3s ease;
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .apu-header {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 4px solid var(--accent-blue);
        }

        .apu-price {
            background: var(--gradient-accent);
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .apu-price-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.25rem;
        }

        .apu-price-label {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.8);
            font-weight: 600;
        }

        .apu-breakdown {
            margin-bottom: 1.25rem;
        }

        .apu-item-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .apu-item-name {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
        }

        .apu-item-value {
            font-weight: 700;
            color: var(--accent-cyan);
        }

        .progress-bar {
            background: var(--bg-secondary);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 0.25rem;
        }

        .progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.6s ease;
        }

        .progress-mo { background: var(--accent-green); }
        .progress-eq { background: var(--accent-orange); }
        .progress-mat { background: var(--accent-blue); }

        .apu-percentage {
            text-align: right;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
        }

        /* Action Buttons Row */
        .action-buttons {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-blue);
        }

        /* Badge */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--accent-blue);
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-left: 0.5rem;
        }

        /* Responsive */
        @media (max-width: 1400px) {
            .main-grid {
                grid-template-columns: 1fr 1fr;
            }

            .card:last-child {
                grid-column: 1 / -1;
            }
        }

        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.75rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>
                    🛣️ Calculadora Presupuestos Vial
                    <span class="badge">MTC 2026</span>
                </h1>
                <p class="subtitle">Base de datos oficial SEACE con 90+ partidas especializadas | Precios actualizados mercado peruano</p>
            </div>
        </div>

        <div class="main-grid">
            <!-- Panel de Selección -->
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">📋</span>
                    <h2 class="card-title">Selección de Partidas</h2>
                </div>

                <select id="categoria">
                    <option value="">📊 Todas las categorías</option>
                    <option value="preliminares">🏗️ Trabajos Preliminares</option>
                    <option value="movimiento">⛏️ Movimiento de Tierras</option>
                    <option value="pavimentos">🛣️ Pavimentos</option>
                    <option value="drenaje">💧 Drenaje</option>
                    <option value="señalizacion">🚦 Señalización</option>
                    <option value="obras_arte">🏛️ Obras de Arte</option>
                </select>

                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="buscar" placeholder="Buscar por código o descripción...">
                    <div id="autocomplete" class="autocomplete"></div>
                </div>

                <select id="partida" size="8" style="height: 280px; margin-bottom: 1rem;">
                    <option value="">Cargando partidas...</option>
                </select>

                <input type="number" id="metrado" placeholder="Ingrese metrado (cantidad)" min="0" step="0.01">
                <button onclick="agregarPartida()" class="btn-success">
                    <span>➕</span> Agregar al Presupuesto
                </button>
            </div>

            <!-- Panel de Métricas -->
            <div class="card">
                <div class="card-header">
                    <span class="card-icon">💰</span>
                    <h2 class="card-title">Resumen Financiero</h2>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">💵 Costo Directo</div>
                        <div class="metric-value" id="costoDirecto">S/ 0</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">📊 Total + GG + Utilidad</div>
                        <div class="metric-value" id="total">S/ 0</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">📦 Partidas Agregadas</div>
                        <div class="metric-value" id="numPartidas">0</div>
                    </div>
                </div>
            </div>

            <!-- Panel APU -->
            <div class="card apu-panel" id="apuPanel" style="display: none;">
                <div class="card-header">
                    <span class="card-icon">🔍</span>
                    <h2 class="card-title">Análisis de Precios Unitarios</h2>
                </div>
                <div id="apuContent">
                    <p style="color: var(--text-secondary); text-align: center; padding: 2rem;">
                        Selecciona una partida para ver su análisis detallado
                    </p>
                </div>
            </div>
        </div>

        <!-- Tabla de Presupuesto -->
        <div class="card">
            <div class="card-header">
                <span class="card-icon">📊</span>
                <h2 class="card-title">Presupuesto Detallado</h2>
            </div>

            <div class="action-buttons">
                <button onclick="exportarCSV()" class="btn-success">
                    <span>📥</span> Descargar CSV
                </button>
                <button onclick="exportarPDF()" class="btn-warning">
                    <span>📄</span> Generar PDF
                </button>
                <button onclick="limpiar()" class="btn-danger">
                    <span>🗑️</span> Limpiar Todo
                </button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Partida</th>
                        <th>Unidad</th>
                        <th>Metrado</th>
                        <th>P.U. (S/)</th>
                        <th>Parcial (S/)</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody id="tbody">
                    <tr>
                        <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                            No hay partidas agregadas. Comienza seleccionando partidas arriba.
                        </td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="4"><strong>COSTO DIRECTO</strong></td>
                        <td id="tdDirecto"><strong>S/ 0.00</strong></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td colspan="4">Gastos Generales (10%)</td>
                        <td id="tdGG">S/ 0.00</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td colspan="4">Utilidad (8%)</td>
                        <td id="tdUtil">S/ 0.00</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td colspan="4"><strong>TOTAL PRESUPUESTO</strong></td>
                        <td id="tdTotal"><strong>S/ 0.00</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </div>

    <script>
        const partidasDB = [
            {cat:'preliminares',cod:'101.01',nombre:'Movilización y desmovilización equipos',unidad:'glb',precio:45000,apu:{mo:8500,eq:32000,mat:4500}},
            {cat:'preliminares',cod:'102.01',nombre:'Topografía y georeferenciación',unidad:'km',precio:2500,apu:{mo:1200,eq:900,mat:400}},
            {cat:'preliminares',cod:'103.01',nombre:'Campamento provisional obra',unidad:'mes',precio:12000,apu:{mo:4500,eq:2500,mat:5000}},
            {cat:'preliminares',cod:'104.01',nombre:'Cartel obra 3.60x7.20m',unidad:'und',precio:3500,apu:{mo:450,eq:250,mat:2800}},
            {cat:'preliminares',cod:'105.01',nombre:'Mantenimiento tránsito temporal',unidad:'mes',precio:8500,apu:{mo:5200,eq:1800,mat:1500}},
            {cat:'preliminares',cod:'106.01',nombre:'Nivelación y replanteo',unidad:'km',precio:1800,apu:{mo:950,eq:600,mat:250}},
            {cat:'movimiento',cod:'201.01',nombre:'Desbroce y limpieza',unidad:'ha',precio:8500,apu:{mo:2800,eq:5200,mat:500}},
            {cat:'movimiento',cod:'202.01',nombre:'Excavación no clasificada',unidad:'m³',precio:18.50,apu:{mo:4.20,eq:13.80,mat:0.50}},
            {cat:'movimiento',cod:'203.01',nombre:'Excavación en roca suelta',unidad:'m³',precio:38.20,apu:{mo:8.50,eq:28.20,mat:1.50}},
            {cat:'movimiento',cod:'204.01',nombre:'Excavación en roca fija',unidad:'m³',precio:62.00,apu:{mo:12.00,eq:45.00,mat:5.00}},
            {cat:'movimiento',cod:'205.01',nombre:'Conformación terraplenes',unidad:'m³',precio:22.40,apu:{mo:5.80,eq:15.60,mat:1.00}},
            {cat:'movimiento',cod:'206.01',nombre:'Perfilado y compactado subrasante',unidad:'m²',precio:3.80,apu:{mo:0.95,eq:2.65,mat:0.20}},
            {cat:'movimiento',cod:'207.01',nombre:'Mejoramiento suelos cal 3%',unidad:'m³',precio:85.00,apu:{mo:18.50,eq:32.50,mat:34.00}},
            {cat:'movimiento',cod:'208.01',nombre:'Eliminación material excedente d<1km',unidad:'m³',precio:12.50,apu:{mo:2.80,eq:9.20,mat:0.50}},
            {cat:'movimiento',cod:'208.02',nombre:'Eliminación material excedente d>1km',unidad:'m³-km',precio:4.20,apu:{mo:0.95,eq:3.10,mat:0.15}},
            {cat:'movimiento',cod:'209.01',nombre:'Relleno compactado material propio',unidad:'m³',precio:28.50,apu:{mo:7.20,eq:19.80,mat:1.50}},
            {cat:'movimiento',cod:'210.01',nombre:'Corte en material suelto',unidad:'m³',precio:15.80,apu:{mo:3.50,eq:11.80,mat:0.50}},
            {cat:'movimiento',cod:'211.01',nombre:'Escarificado 0.20m',unidad:'m²',precio:2.80,apu:{mo:0.60,eq:2.10,mat:0.10}},
            {cat:'pavimentos',cod:'401.01',nombre:'Capa anticontaminante e=0.15m',unidad:'m³',precio:35.00,apu:{mo:8.50,eq:14.50,mat:12.00}},
            {cat:'pavimentos',cod:'402.01',nombre:'Sub-base granular e=0.20m',unidad:'m³',precio:72.50,apu:{mo:15.80,eq:28.70,mat:28.00}},
            {cat:'pavimentos',cod:'403.01',nombre:'Base granular e=0.25m',unidad:'m³',precio:85.50,apu:{mo:18.50,eq:32.00,mat:35.00}},
            {cat:'pavimentos',cod:'404.01',nombre:'Base estabilizada cemento 3%',unidad:'m³',precio:165.00,apu:{mo:35.00,eq:58.00,mat:72.00}},
            {cat:'pavimentos',cod:'405.01',nombre:'Base asfáltica e=0.10m',unidad:'m³',precio:320.00,apu:{mo:55.00,eq:125.00,mat:140.00}},
            {cat:'pavimentos',cod:'406.01',nombre:'Imprimación asfáltica',unidad:'m²',precio:4.80,apu:{mo:0.85,eq:1.75,mat:2.20}},
            {cat:'pavimentos',cod:'407.01',nombre:'Riego liga asfalto diluido',unidad:'m²',precio:2.20,apu:{mo:0.45,eq:0.80,mat:0.95}},
            {cat:'pavimentos',cod:'408.01',nombre:'Tratamiento superficial monocapa',unidad:'m²',precio:18.50,apu:{mo:3.50,eq:6.80,mat:8.20}},
            {cat:'pavimentos',cod:'409.01',nombre:'Tratamiento superficial bicapa',unidad:'m²',precio:28.00,apu:{mo:5.80,eq:10.20,mat:12.00}},
            {cat:'pavimentos',cod:'410.01',nombre:'Sello asfáltico tipo slurry',unidad:'m²',precio:12.00,apu:{mo:2.20,eq:4.50,mat:5.30}},
            {cat:'pavimentos',cod:'411.01',nombre:'Sello fisuras asfalto caliente',unidad:'m',precio:3.50,apu:{mo:0.80,eq:1.20,mat:1.50}},
            {cat:'pavimentos',cod:'412.01',nombre:'Sello grietas c/geomalla',unidad:'m',precio:15.00,apu:{mo:3.20,eq:2.80,mat:9.00}},
            {cat:'pavimentos',cod:'413.01',nombre:'Parchado superficial MAC',unidad:'m²',precio:42.00,apu:{mo:8.50,eq:15.50,mat:18.00}},
            {cat:'pavimentos',cod:'414.01',nombre:'Parchado profundo base+MAC',unidad:'m²',precio:85.00,apu:{mo:18.00,eq:32.00,mat:35.00}},
            {cat:'pavimentos',cod:'415.01',nombre:'Fresado pavimento asfaltico e=5cm',unidad:'m²',precio:12.50,apu:{mo:2.50,eq:9.20,mat:0.80}},
            {cat:'pavimentos',cod:'416.01',nombre:'Pavimento concreto asfaltico caliente e=5cm',unidad:'m³',precio:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
            {cat:'pavimentos',cod:'416.02',nombre:'Pavimento concreto asfaltico caliente e=7.5cm',unidad:'m³',precio:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
            {cat:'pavimentos',cod:'416.03',nombre:'Pavimento concreto asfaltico caliente e=10cm',unidad:'m³',precio:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
            {cat:'pavimentos',cod:'417.01',nombre:'MAC modificado polimeros e=5cm',unidad:'m³',precio:1250.00,apu:{mo:225.00,eq:525.00,mat:500.00}},
            {cat:'pavimentos',cod:'418.01',nombre:'MAC reciclado 20% RAP e=7cm',unidad:'m³',precio:780.00,apu:{mo:155.00,eq:365.00,mat:260.00}},
            {cat:'pavimentos',cod:'419.01',nombre:'Pavimento asfaltico frio emulsión',unidad:'m³',precio:650.00,apu:{mo:125.00,eq:285.00,mat:240.00}},
            {cat:'pavimentos',cod:'421.01',nombre:'Micropavimento bicapa',unidad:'m²',precio:22.00,apu:{mo:4.50,eq:8.50,mat:9.00}},
            {cat:'pavimentos',cod:'422.01',nombre:'Pavimento concreto hidráulico fc=280 e=0.20m',unidad:'m³',precio:450.00,apu:{mo:95.00,eq:155.00,mat:200.00}},
            {cat:'pavimentos',cod:'423.01',nombre:'Pavimento adoquines concreto',unidad:'m²',precio:68.00,apu:{mo:22.00,eq:6.00,mat:40.00}},
            {cat:'pavimentos',cod:'424.01',nombre:'Pavimento adoquines piedra',unidad:'m²',precio:95.00,apu:{mo:32.00,eq:8.00,mat:55.00}},
            {cat:'pavimentos',cod:'425.01',nombre:'Reciclado in-situ base granular',unidad:'m³',precio:45.00,apu:{mo:9.50,eq:28.50,mat:7.00}},
            {cat:'pavimentos',cod:'426.01',nombre:'Estabilización suelos cemento',unidad:'m³',precio:95.00,apu:{mo:18.00,eq:35.00,mat:42.00}},
            {cat:'pavimentos',cod:'427.01',nombre:'Capa nivelación asfalto emulsión',unidad:'m³',precio:520.00,apu:{mo:85.00,eq:180.00,mat:255.00}},
            {cat:'drenaje',cod:'501.01',nombre:'Excavación estructuras material común',unidad:'m³',precio:28.00,apu:{mo:6.50,eq:20.00,mat:1.50}},
            {cat:'drenaje',cod:'502.01',nombre:'Excavación estructuras en roca',unidad:'m³',precio:55.00,apu:{mo:11.00,eq:40.00,mat:4.00}},
            {cat:'drenaje',cod:'503.01',nombre:'Relleno estructuras material propio',unidad:'m³',precio:25.00,apu:{mo:6.00,eq:17.50,mat:1.50}},
            {cat:'drenaje',cod:'504.01',nombre:'Alcantarilla TMC Ø36" L=6m',unidad:'m',precio:380.00,apu:{mo:85.00,eq:120.00,mat:175.00}},
            {cat:'drenaje',cod:'504.02',nombre:'Alcantarilla TMC Ø48" L=6m',unidad:'m',precio:520.00,apu:{mo:115.00,eq:155.00,mat:250.00}},
            {cat:'drenaje',cod:'505.01',nombre:'Alcantarilla marco concreto 1.00x1.00m',unidad:'m',precio:850.00,apu:{mo:245.00,eq:185.00,mat:420.00}},
            {cat:'drenaje',cod:'506.01',nombre:'Cabezal alcantarilla TMC tipo I',unidad:'und',precio:2500,apu:{mo:680.00,eq:520.00,mat:1300}},
            {cat:'drenaje',cod:'507.01',nombre:'Subdrén Ø4" PVC + filtro',unidad:'m',precio:45.00,apu:{mo:12.00,eq:8.50,mat:24.50}},
            {cat:'drenaje',cod:'508.01',nombre:'Cunetas triangulares sin revestir',unidad:'m',precio:8.00,apu:{mo:2.20,eq:5.30,mat:0.50}},
            {cat:'drenaje',cod:'509.01',nombre:'Cunetas revestidas concreto fc=175',unidad:'m',precio:42.00,apu:{mo:12.50,eq:8.50,mat:21.00}},
            {cat:'drenaje',cod:'510.01',nombre:'Zanjas coronación sin revestir',unidad:'m',precio:12.00,apu:{mo:3.50,eq:7.80,mat:0.70}},
            {cat:'drenaje',cod:'511.01',nombre:'Badenes concreto fc=210 e=0.30m',unidad:'m²',precio:185.00,apu:{mo:52.00,eq:38.00,mat:95.00}},
            {cat:'drenaje',cod:'512.01',nombre:'Pontones concreto armado L=6m',unidad:'m',precio:12000,apu:{mo:3200,eq:2800,mat:6000}},
            {cat:'drenaje',cod:'513.01',nombre:'Cunetas profundas triangulares',unidad:'m',precio:15.50,apu:{mo:4.20,eq:9.80,mat:1.50}},
            {cat:'drenaje',cod:'514.01',nombre:'Canal alivio concreto 0.40x0.40m',unidad:'m',precio:95.00,apu:{mo:28.50,eq:15.50,mat:51.00}},
            {cat:'drenaje',cod:'515.01',nombre:'Sumideros rejilla HF 0.60x0.60m',unidad:'und',precio:850.00,apu:{mo:280.00,eq:120.00,mat:450.00}},
            {cat:'obras_arte',cod:'601.01',nombre:'Mampostería piedra',unidad:'m³',precio:280.00,apu:{mo:95.00,eq:35.00,mat:150.00}},
            {cat:'obras_arte',cod:'602.01',nombre:'Muro concreto ciclopeo fc=175+30%PG',unidad:'m³',precio:320.00,apu:{mo:105.00,eq:45.00,mat:170.00}},
            {cat:'obras_arte',cod:'603.01',nombre:'Muro concreto armado fc=210',unidad:'m³',precio:650.00,apu:{mo:220.00,eq:130.00,mat:300.00}},
            {cat:'obras_arte',cod:'604.01',nombre:'Gaviones caja 2x1x1m',unidad:'m³',precio:180.00,apu:{mo:52.00,eq:28.00,mat:100.00}},
            {cat:'obras_arte',cod:'604.02',nombre:'Gaviones colchón 0.30m',unidad:'m²',precio:95.00,apu:{mo:28.00,eq:15.00,mat:52.00}},
            {cat:'obras_arte',cod:'605.01',nombre:'Defensas ribereñas enrocado',unidad:'m³',precio:85.00,apu:{mo:22.00,eq:48.00,mat:15.00}},
            {cat:'obras_arte',cod:'606.01',nombre:'Demolición concreto simple',unidad:'m³',precio:45.00,apu:{mo:12.00,eq:31.00,mat:2.00}},
            {cat:'obras_arte',cod:'606.02',nombre:'Demolición concreto armado',unidad:'m³',precio:85.00,apu:{mo:22.00,eq:60.00,mat:3.00}},
            {cat:'obras_arte',cod:'607.01',nombre:'Geomalla biaxial 40kN/m',unidad:'m²',precio:12.50,apu:{mo:2.50,eq:0.80,mat:9.20}},
            {cat:'obras_arte',cod:'608.01',nombre:'Geotextil NT-2000',unidad:'m²',precio:4.80,apu:{mo:0.80,eq:0.20,mat:3.80}},
            {cat:'obras_arte',cod:'609.01',nombre:'Geomembrana HDPE 1.5mm',unidad:'m²',precio:18.50,apu:{mo:3.50,eq:1.00,mat:14.00}},
            {cat:'obras_arte',cod:'610.01',nombre:'Protección taludes semilla+fertilizante',unidad:'m²',precio:8.50,apu:{mo:2.80,eq:1.50,mat:4.20}},
            {cat:'obras_arte',cod:'611.01',nombre:'Concreto lanzado shotcrete e=5cm',unidad:'m²',precio:85.00,apu:{mo:22.00,eq:28.00,mat:35.00}},
            {cat:'obras_arte',cod:'612.01',nombre:'Anclajes terreno 3m Ø1"',unidad:'und',precio:280.00,apu:{mo:85.00,eq:95.00,mat:100.00}},
            {cat:'señalizacion',cod:'801.01',nombre:'Señal vertical reglamentaria 0.60x0.60m',unidad:'und',precio:280.00,apu:{mo:52.00,eq:28.00,mat:200.00}},
            {cat:'señalizacion',cod:'801.02',nombre:'Señal vertical preventiva 0.75x0.75m',unidad:'und',precio:320.00,apu:{mo:58.00,eq:32.00,mat:230.00}},
            {cat:'señalizacion',cod:'801.03',nombre:'Señal informativa 2.40x1.20m',unidad:'und',precio:1200,apu:{mo:225.00,eq:125.00,mat:850.00}},
            {cat:'señalizacion',cod:'802.01',nombre:'Poste soporte señal Ø2" h=3m',unidad:'und',precio:180.00,apu:{mo:42.00,eq:28.00,mat:110.00}},
            {cat:'señalizacion',cod:'803.01',nombre:'Marcas pavimento pintura tráfico continua 0.10m',unidad:'m',precio:1.80,apu:{mo:0.35,eq:0.65,mat:0.80}},
            {cat:'señalizacion',cod:'803.02',nombre:'Marcas pavimento pintura tráfico discontinua',unidad:'m',precio:1.50,apu:{mo:0.30,eq:0.55,mat:0.65}},
            {cat:'señalizacion',cod:'804.01',nombre:'Símbolos y leyendas pavimento',unidad:'m²',precio:28.50,apu:{mo:5.80,eq:8.70,mat:14.00}},
            {cat:'señalizacion',cod:'805.01',nombre:'Tachas reflectivas bidireccional',unidad:'und',precio:18.00,apu:{mo:2.50,eq:1.50,mat:14.00}},
            {cat:'señalizacion',cod:'806.01',nombre:'Delineadores Ø4" h=1.20m',unidad:'und',precio:95.00,apu:{mo:18.00,eq:12.00,mat:65.00}},
            {cat:'señalizacion',cod:'807.01',nombre:'Guardavías metálico doble onda',unidad:'m',precio:180.00,apu:{mo:38.00,eq:32.00,mat:110.00}},
            {cat:'señalizacion',cod:'808.01',nombre:'Hitos kilométricos concreto',unidad:'und',precio:220.00,apu:{mo:65.00,eq:35.00,mat:120.00}},
            {cat:'señalizacion',cod:'809.01',nombre:'Postes SOS h=3m c/panel solar',unidad:'und',precio:4500,apu:{mo:850.00,eq:450.00,mat:3200}},
            {cat:'señalizacion',cod:'810.01',nombre:'Captafaros bidireccional alto tráfico',unidad:'und',precio:28.00,apu:{mo:3.50,eq:1.50,mat:23.00}},
            {cat:'señalizacion',cod:'811.01',nombre:'Barreras new jersey concreto',unidad:'m',precio:185.00,apu:{mo:52.00,eq:38.00,mat:95.00}},
            {cat:'señalizacion',cod:'812.01',nombre:'Marcas pavimento termoplástico',unidad:'m²',precio:45.00,apu:{mo:8.50,eq:12.50,mat:24.00}}
        ];

        let presupuesto = [];

        function cargarPartidas() {
            const cat = document.getElementById('categoria').value;
            const select = document.getElementById('partida');
            select.innerHTML = '';

            const filtered = cat ? partidasDB.filter(p => p.cat === cat) : partidasDB;

            if (filtered.length === 0) {
                select.innerHTML = '<option value="">❌ No hay partidas disponibles</option>';
                return;
            }

            filtered.forEach(p => {
                const option = document.createElement('option');
                option.value = p.cod;
                option.textContent = `${p.cod} | ${p.nombre} | ${p.unidad} | S/ ${p.precio.toFixed(2)}`;
                select.appendChild(option);
            });
        }

        document.getElementById('categoria').addEventListener('change', cargarPartidas);

        const buscar = document.getElementById('buscar');
        const autocomplete = document.getElementById('autocomplete');

        buscar.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if(query.length < 2) {
                autocomplete.style.display = 'none';
                return;
            }

            const results = partidasDB.filter(p => 
                p.nombre.toLowerCase().includes(query) || 
                p.cod.toLowerCase().includes(query)
            );

            if(results.length > 0) {
                autocomplete.innerHTML = results.slice(0, 8).map(p => 
                    `<div class="autocomplete-item" onclick="seleccionarPartida('${p.cod}')">${p.cod} - ${p.nombre}</div>`
                ).join('');
                autocomplete.style.display = 'block';
            } else {
                autocomplete.style.display = 'none';
            }
        });

        function seleccionarPartida(cod) {
            document.getElementById('partida').value = cod;
            document.getElementById('buscar').value = '';
            autocomplete.style.display = 'none';
            mostrarAPU(cod);
        }

        document.getElementById('partida').addEventListener('change', function() {
            const cod = this.value;
            if(cod) mostrarAPU(cod);
        });

        function mostrarAPU(cod) {
            const partida = partidasDB.find(p => p.cod === cod);
            if(!partida || !partida.apu) return;

            const panel = document.getElementById('apuPanel');
            const content = document.getElementById('apuContent');

            const total = partida.precio;
            const moPorc = ((partida.apu.mo / total) * 100).toFixed(1);
            const eqPorc = ((partida.apu.eq / total) * 100).toFixed(1);
            const matPorc = ((partida.apu.mat / total) * 100).toFixed(1);

            content.innerHTML = `
                <div class="apu-header">
                    <strong style="color: var(--accent-cyan); font-size: 1.1rem;">${partida.cod}</strong>
                    <div style="color: var(--text-primary); margin-top: 0.5rem; font-weight: 500;">${partida.nombre}</div>
                    <div style="color: var(--text-muted); margin-top: 0.25rem; font-size: 0.9rem;">Unidad: ${partida.unidad}</div>
                </div>

                <div class="apu-price">
                    <div class="apu-price-value">S/ ${total.toFixed(2)}</div>
                    <div class="apu-price-label">Precio Unitario Total</div>
                </div>

                <div class="apu-breakdown">
                    <div class="apu-item-header">
                        <span class="apu-item-name">👷 Mano de Obra</span>
                        <span class="apu-item-value">S/ ${partida.apu.mo.toFixed(2)}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill progress-mo" style="width: ${moPorc}%;"></div>
                    </div>
                    <div class="apu-percentage">${moPorc}%</div>
                </div>

                <div class="apu-breakdown">
                    <div class="apu-item-header">
                        <span class="apu-item-name">🚜 Equipos</span>
                        <span class="apu-item-value">S/ ${partida.apu.eq.toFixed(2)}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill progress-eq" style="width: ${eqPorc}%;"></div>
                    </div>
                    <div class="apu-percentage">${eqPorc}%</div>
                </div>

                <div class="apu-breakdown">
                    <div class="apu-item-header">
                        <span class="apu-item-name">📦 Materiales</span>
                        <span class="apu-item-value">S/ ${partida.apu.mat.toFixed(2)}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill progress-mat" style="width: ${matPorc}%;"></div>
                    </div>
                    <div class="apu-percentage">${matPorc}%</div>
                </div>
            `;

            panel.style.display = 'block';
        }

        function agregarPartida() {
            const cod = document.getElementById('partida').value;
            const metrado = parseFloat(document.getElementById('metrado').value);

            if(!cod || !metrado || metrado <= 0) {
                alert('⚠️ Selecciona una partida e ingresa un metrado válido mayor a 0');
                return;
            }

            const partida = partidasDB.find(p => p.cod === cod);
            if (!partida) {
                alert('⚠️ Partida no encontrada en la base de datos');
                return;
            }

            const parcial = metrado * partida.precio;

            presupuesto.push({
                cod: partida.cod,
                nombre: partida.nombre,
                unidad: partida.unidad,
                metrado: metrado,
                precio: partida.precio,
                parcial: parcial
            });

            document.getElementById('metrado').value = '';
            renderizarTabla();
        }

        function renderizarTabla() {
            const tbody = document.getElementById('tbody');
            tbody.innerHTML = '';

            if (presupuesto.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                            No hay partidas agregadas. Comienza seleccionando partidas arriba.
                        </td>
                    </tr>
                `;
                actualizarTotales(0);
                return;
            }

            let directo = 0;
            presupuesto.forEach((p, idx) => {
                directo += p.parcial;
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${p.cod}</strong> - ${p.nombre}</td>
                        <td>${p.unidad}</td>
                        <td>${p.metrado.toFixed(2)}</td>
                        <td>S/ ${p.precio.toFixed(2)}</td>
                        <td><strong>S/ ${p.parcial.toFixed(2)}</strong></td>
                        <td>
                            <button onclick="eliminar(${idx})" class="btn-danger" style="padding: 0.5rem 1rem;">
                                ❌ Eliminar
                            </button>
                        </td>
                    </tr>
                `;
            });

            actualizarTotales(directo);
        }

        function actualizarTotales(directo) {
            const gg = directo * 0.10;
            const util = directo * 0.08;
            const total = directo + gg + util;

            document.getElementById('tdDirecto').innerHTML = `<strong>S/ ${directo.toFixed(2)}</strong>`;
            document.getElementById('tdGG').textContent = `S/ ${gg.toFixed(2)}`;
            document.getElementById('tdUtil').textContent = `S/ ${util.toFixed(2)}`;
            document.getElementById('tdTotal').innerHTML = `<strong>S/ ${total.toFixed(2)}</strong>`;

            document.getElementById('costoDirecto').textContent = `S/ ${directo.toLocaleString('es-PE', {maximumFractionDigits: 0})}`;
            document.getElementById('total').textContent = `S/ ${total.toLocaleString('es-PE', {maximumFractionDigits: 0})}`;
            document.getElementById('numPartidas').textContent = presupuesto.length;
        }

        function eliminar(idx) {
            if (confirm('¿Eliminar esta partida del presupuesto?')) {
                presupuesto.splice(idx, 1);
                renderizarTabla();
            }
        }

        function limpiar() {
            if(confirm('⚠️ ¿Estás seguro de borrar TODO el presupuesto? Esta acción no se puede deshacer.')) {
                presupuesto = [];
                renderizarTabla();
            }
        }

        function exportarCSV() {
            if(presupuesto.length === 0) {
                alert('⚠️ Agrega al menos una partida antes de exportar');
                return;
            }

            let csv = 'Código,Partida,Unidad,Metrado,P.U. (S/),Parcial (S/)\n';
            presupuesto.forEach(p => {
                csv += `${p.cod},"${p.nombre}",${p.unidad},${p.metrado},${p.precio},${p.parcial}\n`;
            });

            const directo = presupuesto.reduce((sum, p) => sum + p.parcial, 0);
            const gg = directo * 0.10;
            const util = directo * 0.08;
            const total = directo + gg + util;

            csv += `\n,COSTO DIRECTO,,,,${directo.toFixed(2)}\n`;
            csv += `,Gastos Generales (10%),,,,${gg.toFixed(2)}\n`;
            csv += `,Utilidad (8%),,,,${util.toFixed(2)}\n`;
            csv += `,TOTAL PRESUPUESTO,,,,${total.toFixed(2)}\n`;

            const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const fecha = new Date().toISOString().split('T')[0];
            a.download = `presupuesto_vial_SEACE_${fecha}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function exportarPDF() {
            alert('📄 Exportación PDF en desarrollo.\n\nPor ahora:\n1. Descarga el CSV\n2. Ábrelo en Excel/Google Sheets\n3. Exporta como PDF desde ahí');
        }

        // Inicializar
        window.addEventListener('load', function() {
            cargarPartidas();
            renderizarTabla();
        });
    </script>
</body>
</html>
"""

components.html(html_content, height=1300, scrolling=True)
