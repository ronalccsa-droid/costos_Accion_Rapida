import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Calculadora Vial SEACE",
    page_icon="🛣️",
    layout="wide"
)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Vial SEACE - Base Datos Completa</title>
    <style>
        :root {
            --color-bg: #0f172a;
            --color-surface: #1e293b;
            --color-text: #f1f5f9;
            --color-accent: #38bdf8;
            --color-border: #334155;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--color-bg);
            color: var(--color-text);
            padding: 2rem;
        }
        h1 { color: var(--color-accent); margin-bottom: 1rem; }
        h2 { color: var(--color-accent); margin: 1.5rem 0 1rem; font-size: 1.3rem; }
        .container { max-width: 1400px; margin: 0 auto; }
        .card {
            background: var(--color-surface);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--color-border);
        }
        select, input {
            width: 100%;
            padding: 0.75rem;
            background: var(--color-bg);
            color: var(--color-text);
            border: 1px solid var(--color-border);
            border-radius: 6px;
            margin-bottom: 1rem;
            font-size: 1rem;
        }
        button {
            background: var(--color-accent);
            color: var(--color-bg);
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            margin-right: 0.5rem;
            font-size: 1rem;
        }
        button:hover { opacity: 0.9; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            background: var(--color-surface);
        }
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }
        th { background: var(--color-bg); color: var(--color-accent); font-weight: 600; }
        .metric {
            display: inline-block;
            background: var(--color-bg);
            padding: 1rem 1.5rem;
            border-radius: 6px;
            margin-right: 1rem;
            margin-bottom: 0.5rem;
        }
        .metric-label { font-size: 0.9rem; color: #94a3b8; }
        .metric-value { font-size: 1.8rem; font-weight: 700; color: var(--color-accent); }
        .search-box { position: relative; margin-bottom: 1rem; }
        .autocomplete {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--color-surface);
            border: 1px solid var(--color-border);
            border-radius: 6px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        }
        .autocomplete div {
            padding: 0.75rem;
            cursor: pointer;
            border-bottom: 1px solid var(--color-border);
        }
        .autocomplete div:hover { background: var(--color-bg); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛣️ Calculadora Presupuestos Vial - Base SEACE/MTC 2026</h1>
        <p style="color: #94a3b8; margin-bottom: 2rem;">90+ partidas oficiales MTC con precios mercado actualizados</p>

        <div style="display: grid; grid-template-columns: 1fr 1fr 400px; gap: 1.5rem; margin-bottom: 2rem;">
            <div class="card">
                <h2>📋 Selección de Partidas</h2>
                <select id="categoria">
                    <option value="">Filtrar por categoría...</option>
                    <option value="preliminares">Trabajos Preliminares</option>
                    <option value="movimiento">Movimiento Tierras</option>
                    <option value="pavimentos">Pavimentos</option>
                    <option value="drenaje">Drenaje</option>
                    <option value="señalizacion">Señalización</option>
                    <option value="obras_arte">Obras de Arte</option>
                </select>
                
                <div class="search-box">
                    <input type="text" id="buscar" placeholder="🔍 Buscar partida por nombre...">
                    <div id="autocomplete" class="autocomplete"></div>
                </div>

                <select id="partida" size="10" style="height: 300px;">
                    <option value="">Selecciona partidas...</option>
                </select>
                
                <input type="number" id="metrado" placeholder="Metrado (cantidad)" min="0" step="0.01">
                <button onclick="agregarPartida()">➕ Agregar al Presupuesto</button>
            </div>

            <div class="card">
                <h2>💰 Métricas</h2>
                <div class="metric">
                    <div class="metric-label">Costo Directo</div>
                    <div class="metric-value" id="costoDirecto">S/ 0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total + GG+Util.</div>
                    <div class="metric-value" id="total">S/ 0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Partidas</div>
                    <div class="metric-value" id="numPartidas">0</div>
                </div>
            </div>

            <div class="card" id="apuPanel" style="display: none;">
                <h2>🔍 Análisis Unitario</h2>
                <div id="apuContent" style="font-size: 0.9rem;">
                    <p style="color: #94a3b8;">Selecciona una partida para ver su análisis de precios unitarios</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>📊 Presupuesto Actual</h2>
            <button onclick="exportarCSV()">📥 Descargar CSV</button>
            <button onclick="exportarPDF()">📄 Generar PDF</button>
            <button onclick="limpiar()">🗑️ Limpiar Todo</button>
            
            <table id="tablaPresupuesto">
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
                <tbody id="tbody"></tbody>
                <tfoot>
                    <tr style="font-weight: 700; background: var(--color-bg);">
                        <td colspan="4">TOTAL DIRECTO</td>
                        <td id="tdDirecto">S/ 0.00</td>
                        <td></td>
                    </tr>
                    <tr style="background: var(--color-bg);">
                        <td colspan="4">Gastos Generales (10%)</td>
                        <td id="tdGG">S/ 0.00</td>
                        <td></td>
                    </tr>
                    <tr style="background: var(--color-bg);">
                        <td colspan="4">Utilidad (8%)</td>
                        <td id="tdUtil">S/ 0.00</td>
                        <td></td>
                    </tr>
                    <tr style="font-weight: 700; background: var(--color-accent); color: var(--color-bg);">
                        <td colspan="4">TOTAL PRESUPUESTO</td>
                        <td id="tdTotal">S/ 0.00</td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </div>

    <script>
        const partidasDB = [
            // TRABAJOS PRELIMINARES
            {cat: 'preliminares', cod: '101.01', nombre: 'Movilización y desmovilización equipos', unidad: 'glb', precio: 45000, apu: {mo: 8500, eq: 32000, mat: 4500}},
            {cat: 'preliminares', cod: '102.01', nombre: 'Topografía y georeferenciación', unidad: 'km', precio: 2500, apu: {mo: 1200, eq: 900, mat: 400}},
            {cat: 'preliminares', cod: '103.01', nombre: 'Campamento provisional obra', unidad: 'mes', precio: 12000, apu: {mo: 4500, eq: 2500, mat: 5000}},
            {cat: 'preliminares', cod: '104.01', nombre: 'Cartel obra 3.60x7.20m', unidad: 'und', precio: 3500, apu: {mo: 450, eq: 250, mat: 2800}},
            {cat: 'preliminares', cod: '105.01', nombre: 'Mantenimiento tránsito temporal', unidad: 'mes', precio: 8500, apu: {mo: 5200, eq: 1800, mat: 1500}},
            {cat: 'preliminares', cod: '106.01', nombre: 'Nivelación y replanteo', unidad: 'km', precio: 1800, apu: {mo: 950, eq: 600, mat: 250}},
            
            // MOVIMIENTO TIERRAS
            {cat: 'movimiento', cod: '201.01', nombre: 'Desbroce y limpieza', unidad: 'ha', precio: 8500, apu: {mo: 2800, eq: 5200, mat: 500}},
            {cat: 'movimiento', cod: '202.01', nombre: 'Excavación no clasificada', unidad: 'm³', precio: 18.50, apu: {mo: 4.20, eq: 13.80, mat: 0.50}},
            {cat: 'movimiento', cod: '203.01', nombre: 'Excavación en roca suelta', unidad: 'm³', precio: 38.20, apu: {mo: 8.50, eq: 28.20, mat: 1.50}},
            {cat: 'movimiento', cod: '204.01', nombre: 'Excavación en roca fija', unidad: 'm³', precio: 62.00, apu: {mo: 12.00, eq: 45.00, mat: 5.00}},
            {cat: 'movimiento', cod: '205.01', nombre: 'Conformación terraplenes', unidad: 'm³', precio: 22.40, apu: {mo: 5.80, eq: 15.60, mat: 1.00}},
            {cat: 'movimiento', cod: '206.01', nombre: 'Perfilado y compactado subrasante', unidad: 'm²', precio: 3.80, apu: {mo: 0.95, eq: 2.65, mat: 0.20}},
            {cat: 'movimiento', cod: '207.01', nombre: 'Mejoramiento suelos cal 3%', unidad: 'm³', precio: 85.00, apu: {mo: 18.50, eq: 32.50, mat: 34.00}},
            {cat: 'movimiento', cod: '208.01', nombre: 'Eliminación material excedente d<1km', unidad: 'm³', precio: 12.50, apu: {mo: 2.80, eq: 9.20, mat: 0.50}},
            {cat: 'movimiento', cod: '208.02', nombre: 'Eliminación material excedente d>1km', unidad: 'm³-km', precio: 4.20, apu: {mo: 0.95, eq: 3.10, mat: 0.15}},
            {cat: 'movimiento', cod: '209.01', nombre: 'Relleno compactado material propio', unidad: 'm³', precio: 28.50, apu: {mo: 7.20, eq: 19.80, mat: 1.50}},
            {cat: 'movimiento', cod: '210.01', nombre: 'Corte en material suelto', unidad: 'm³', precio: 15.80, apu: {mo: 3.50, eq: 11.80, mat: 0.50}},
            {cat: 'movimiento', cod: '211.01', nombre: 'Escarificado 0.20m', unidad: 'm²', precio: 2.80, apu: {mo: 0.60, eq: 2.10, mat: 0.10}},
            
            // PAVIMENTOS
            {cat: 'pavimentos', cod: '401.01', nombre: 'Capa anticontaminante e=0.15m', unidad: 'm³', precio: 35.00, apu: {mo: 8.50, eq: 14.50, mat: 12.00}},
            {cat: 'pavimentos', cod: '402.01', nombre: 'Sub-base granular e=0.20m', unidad: 'm³', precio: 72.50, apu: {mo: 15.80, eq: 28.70, mat: 28.00}},
            {cat: 'pavimentos', cod: '403.01', nombre: 'Base granular e=0.25m', unidad: 'm³', precio: 85.50, apu: {mo: 18.50, eq: 32.00, mat: 35.00}},
            {cat: 'pavimentos', cod: '404.01', nombre: 'Base estabilizada cemento 3%', unidad: 'm³', precio: 165.00, apu: {mo: 35.00, eq: 58.00, mat: 72.00}},
            {cat: 'pavimentos', cod: '405.01', nombre: 'Base asfáltica e=0.10m', unidad: 'm³', precio: 320.00, apu: {mo: 55.00, eq: 125.00, mat: 140.00}},
            {cat: 'pavimentos', cod: '406.01', nombre: 'Imprimación asfáltica', unidad: 'm²', precio: 4.80, apu: {mo: 0.85, eq: 1.75, mat: 2.20}},
            {cat: 'pavimentos', cod: '407.01', nombre: 'Riego liga asfalto diluido', unidad: 'm²', precio: 2.20, apu: {mo: 0.45, eq: 0.80, mat: 0.95}},
            {cat: 'pavimentos', cod: '408.01', nombre: 'Tratamiento superficial monocapa', unidad: 'm²', precio: 18.50, apu: {mo: 3.50, eq: 6.80, mat: 8.20}},
            {cat: 'pavimentos', cod: '409.01', nombre: 'Tratamiento superficial bicapa', unidad: 'm²', precio: 28.00, apu: {mo: 5.80, eq: 10.20, mat: 12.00}},
            {cat: 'pavimentos', cod: '410.01', nombre: 'Sello asfáltico tipo slurry', unidad: 'm²', precio: 12.00, apu: {mo: 2.20, eq: 4.50, mat: 5.30}},
            {cat: 'pavimentos', cod: '411.01', nombre: 'Sello fisuras asfalto caliente', unidad: 'm', precio: 3.50, apu: {mo: 0.80, eq: 1.20, mat: 1.50}},
            {cat: 'pavimentos', cod: '412.01', nombre: 'Sello grietas c/geomalla', unidad: 'm', precio: 15.00, apu: {mo: 3.20, eq: 2.80, mat: 9.00}},
            {cat: 'pavimentos', cod: '413.01', nombre: 'Parchado superficial MAC', unidad: 'm²', precio: 42.00, apu: {mo: 8.50, eq: 15.50, mat: 18.00}},
            {cat: 'pavimentos', cod: '414.01', nombre: 'Parchado profundo base+MAC', unidad: 'm²', precio: 85.00, apu: {mo: 18.00, eq: 32.00, mat: 35.00}},
            {cat: 'pavimentos', cod: '415.01', nombre: 'Fresado pavimento asfaltico e=5cm', unidad: 'm²', precio: 12.50, apu: {mo: 2.50, eq: 9.20, mat: 0.80}},
            {cat: 'pavimentos', cod: '416.01', nombre: 'Pavimento concreto asfaltico caliente e=5cm', unidad: 'm³', precio: 920.00, apu: {mo: 180.00, eq: 420.00, mat: 320.00}},
            {cat: 'pavimentos', cod: '416.02', nombre: 'Pavimento concreto asfaltico caliente e=7.5cm', unidad: 'm³', precio: 920.00, apu: {mo: 180.00, eq: 420.00, mat: 320.00}},
            {cat: 'pavimentos', cod: '416.03', nombre: 'Pavimento concreto asfaltico caliente e=10cm', unidad: 'm³', precio: 920.00, apu: {mo: 180.00, eq: 420.00, mat: 320.00}},
            {cat: 'pavimentos', cod: '417.01', nombre: 'MAC modificado polimeros e=5cm', unidad: 'm³', precio: 1250.00, apu: {mo: 225.00, eq: 525.00, mat: 500.00}},
            {cat: 'pavimentos', cod: '418.01', nombre: 'MAC reciclado 20% RAP e=7cm', unidad: 'm³', precio: 780.00, apu: {mo: 155.00, eq: 365.00, mat: 260.00}},
            {cat: 'pavimentos', cod: '419.01', nombre: 'Pavimento asfaltico frio emulsión', unidad: 'm³', precio: 650.00, apu: {mo: 125.00, eq: 285.00, mat: 240.00}},
            {cat: 'pavimentos', cod: '421.01', nombre: 'Micropavimento bicapa', unidad: 'm²', precio: 22.00, apu: {mo: 4.50, eq: 8.50, mat: 9.00}},
            {cat: 'pavimentos', cod: '422.01', nombre: 'Pavimento concreto hidráulico fc=280 e=0.20m', unidad: 'm³', precio: 450.00, apu: {mo: 95.00, eq: 155.00, mat: 200.00}},
            {cat: 'pavimentos', cod: '423.01', nombre: 'Pavimento adoquines concreto', unidad: 'm²', precio: 68.00, apu: {mo: 22.00, eq: 6.00, mat: 40.00}},
            {cat: 'pavimentos', cod: '424.01', nombre: 'Pavimento adoquines piedra', unidad: 'm²', precio: 95.00, apu: {mo: 32.00, eq: 8.00, mat: 55.00}},
            {cat: 'pavimentos', cod: '425.01', nombre: 'Reciclado in-situ base granular', unidad: 'm³', precio: 45.00, apu: {mo: 9.50, eq: 28.50, mat: 7.00}},
            {cat: 'pavimentos', cod: '426.01', nombre: 'Estabilización suelos cemento', unidad: 'm³', precio: 95.00, apu: {mo: 18.00, eq: 35.00, mat: 42.00}},
            {cat: 'pavimentos', cod: '427.01', nombre: 'Capa nivelación asfalto emulsión', unidad: 'm³', precio: 520.00, apu: {mo: 85.00, eq: 180.00, mat: 255.00}},
            
            // DRENAJE
            {cat: 'drenaje', cod: '501.01', nombre: 'Excavación estructuras material común', unidad: 'm³', precio: 28.00, apu: {mo: 6.50, eq: 20.00, mat: 1.50}},
            {cat: 'drenaje', cod: '502.01', nombre: 'Excavación estructuras en roca', unidad: 'm³', precio: 55.00, apu: {mo: 11.00, eq: 40.00, mat: 4.00}},
            {cat: 'drenaje', cod: '503.01', nombre: 'Relleno estructuras material propio', unidad: 'm³', precio: 25.00, apu: {mo: 6.00, eq: 17.50, mat: 1.50}},
            {cat: 'drenaje', cod: '504.01', nombre: 'Alcantarilla TMC Ø36" L=6m', unidad: 'm', precio: 380.00, apu: {mo: 85.00, eq: 120.00, mat: 175.00}},
            {cat: 'drenaje', cod: '504.02', nombre: 'Alcantarilla TMC Ø48" L=6m', unidad: 'm', precio: 520.00, apu: {mo: 115.00, eq: 155.00, mat: 250.00}},
            {cat: 'drenaje', cod: '505.01', nombre: 'Alcantarilla marco concreto 1.00x1.00m', unidad: 'm', precio: 850.00, apu: {mo: 245.00, eq: 185.00, mat: 420.00}},
            {cat: 'drenaje', cod: '506.01', nombre: 'Cabezal alcantarilla TMC tipo I', unidad: 'und', precio: 2500, apu: {mo: 680.00, eq: 520.00, mat: 1300}},
            {cat: 'drenaje', cod: '507.01', nombre: 'Subdrén Ø4" PVC + filtro', unidad: 'm', precio: 45.00, apu: {mo: 12.00, eq: 8.50, mat: 24.50}},
            {cat: 'drenaje', cod: '508.01', nombre: 'Cunetas triangulares sin revestir', unidad: 'm', precio: 8.00, apu: {mo: 2.20, eq: 5.30, mat: 0.50}},
            {cat: 'drenaje', cod: '509.01', nombre: 'Cunetas revestidas concreto fc=175', unidad: 'm', precio: 42.00, apu: {mo: 12.50, eq: 8.50, mat: 21.00}},
            {cat: 'drenaje', cod: '510.01', nombre: 'Zanjas coronación sin revestir', unidad: 'm', precio: 12.00, apu: {mo: 3.50, eq: 7.80, mat: 0.70}},
            {cat: 'drenaje', cod: '511.01', nombre: 'Badenes concreto fc=210 e=0.30m', unidad: 'm²', precio: 185.00, apu: {mo: 52.00, eq: 38.00, mat: 95.00}},
            {cat: 'drenaje', cod: '512.01', nombre: 'Pontones concreto armado L=6m', unidad: 'm', precio: 12000, apu: {mo: 3200, eq: 2800, mat: 6000}},
            {cat: 'drenaje', cod: '513.01', nombre: 'Cunetas profundas triangulares', unidad: 'm', precio: 15.50, apu: {mo: 4.20, eq: 9.80, mat: 1.50}},
            {cat: 'drenaje', cod: '514.01', nombre: 'Canal alivio concreto 0.40x0.40m', unidad: 'm', precio: 95.00, apu: {mo: 28.50, eq: 15.50, mat: 51.00}},
            {cat: 'drenaje', cod: '515.01', nombre: 'Sumideros rejilla HF 0.60x0.60m', unidad: 'und', precio: 850.00, apu: {mo: 280.00, eq: 120.00, mat: 450.00}},
            
            // OBRAS DE ARTE
            {cat: 'obras_arte', cod: '601.01', nombre: 'Mampostería piedra', unidad: 'm³', precio: 280.00, apu: {mo: 95.00, eq: 35.00, mat: 150.00}},
            {cat: 'obras_arte', cod: '602.01', nombre: 'Muro concreto ciclopeo fc=175+30%PG', unidad: 'm³', precio: 320.00, apu: {mo: 105.00, eq: 45.00, mat: 170.00}},
            {cat: 'obras_arte', cod: '603.01', nombre: 'Muro concreto armado fc=210', unidad: 'm³', precio: 650.00, apu: {mo: 220.00, eq: 130.00, mat: 300.00}},
            {cat: 'obras_arte', cod: '604.01', nombre: 'Gaviones caja 2x1x1m', unidad: 'm³', precio: 180.00, apu: {mo: 52.00, eq: 28.00, mat: 100.00}},
            {cat: 'obras_arte', cod: '604.02', nombre: 'Gaviones colchón 0.30m', unidad: 'm²', precio: 95.00, apu: {mo: 28.00, eq: 15.00, mat: 52.00}},
            {cat: 'obras_arte', cod: '605.01', nombre: 'Defensas ribereñas enrocado', unidad: 'm³', precio: 85.00, apu: {mo: 22.00, eq: 48.00, mat: 15.00}},
            {cat: 'obras_arte', cod: '606.01', nombre: 'Demolición concreto simple', unidad: 'm³', precio: 45.00, apu: {mo: 12.00, eq: 31.00, mat: 2.00}},
            {cat: 'obras_arte', cod: '606.02', nombre: 'Demolición concreto armado', unidad: 'm³', precio: 85.00, apu: {mo: 22.00, eq: 60.00, mat: 3.00}},
            {cat: 'obras_arte', cod: '607.01', nombre: 'Geomalla biaxial 40kN/m', unidad: 'm²', precio: 12.50, apu: {mo: 2.50, eq: 0.80, mat: 9.20}},
            {cat: 'obras_arte', cod: '608.01', nombre: 'Geotextil NT-2000', unidad: 'm²', precio: 4.80, apu: {mo: 0.80, eq: 0.20, mat: 3.80}},
            {cat: 'obras_arte', cod: '609.01', nombre: 'Geomembrana HDPE 1.5mm', unidad: 'm²', precio: 18.50, apu: {mo: 3.50, eq: 1.00, mat: 14.00}},
            {cat: 'obras_arte', cod: '610.01', nombre: 'Protección taludes semilla+fertilizante', unidad: 'm²', precio: 8.50, apu: {mo: 2.80, eq: 1.50, mat: 4.20}},
            {cat: 'obras_arte', cod: '611.01', nombre: 'Concreto lanzado shotcrete e=5cm', unidad: 'm²', precio: 85.00, apu: {mo: 22.00, eq: 28.00, mat: 35.00}},
            {cat: 'obras_arte', cod: '612.01', nombre: 'Anclajes terreno 3m Ø1"', unidad: 'und', precio: 280.00, apu: {mo: 85.00, eq: 95.00, mat: 100.00}},
            
            // SEÑALIZACION
            {cat: 'señalizacion', cod: '801.01', nombre: 'Señal vertical reglamentaria 0.60x0.60m', unidad: 'und', precio: 280.00, apu: {mo: 52.00, eq: 28.00, mat: 200.00}},
            {cat: 'señalizacion', cod: '801.02', nombre: 'Señal vertical preventiva 0.75x0.75m', unidad: 'und', precio: 320.00, apu: {mo: 58.00, eq: 32.00, mat: 230.00}},
            {cat: 'señalizacion', cod: '801.03', nombre: 'Señal informativa 2.40x1.20m', unidad: 'und', precio: 1200, apu: {mo: 225.00, eq: 125.00, mat: 850.00}},
            {cat: 'señalizacion', cod: '802.01', nombre: 'Poste soporte señal Ø2" h=3m', unidad: 'und', precio: 180.00, apu: {mo: 42.00, eq: 28.00, mat: 110.00}},
            {cat: 'señalizacion', cod: '803.01', nombre: 'Marcas pavimento pintura tráfico continua 0.10m', unidad: 'm', precio: 1.80, apu: {mo: 0.35, eq: 0.65, mat: 0.80}},
            {cat: 'señalizacion', cod: '803.02', nombre: 'Marcas pavimento pintura tráfico discontinua', unidad: 'm', precio: 1.50, apu: {mo: 0.30, eq: 0.55, mat: 0.65}},
            {cat: 'señalizacion', cod: '804.01', nombre: 'Símbolos y leyendas pavimento', unidad: 'm²', precio: 28.50, apu: {mo: 5.80, eq: 8.70, mat: 14.00}},
            {cat: 'señalizacion', cod: '805.01', nombre: 'Tachas reflectivas bidireccional', unidad: 'und', precio: 18.00, apu: {mo: 2.50, eq: 1.50, mat: 14.00}},
            {cat: 'señalizacion', cod: '806.01', nombre: 'Delineadores Ø4" h=1.20m', unidad: 'und', precio: 95.00, apu: {mo: 18.00, eq: 12.00, mat: 65.00}},
            {cat: 'señalizacion', cod: '807.01', nombre: 'Guardavías metálico doble onda', unidad: 'm', precio: 180.00, apu: {mo: 38.00, eq: 32.00, mat: 110.00}},
            {cat: 'señalizacion', cod: '808.01', nombre: 'Hitos kilométricos concreto', unidad: 'und', precio: 220.00, apu: {mo: 65.00, eq: 35.00, mat: 120.00}},
            {cat: 'señalizacion', cod: '809.01', nombre: 'Postes SOS h=3m c/panel solar', unidad: 'und', precio: 4500, apu: {mo: 850.00, eq: 450.00, mat: 3200}},
            {cat: 'señalizacion', cod: '810.01', nombre: 'Captafaros bidireccional alto tráfico', unidad: 'und', precio: 28.00, apu: {mo: 3.50, eq: 1.50, mat: 23.00}},
            {cat: 'señalizacion', cod: '811.01', nombre: 'Barreras new jersey concreto', unidad: 'm', precio: 185.00, apu: {mo: 52.00, eq: 38.00, mat: 95.00}},
            {cat: 'señalizacion', cod: '812.01', nombre: 'Marcas pavimento termoplástico', unidad: 'm²', precio: 45.00, apu: {mo: 8.50, eq: 12.50, mat: 24.00}},
        ];

        let presupuesto = [];

        document.getElementById('categoria').addEventListener('change', function() {
            const cat = this.value;
            const select = document.getElementById('partida');
            select.innerHTML = '<option value="">Selecciona partida...</option>';
            
            const filtered = cat ? partidasDB.filter(p => p.cat === cat) : partidasDB;
            filtered.forEach(p => {
                select.innerHTML += `<option value="${p.cod}">${p.cod} - ${p.nombre} (${p.unidad}) - S/ ${p.precio.toFixed(2)}</option>`;
            });
        });

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
                    `<div onclick="seleccionarPartida('${p.cod}')">${p.cod} - ${p.nombre}</div>`
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
                <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--color-border);">
                    <strong style="color: var(--color-accent); font-size: 1rem;">${partida.cod}</strong>
                    <div style="color: var(--color-text); margin-top: 0.3rem;">${partida.nombre}</div>
                    <div style="color: #94a3b8; margin-top: 0.3rem;">Unidad: ${partida.unidad}</div>
                </div>
                
                <div style="background: var(--color-bg); padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--color-accent);">S/ ${total.toFixed(2)}</div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">Precio Unitario Total</div>
                </div>
                
                <div style="margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>👷 Mano Obra</span>
                        <strong style="color: var(--color-accent);">S/ ${partida.apu.mo.toFixed(2)}</strong>
                    </div>
                    <div style="background: var(--color-bg); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #22c55e; height: 100%; width: ${moPorc}%;"></div>
                    </div>
                    <div style="text-align: right; color: #94a3b8; font-size: 0.8rem; margin-top: 0.2rem;">${moPorc}%</div>
                </div>
                
                <div style="margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>🚜 Equipos</span>
                        <strong style="color: var(--color-accent);">S/ ${partida.apu.eq.toFixed(2)}</strong>
                    </div>
                    <div style="background: var(--color-bg); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #f59e0b; height: 100%; width: ${eqPorc}%;"></div>
                    </div>
                    <div style="text-align: right; color: #94a3b8; font-size: 0.8rem; margin-top: 0.2rem;">${eqPorc}%</div>
                </div>
                
                <div style="margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>📦 Materiales</span>
                        <strong style="color: var(--color-accent);">S/ ${partida.apu.mat.toFixed(2)}</strong>
                    </div>
                    <div style="background: var(--color-bg); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #3b82f6; height: 100%; width: ${matPorc}%;"></div>
                    </div>
                    <div style="text-align: right; color: #94a3b8; font-size: 0.8rem; margin-top: 0.2rem;">${matPorc}%</div>
                </div>
            `;
            
            panel.style.display = 'block';
        }

        function agregarPartida() {
            const cod = document.getElementById('partida').value;
            const metrado = parseFloat(document.getElementById('metrado').value);
            
            if(!cod || !metrado) {
                alert('Selecciona partida e ingresa metrado');
                return;
            }
            
            const partida = partidasDB.find(p => p.cod === cod);
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
            
            let directo = 0;
            presupuesto.forEach((p, idx) => {
                directo += p.parcial;
                tbody.innerHTML += `
                    <tr>
                        <td>${p.cod} - ${p.nombre}</td>
                        <td>${p.unidad}</td>
                        <td>${p.metrado.toFixed(2)}</td>
                        <td>S/ ${p.precio.toFixed(2)}</td>
                        <td>S/ ${p.parcial.toFixed(2)}</td>
                        <td><button onclick="eliminar(${idx})" style="background: #dc2626; padding: 0.5rem;">❌</button></td>
                    </tr>
                `;
            });
            
            const gg = directo * 0.10;
            const util = directo * 0.08;
            const total = directo + gg + util;
            
            document.getElementById('tdDirecto').textContent = `S/ ${directo.toFixed(2)}`;
            document.getElementById('tdGG').textContent = `S/ ${gg.toFixed(2)}`;
            document.getElementById('tdUtil').textContent = `S/ ${util.toFixed(2)}`;
            document.getElementById('tdTotal').textContent = `S/ ${total.toFixed(2)}`;
            
            document.getElementById('costoDirecto').textContent = `S/ ${directo.toLocaleString('es-PE', {maximumFractionDigits: 0})}`;
            document.getElementById('total').textContent = `S/ ${total.toLocaleString('es-PE', {maximumFractionDigits: 0})}`;
            document.getElementById('numPartidas').textContent = presupuesto.length;
        }

        function eliminar(idx) {
            presupuesto.splice(idx, 1);
            renderizarTabla();
        }

        function limpiar() {
            if(confirm('¿Borrar todo el presupuesto?')) {
                presupuesto = [];
                renderizarTabla();
            }
        }

        function exportarCSV() {
            let csv = 'Código,Partida,Unidad,Metrado,P.U.,Parcial\\n';
            presupuesto.forEach(p => {
                csv += `${p.cod},"${p.nombre}",${p.unidad},${p.metrado},${p.precio},${p.parcial}\\n`;
            });
            
            const directo = presupuesto.reduce((sum, p) => sum + p.parcial, 0);
            const gg = directo * 0.10;
            const util = directo * 0.08;
            const total = directo + gg + util;
            
            csv += `\\n,COSTO DIRECTO,,,,${directo.toFixed(2)}\\n`;
            csv += `,Gastos Generales 10%,,,,${gg.toFixed(2)}\\n`;
            csv += `,Utilidad 8%,,,,${util.toFixed(2)}\\n`;
            csv += `,TOTAL PRESUPUESTO,,,,${total.toFixed(2)}\\n`;
            
            const blob = new Blob([csv], {type: 'text/csv'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'presupuesto_vial_seace.csv';
            a.click();
        }

        function exportarPDF() {
            alert('📄 Para PDF profesional: Usa reportlab en Python Streamlit. Esta versión HTML exporta CSV. Si necesitas PDF con gráficos, implementa jsPDF o backend Python.');
        }

        document.getElementById('categoria').dispatchEvent(new Event('change'));
    </script>
</body>
</html>
"""

components.html(html_content, height=1400, scrolling=True)
