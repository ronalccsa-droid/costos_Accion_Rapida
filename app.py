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
    <title>Calculadora Vial SEACE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            color: #667eea;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .subtitle {
            color: #64748b;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr 450px;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #e2e8f0;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        select, input {
            width: 100%;
            padding: 0.875rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            margin-bottom: 1rem;
            transition: all 0.2s;
        }

        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.875rem 1.5rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            width: 100%;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .btn-danger { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
        .btn-warning { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }

        .metric {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 2px solid #bae6fd;
        }

        .metric-label {
            color: #0369a1;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            color: #0c4a6e;
            font-size: 2rem;
            font-weight: 800;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }

        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            background: #f8fafc;
            color: #1e293b;
            font-weight: 700;
            font-size: 0.875rem;
            text-transform: uppercase;
        }

        tbody tr:hover {
            background: #f8fafc;
        }

        tfoot tr {
            background: #f1f5f9;
            font-weight: 600;
        }

        tfoot tr:last-child {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 700;
        }

        .apu-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }

        .apu-price {
            font-size: 2rem;
            font-weight: 800;
        }

        .apu-item {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        }

        .progress {
            background: rgba(255,255,255,0.2);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin: 0.5rem 0;
        }

        .progress-bar {
            background: white;
            height: 100%;
            transition: width 0.5s;
        }

        .action-btns {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .action-btns button {
            flex: 1;
        }

        .autocomplete {
            position: relative;
        }

        .autocomplete-list {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .autocomplete-item {
            padding: 0.875rem;
            cursor: pointer;
            border-bottom: 1px solid #f1f5f9;
        }

        .autocomplete-item:hover {
            background: #f8fafc;
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #64748b;
        }

        @media (max-width: 1200px) {
            .grid { grid-template-columns: 1fr 1fr; }
            .card:last-child { grid-column: 1 / -1; }
        }

        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            .action-btns { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛣️ Calculadora Vial SEACE</h1>
        <p class="subtitle">Base de datos MTC 2026 con 90+ partidas oficiales | Precios actualizados</p>

        <div class="grid">
            <div class="card">
                <h2 class="card-title">📋 Selección de Partidas</h2>
                <select id="categoria">
                    <option value="">📊 Todas las categorías</option>
                    <option value="preliminares">🏗️ Trabajos Preliminares</option>
                    <option value="movimiento">⛏️ Movimiento de Tierras</option>
                    <option value="pavimentos">🛣️ Pavimentos</option>
                    <option value="drenaje">💧 Drenaje</option>
                    <option value="señalizacion">🚦 Señalización</option>
                    <option value="obras_arte">🏛️ Obras de Arte</option>
                </select>

                <div class="autocomplete">
                    <input type="text" id="buscar" placeholder="🔍 Buscar partida...">
                    <div id="autocompleteList" class="autocomplete-list"></div>
                </div>

                <select id="partida" size="8" style="height: 280px;"></select>
                <input type="number" id="metrado" placeholder="Metrado (cantidad)" min="0" step="0.01">
                <button onclick="agregarPartida()" class="btn-success">➕ Agregar al Presupuesto</button>
            </div>

            <div class="card">
                <h2 class="card-title">💰 Resumen Financiero</h2>
                <div class="metric">
                    <div class="metric-label">💵 Costo Directo</div>
                    <div class="metric-value" id="costoDirecto">S/ 0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">📊 Total + GG + Utilidad</div>
                    <div class="metric-value" id="total">S/ 0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">📦 Partidas</div>
                    <div class="metric-value" id="numPartidas">0</div>
                </div>
            </div>

            <div class="card" id="apuPanel" style="display: none;">
                <h2 class="card-title">🔍 Análisis Unitario</h2>
                <div id="apuContent"></div>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">📊 Presupuesto Detallado</h2>
            <div class="action-btns">
                <button onclick="exportarCSV()" class="btn-success">📥 Descargar CSV</button>
                <button onclick="exportarPDF()" class="btn-warning">📄 Generar PDF</button>
                <button onclick="limpiar()" class="btn-danger">🗑️ Limpiar Todo</button>
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
                    <tr><td colspan="6" class="empty-state">No hay partidas. Comienza agregando arriba.</td></tr>
                </tbody>
                <tfoot>
                    <tr><td colspan="4">COSTO DIRECTO</td><td id="tdDirecto">S/ 0.00</td><td></td></tr>
                    <tr><td colspan="4">Gastos Generales (10%)</td><td id="tdGG">S/ 0.00</td><td></td></tr>
                    <tr><td colspan="4">Utilidad (8%)</td><td id="tdUtil">S/ 0.00</td><td></td></tr>
                    <tr><td colspan="4">TOTAL PRESUPUESTO</td><td id="tdTotal">S/ 0.00</td><td></td></tr>
                </tfoot>
            </table>
        </div>
    </div>

    <script>
        const partidas = [
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
            const sel = document.getElementById('partida');
            const cat = document.getElementById('categoria').value;
            const filtradas = cat ? partidas.filter(p => p.cat === cat) : partidas;

            sel.innerHTML = '';
            filtradas.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p.cod;
                opt.textContent = p.cod + ' - ' + p.nombre + ' (' + p.unidad + ') S/ ' + p.precio.toFixed(2);
                sel.appendChild(opt);
            });
        }

        document.getElementById('categoria').onchange = cargarPartidas;

        document.getElementById('buscar').oninput = function() {
            const q = this.value.toLowerCase();
            const lista = document.getElementById('autocompleteList');

            if (q.length < 2) {
                lista.style.display = 'none';
                return;
            }

            const res = partidas.filter(p => p.nombre.toLowerCase().includes(q) || p.cod.toLowerCase().includes(q));

            if (res.length > 0) {
                lista.innerHTML = res.slice(0, 8).map(p => 
                    '<div class="autocomplete-item" onclick="selPartida(\'' + p.cod + '\')">' + 
                    p.cod + ' - ' + p.nombre + '</div>'
                ).join('');
                lista.style.display = 'block';
            } else {
                lista.style.display = 'none';
            }
        };

        function selPartida(cod) {
            document.getElementById('partida').value = cod;
            document.getElementById('buscar').value = '';
            document.getElementById('autocompleteList').style.display = 'none';
            mostrarAPU(cod);
        }

        document.getElementById('partida').onchange = function() {
            if (this.value) mostrarAPU(this.value);
        };

        function mostrarAPU(cod) {
            const p = partidas.find(x => x.cod === cod);
            if (!p) return;

            const moP = ((p.apu.mo / p.precio) * 100).toFixed(1);
            const eqP = ((p.apu.eq / p.precio) * 100).toFixed(1);
            const matP = ((p.apu.mat / p.precio) * 100).toFixed(1);

            document.getElementById('apuContent').innerHTML = 
                '<div class="apu-box"><div class="apu-price">S/ ' + p.precio.toFixed(2) + 
                '</div><div style="font-size:0.875rem;opacity:0.9;">Precio Unitario</div></div>' +
                '<div><strong>' + p.cod + '</strong> - ' + p.nombre + '</div>' +
                '<div style="color:#64748b;margin:0.5rem 0;">Unidad: ' + p.unidad + '</div>' +
                '<div class="apu-item"><div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">' +
                '<span>👷 Mano Obra</span><strong>S/ ' + p.apu.mo.toFixed(2) + '</strong></div>' +
                '<div class="progress"><div class="progress-bar" style="width:' + moP + '%"></div></div>' +
                '<div style="text-align:right;font-size:0.8rem;opacity:0.8;">' + moP + '%</div></div>' +
                '<div class="apu-item"><div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">' +
                '<span>🚜 Equipos</span><strong>S/ ' + p.apu.eq.toFixed(2) + '</strong></div>' +
                '<div class="progress"><div class="progress-bar" style="width:' + eqP + '%"></div></div>' +
                '<div style="text-align:right;font-size:0.8rem;opacity:0.8;">' + eqP + '%</div></div>' +
                '<div class="apu-item"><div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">' +
                '<span>📦 Materiales</span><strong>S/ ' + p.apu.mat.toFixed(2) + '</strong></div>' +
                '<div class="progress"><div class="progress-bar" style="width:' + matP + '%"></div></div>' +
                '<div style="text-align:right;font-size:0.8rem;opacity:0.8;">' + matP + '%</div></div>';

            document.getElementById('apuPanel').style.display = 'block';
        }

        function agregarPartida() {
            const cod = document.getElementById('partida').value;
            const met = parseFloat(document.getElementById('metrado').value);

            if (!cod || !met || met <= 0) {
                alert('⚠️ Selecciona partida e ingresa metrado válido');
                return;
            }

            const p = partidas.find(x => x.cod === cod);
            if (!p) return;

            presupuesto.push({
                cod: p.cod,
                nombre: p.nombre,
                unidad: p.unidad,
                metrado: met,
                precio: p.precio,
                parcial: met * p.precio
            });

            document.getElementById('metrado').value = '';
            actualizar();
        }

        function actualizar() {
            const tb = document.getElementById('tbody');

            if (presupuesto.length === 0) {
                tb.innerHTML = '<tr><td colspan="6" class="empty-state">No hay partidas. Comienza agregando arriba.</td></tr>';
                document.getElementById('tdDirecto').textContent = 'S/ 0.00';
                document.getElementById('tdGG').textContent = 'S/ 0.00';
                document.getElementById('tdUtil').textContent = 'S/ 0.00';
                document.getElementById('tdTotal').textContent = 'S/ 0.00';
                document.getElementById('costoDirecto').textContent = 'S/ 0';
                document.getElementById('total').textContent = 'S/ 0';
                document.getElementById('numPartidas').textContent = '0';
                return;
            }

            let dir = 0;
            tb.innerHTML = presupuesto.map((p, i) => {
                dir += p.parcial;
                return '<tr><td><strong>' + p.cod + '</strong> - ' + p.nombre + '</td><td>' + 
                    p.unidad + '</td><td>' + p.metrado.toFixed(2) + '</td><td>S/ ' + 
                    p.precio.toFixed(2) + '</td><td><strong>S/ ' + p.parcial.toFixed(2) + 
                    '</strong></td><td><button onclick="eliminar(' + i + 
                    ')" style="width:auto;padding:0.5rem 1rem;" class="btn-danger">❌</button></td></tr>';
            }).join('');

            const gg = dir * 0.10;
            const ut = dir * 0.08;
            const tot = dir + gg + ut;

            document.getElementById('tdDirecto').textContent = 'S/ ' + dir.toFixed(2);
            document.getElementById('tdGG').textContent = 'S/ ' + gg.toFixed(2);
            document.getElementById('tdUtil').textContent = 'S/ ' + ut.toFixed(2);
            document.getElementById('tdTotal').textContent = 'S/ ' + tot.toFixed(2);
            document.getElementById('costoDirecto').textContent = 'S/ ' + Math.round(dir).toLocaleString('es-PE');
            document.getElementById('total').textContent = 'S/ ' + Math.round(tot).toLocaleString('es-PE');
            document.getElementById('numPartidas').textContent = presupuesto.length;
        }

        function eliminar(i) {
            if (confirm('¿Eliminar esta partida?')) {
                presupuesto.splice(i, 1);
                actualizar();
            }
        }

        function limpiar() {
            if (confirm('⚠️ ¿Borrar TODO el presupuesto?')) {
                presupuesto = [];
                actualizar();
            }
        }

        function exportarCSV() {
            if (presupuesto.length === 0) {
                alert('⚠️ Agrega partidas antes de exportar');
                return;
            }

            let csv = 'Código,Partida,Unidad,Metrado,P.U.,Parcial\n';
            let dir = 0;
            presupuesto.forEach(p => {
                csv += p.cod + ',"' + p.nombre + '",' + p.unidad + ',' + p.metrado + ',' + p.precio + ',' + p.parcial + '\n';
                dir += p.parcial;
            });

            const gg = dir * 0.10;
            const ut = dir * 0.08;
            const tot = dir + gg + ut;

            csv += '\n,COSTO DIRECTO,,,,'+dir.toFixed(2)+'\n';
            csv += ',Gastos Generales 10%,,,,'+gg.toFixed(2)+'\n';
            csv += ',Utilidad 8%,,,,'+ut.toFixed(2)+'\n';
            csv += ',TOTAL PRESUPUESTO,,,,'+tot.toFixed(2)+'\n';

            const blob = new Blob([csv], {type: 'text/csv'});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'presupuesto_' + new Date().toISOString().split('T')[0] + '.csv';
            a.click();
        }

        function exportarPDF() {
            alert('📄 Para PDF:\n1. Descarga CSV\n2. Abre en Excel\n3. Exporta como PDF');
        }

        cargarPartidas();
        actualizar();
    </script>
</body>
</html>
"""

components.html(html_content, height=1300, scrolling=True)
