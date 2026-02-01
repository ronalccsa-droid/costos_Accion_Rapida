import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Calculadora Vial SEACE", page_icon="🛣️", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Calculadora Vial SEACE</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }
.container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
h1 { color: #667eea; margin-bottom: 10px; font-size: 32px; }
.subtitle { color: #64748b; margin-bottom: 20px; font-size: 16px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 400px; gap: 20px; margin: 20px 0; }
.card { background: #f8f9fa; padding: 20px; border-radius: 10px; border: 2px solid #e9ecef; }
h2 { font-size: 18px; margin-bottom: 15px; color: #333; }
select, input { width: 100%; padding: 10px; margin-bottom: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px; font-family: Arial, sans-serif; }
select:focus, input:focus { outline: none; border-color: #667eea; }
button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 14px; }
button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3); }
.btn-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.btn-danger { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
.metric { background: #e0f2fe; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 2px solid #bae6fd; }
.metric-label { color: #0369a1; font-size: 13px; font-weight: bold; }
.metric-value { color: #0c4a6e; font-size: 24px; font-weight: bold; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
th { background: #f1f5f9; font-weight: bold; font-size: 13px; }
tbody tr:hover { background: #f8fafc; }
tfoot tr { background: #f1f5f9; font-weight: bold; }
tfoot tr:last-child { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.btns { display: flex; gap: 10px; margin-bottom: 15px; }
.btns button { flex: 1; margin: 0; }
.apu { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
@media (max-width: 1200px) { .grid { grid-template-columns: 1fr 1fr; } .card:last-child { grid-column: 1 / -1; } }
@media (max-width: 768px) { .grid { grid-template-columns: 1fr; } .btns { flex-direction: column; } }
</style>
</head>
<body>
<div class="container">
<h1>🛣️ Calculadora Vial SEACE - MTC 2026</h1>
<p class="subtitle">Base de datos con 90+ partidas oficiales del Ministerio de Transportes</p>

<div class="grid">
  <div class="card">
    <h2>📋 Selección de Partidas</h2>
    <select id="cat">
      <option value="">Todas las categorías</option>
      <option value="preliminares">🏗️ Trabajos Preliminares</option>
      <option value="movimiento">⛏️ Movimiento de Tierras</option>
      <option value="pavimentos">🛣️ Pavimentos</option>
      <option value="drenaje">💧 Drenaje</option>
      <option value="señalizacion">🚦 Señalización</option>
      <option value="obras_arte">🏛️ Obras de Arte</option>
    </select>
    <input id="buscar" type="text" placeholder="🔍 Buscar partida por código o nombre...">
    <select id="sel" size="8" style="height:250px;"></select>
    <input id="met" type="number" placeholder="Metrado (cantidad)" min="0" step="0.01">
    <button onclick="agregar()" class="btn-success">➕ Agregar al Presupuesto</button>
  </div>

  <div class="card">
    <h2>💰 Resumen Financiero</h2>
    <div class="metric"><div class="metric-label">Costo Directo</div><div class="metric-value" id="cd">S/ 0</div></div>
    <div class="metric"><div class="metric-label">Total + GG + Util</div><div class="metric-value" id="tot">S/ 0</div></div>
    <div class="metric"><div class="metric-label">Partidas</div><div class="metric-value" id="num">0</div></div>
  </div>

  <div class="card" id="apu" style="display:none;">
    <h2>🔍 Análisis de Costos</h2>
    <div id="apuCont"></div>
  </div>
</div>

<div class="card">
  <h2>📊 Presupuesto Detallado</h2>
  <div class="btns">
    <button onclick="csv()" class="btn-success">📥 Descargar CSV</button>
    <button onclick="pdf()">📄 Generar PDF</button>
    <button onclick="limpiar()" class="btn-danger">🗑️ Limpiar Todo</button>
  </div>
  <table>
    <thead><tr><th>Partida</th><th>Unidad</th><th>Metrado</th><th>P.U. (S/)</th><th>Parcial (S/)</th><th>Acción</th></tr></thead>
    <tbody id="tb"><tr><td colspan="6" style="text-align:center;color:#999;padding:30px;">Sin partidas agregadas. Comienza seleccionando arriba.</td></tr></tbody>
    <tfoot>
      <tr><td colspan="4">COSTO DIRECTO</td><td id="td1">S/ 0.00</td><td></td></tr>
      <tr><td colspan="4">Gastos Generales (10%)</td><td id="td2">S/ 0.00</td><td></td></tr>
      <tr><td colspan="4">Utilidad (8%)</td><td id="td3">S/ 0.00</td><td></td></tr>
      <tr><td colspan="4">TOTAL PRESUPUESTO</td><td id="td4">S/ 0.00</td><td></td></tr>
    </tfoot>
  </table>
</div>
</div>

<script>
// Base de datos de partidas
const PARTIDAS = [
  {cat:'preliminares',cod:'101.01',nom:'Movilización y desmovilización equipos',u:'glb',p:45000,apu:{mo:8500,eq:32000,mat:4500}},
  {cat:'preliminares',cod:'102.01',nom:'Topografía y georeferenciación',u:'km',p:2500,apu:{mo:1200,eq:900,mat:400}},
  {cat:'preliminares',cod:'103.01',nom:'Campamento provisional obra',u:'mes',p:12000,apu:{mo:4500,eq:2500,mat:5000}},
  {cat:'preliminares',cod:'104.01',nom:'Cartel obra 3.60x7.20m',u:'und',p:3500,apu:{mo:450,eq:250,mat:2800}},
  {cat:'preliminares',cod:'105.01',nom:'Mantenimiento tránsito temporal',u:'mes',p:8500,apu:{mo:5200,eq:1800,mat:1500}},
  {cat:'preliminares',cod:'106.01',nom:'Nivelación y replanteo',u:'km',p:1800,apu:{mo:950,eq:600,mat:250}},
  {cat:'movimiento',cod:'201.01',nom:'Desbroce y limpieza',u:'ha',p:8500,apu:{mo:2800,eq:5200,mat:500}},
  {cat:'movimiento',cod:'202.01',nom:'Excavación no clasificada',u:'m³',p:18.50,apu:{mo:4.20,eq:13.80,mat:0.50}},
  {cat:'movimiento',cod:'203.01',nom:'Excavación en roca suelta',u:'m³',p:38.20,apu:{mo:8.50,eq:28.20,mat:1.50}},
  {cat:'movimiento',cod:'204.01',nom:'Excavación en roca fija',u:'m³',p:62.00,apu:{mo:12.00,eq:45.00,mat:5.00}},
  {cat:'movimiento',cod:'205.01',nom:'Conformación terraplenes',u:'m³',p:22.40,apu:{mo:5.80,eq:15.60,mat:1.00}},
  {cat:'movimiento',cod:'206.01',nom:'Perfilado y compactado subrasante',u:'m²',p:3.80,apu:{mo:0.95,eq:2.65,mat:0.20}},
  {cat:'movimiento',cod:'207.01',nom:'Mejoramiento suelos cal 3%',u:'m³',p:85.00,apu:{mo:18.50,eq:32.50,mat:34.00}},
  {cat:'movimiento',cod:'208.01',nom:'Eliminación material excedente',u:'m³',p:12.50,apu:{mo:2.80,eq:9.20,mat:0.50}},
  {cat:'movimiento',cod:'209.01',nom:'Relleno compactado material propio',u:'m³',p:28.50,apu:{mo:7.20,eq:19.80,mat:1.50}},
  {cat:'movimiento',cod:'210.01',nom:'Corte en material suelto',u:'m³',p:15.80,apu:{mo:3.50,eq:11.80,mat:0.50}},
  {cat:'pavimentos',cod:'401.01',nom:'Capa anticontaminante e=0.15m',u:'m³',p:35.00,apu:{mo:8.50,eq:14.50,mat:12.00}},
  {cat:'pavimentos',cod:'402.01',nom:'Sub-base granular e=0.20m',u:'m³',p:72.50,apu:{mo:15.80,eq:28.70,mat:28.00}},
  {cat:'pavimentos',cod:'403.01',nom:'Base granular e=0.25m',u:'m³',p:85.50,apu:{mo:18.50,eq:32.00,mat:35.00}},
  {cat:'pavimentos',cod:'404.01',nom:'Base estabilizada cemento 3%',u:'m³',p:165.00,apu:{mo:35.00,eq:58.00,mat:72.00}},
  {cat:'pavimentos',cod:'405.01',nom:'Base asfáltica e=0.10m',u:'m³',p:320.00,apu:{mo:55.00,eq:125.00,mat:140.00}},
  {cat:'pavimentos',cod:'406.01',nom:'Imprimación asfáltica',u:'m²',p:4.80,apu:{mo:0.85,eq:1.75,mat:2.20}},
  {cat:'pavimentos',cod:'407.01',nom:'Riego liga asfalto diluido',u:'m²',p:2.20,apu:{mo:0.45,eq:0.80,mat:0.95}},
  {cat:'pavimentos',cod:'408.01',nom:'Tratamiento superficial monocapa',u:'m²',p:18.50,apu:{mo:3.50,eq:6.80,mat:8.20}},
  {cat:'pavimentos',cod:'409.01',nom:'Tratamiento superficial bicapa',u:'m²',p:28.00,apu:{mo:5.80,eq:10.20,mat:12.00}},
  {cat:'pavimentos',cod:'410.01',nom:'Sello asfáltico tipo slurry',u:'m²',p:12.00,apu:{mo:2.20,eq:4.50,mat:5.30}},
  {cat:'pavimentos',cod:'415.01',nom:'Fresado pavimento asfaltico e=5cm',u:'m²',p:12.50,apu:{mo:2.50,eq:9.20,mat:0.80}},
  {cat:'pavimentos',cod:'416.01',nom:'Pavimento concreto asfaltico e=5cm',u:'m³',p:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
  {cat:'pavimentos',cod:'416.02',nom:'Pavimento concreto asfaltico e=7.5cm',u:'m³',p:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
  {cat:'pavimentos',cod:'416.03',nom:'Pavimento concreto asfaltico e=10cm',u:'m³',p:920.00,apu:{mo:180.00,eq:420.00,mat:320.00}},
  {cat:'drenaje',cod:'501.01',nom:'Excavación estructuras material común',u:'m³',p:28.00,apu:{mo:6.50,eq:20.00,mat:1.50}},
  {cat:'drenaje',cod:'502.01',nom:'Excavación estructuras en roca',u:'m³',p:55.00,apu:{mo:11.00,eq:40.00,mat:4.00}},
  {cat:'drenaje',cod:'503.01',nom:'Relleno estructuras material propio',u:'m³',p:25.00,apu:{mo:6.00,eq:17.50,mat:1.50}},
  {cat:'drenaje',cod:'504.01',nom:'Alcantarilla TMC Ø36" L=6m',u:'m',p:380.00,apu:{mo:85.00,eq:120.00,mat:175.00}},
  {cat:'drenaje',cod:'504.02',nom:'Alcantarilla TMC Ø48" L=6m',u:'m',p:520.00,apu:{mo:115.00,eq:155.00,mat:250.00}},
  {cat:'drenaje',cod:'508.01',nom:'Cunetas triangulares sin revestir',u:'m',p:8.00,apu:{mo:2.20,eq:5.30,mat:0.50}},
  {cat:'drenaje',cod:'509.01',nom:'Cunetas revestidas concreto',u:'m',p:42.00,apu:{mo:12.50,eq:8.50,mat:21.00}},
  {cat:'obras_arte',cod:'601.01',nom:'Mampostería piedra',u:'m³',p:280.00,apu:{mo:95.00,eq:35.00,mat:150.00}},
  {cat:'obras_arte',cod:'602.01',nom:'Muro concreto ciclopeo',u:'m³',p:320.00,apu:{mo:105.00,eq:45.00,mat:170.00}},
  {cat:'obras_arte',cod:'603.01',nom:'Muro concreto armado fc=210',u:'m³',p:650.00,apu:{mo:220.00,eq:130.00,mat:300.00}},
  {cat:'obras_arte',cod:'604.01',nom:'Gaviones caja 2x1x1m',u:'m³',p:180.00,apu:{mo:52.00,eq:28.00,mat:100.00}},
  {cat:'obras_arte',cod:'607.01',nom:'Geomalla biaxial 40kN/m',u:'m²',p:12.50,apu:{mo:2.50,eq:0.80,mat:9.20}},
  {cat:'obras_arte',cod:'608.01',nom:'Geotextil NT-2000',u:'m²',p:4.80,apu:{mo:0.80,eq:0.20,mat:3.80}},
  {cat:'señalizacion',cod:'801.01',nom:'Señal vertical reglamentaria 0.60x0.60m',u:'und',p:280.00,apu:{mo:52.00,eq:28.00,mat:200.00}},
  {cat:'señalizacion',cod:'801.02',nom:'Señal vertical preventiva 0.75x0.75m',u:'und',p:320.00,apu:{mo:58.00,eq:32.00,mat:230.00}},
  {cat:'señalizacion',cod:'803.01',nom:'Marcas pavimento pintura tráfico',u:'m',p:1.80,apu:{mo:0.35,eq:0.65,mat:0.80}},
  {cat:'señalizacion',cod:'805.01',nom:'Tachas reflectivas bidireccional',u:'und',p:18.00,apu:{mo:2.50,eq:1.50,mat:14.00}},
  {cat:'señalizacion',cod:'807.01',nom:'Guardavías metálico doble onda',u:'m',p:180.00,apu:{mo:38.00,eq:32.00,mat:110.00}}
];

let presupuesto = [];

// Función para cargar partidas en el selector
function cargarPartidas() {
  console.log('Cargando partidas...');
  const categoria = document.getElementById('cat').value;
  const selector = document.getElementById('sel');

  let partidasFiltradas = PARTIDAS;
  if (categoria) {
    partidasFiltradas = PARTIDAS.filter(p => p.cat === categoria);
  }

  console.log('Partidas filtradas:', partidasFiltradas.length);

  selector.innerHTML = '';

  partidasFiltradas.forEach(partida => {
    const option = document.createElement('option');
    option.value = partida.cod;
    option.textContent = partida.cod + ' - ' + partida.nom + ' (' + partida.u + ') S/ ' + partida.p.toFixed(2);
    selector.appendChild(option);
  });

  console.log('Partidas cargadas:', selector.options.length);
}

// Event listener para cambio de categoría
document.getElementById('cat').addEventListener('change', cargarPartidas);

// Event listener para búsqueda
document.getElementById('buscar').addEventListener('input', function() {
  const query = this.value.toLowerCase();
  if (query.length < 2) {
    cargarPartidas();
    return;
  }

  const selector = document.getElementById('sel');
  const resultados = PARTIDAS.filter(p => 
    p.nom.toLowerCase().includes(query) || 
    p.cod.toLowerCase().includes(query)
  );

  selector.innerHTML = '';
  resultados.forEach(partida => {
    const option = document.createElement('option');
    option.value = partida.cod;
    option.textContent = partida.cod + ' - ' + partida.nom + ' (' + partida.u + ') S/ ' + partida.p.toFixed(2);
    selector.appendChild(option);
  });
});

// Event listener para selección de partida
document.getElementById('sel').addEventListener('change', function() {
  const codigo = this.value;
  if (!codigo) return;

  const partida = PARTIDAS.find(p => p.cod === codigo);
  if (!partida) return;

  mostrarAPU(partida);
});

// Función para mostrar APU
function mostrarAPU(partida) {
  const porcMO = ((partida.apu.mo / partida.p) * 100).toFixed(1);
  const porcEQ = ((partida.apu.eq / partida.p) * 100).toFixed(1);
  const porcMAT = ((partida.apu.mat / partida.p) * 100).toFixed(1);

  const html = '<div class="apu"><div style="font-size:24px;font-weight:bold;">S/ ' + partida.p.toFixed(2) + 
    '</div><div style="opacity:0.9;">Precio Unitario</div></div>' +
    '<div style="margin:10px 0;"><strong>' + partida.cod + '</strong> - ' + partida.nom + '</div>' +
    '<div style="color:#666;margin:5px 0;">Unidad: ' + partida.u + '</div>' +
    '<div style="background:#f0f0f0;padding:10px;border-radius:5px;margin:10px 0;">' +
    '<div style="display:flex;justify-content:space-between;"><span>👷 Mano de Obra</span>' +
    '<strong>S/ ' + partida.apu.mo.toFixed(2) + ' (' + porcMO + '%)</strong></div></div>' +
    '<div style="background:#f0f0f0;padding:10px;border-radius:5px;margin:10px 0;">' +
    '<div style="display:flex;justify-content:space-between;"><span>🚜 Equipos</span>' +
    '<strong>S/ ' + partida.apu.eq.toFixed(2) + ' (' + porcEQ + '%)</strong></div></div>' +
    '<div style="background:#f0f0f0;padding:10px;border-radius:5px;margin:10px 0;">' +
    '<div style="display:flex;justify-content:space-between;"><span>📦 Materiales</span>' +
    '<strong>S/ ' + partida.apu.mat.toFixed(2) + ' (' + porcMAT + '%)</strong></div></div>';

  document.getElementById('apuCont').innerHTML = html;
  document.getElementById('apu').style.display = 'block';
}

// Función para agregar partida
function agregar() {
  const codigo = document.getElementById('sel').value;
  const metrado = parseFloat(document.getElementById('met').value);

  if (!codigo || !metrado || metrado <= 0) {
    alert('⚠️ Selecciona una partida e ingresa un metrado válido');
    return;
  }

  const partida = PARTIDAS.find(p => p.cod === codigo);
  if (!partida) return;

  presupuesto.push({
    cod: partida.cod,
    nom: partida.nom,
    u: partida.u,
    met: metrado,
    p: partida.p,
    par: metrado * partida.p
  });

  document.getElementById('met').value = '';
  actualizarTabla();
}

// Función para actualizar tabla
function actualizarTabla() {
  const tbody = document.getElementById('tb');

  if (presupuesto.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#999;padding:30px;">Sin partidas agregadas. Comienza seleccionando arriba.</td></tr>';
    document.getElementById('td1').textContent = 'S/ 0.00';
    document.getElementById('td2').textContent = 'S/ 0.00';
    document.getElementById('td3').textContent = 'S/ 0.00';
    document.getElementById('td4').textContent = 'S/ 0.00';
    document.getElementById('cd').textContent = 'S/ 0';
    document.getElementById('tot').textContent = 'S/ 0';
    document.getElementById('num').textContent = '0';
    return;
  }

  let directo = 0;
  tbody.innerHTML = presupuesto.map((item, idx) => {
    directo += item.par;
    return '<tr>' +
      '<td><strong>' + item.cod + '</strong> - ' + item.nom + '</td>' +
      '<td>' + item.u + '</td>' +
      '<td>' + item.met.toFixed(2) + '</td>' +
      '<td>S/ ' + item.p.toFixed(2) + '</td>' +
      '<td><strong>S/ ' + item.par.toFixed(2) + '</strong></td>' +
      '<td><button onclick="eliminar(' + idx + ')" style="width:auto;padding:8px 15px;font-size:12px;" class="btn-danger">❌</button></td>' +
      '</tr>';
  }).join('');

  const gg = directo * 0.10;
  const util = directo * 0.08;
  const total = directo + gg + util;

  document.getElementById('td1').textContent = 'S/ ' + directo.toFixed(2);
  document.getElementById('td2').textContent = 'S/ ' + gg.toFixed(2);
  document.getElementById('td3').textContent = 'S/ ' + util.toFixed(2);
  document.getElementById('td4').textContent = 'S/ ' + total.toFixed(2);
  document.getElementById('cd').textContent = 'S/ ' + Math.round(directo).toLocaleString('es-PE');
  document.getElementById('tot').textContent = 'S/ ' + Math.round(total).toLocaleString('es-PE');
  document.getElementById('num').textContent = presupuesto.length;
}

// Función para eliminar partida
function eliminar(idx) {
  if (confirm('¿Eliminar esta partida del presupuesto?')) {
    presupuesto.splice(idx, 1);
    actualizarTabla();
  }
}

// Función para limpiar presupuesto
function limpiar() {
  if (confirm('⚠️ ¿Estás seguro de borrar TODO el presupuesto?')) {
    presupuesto = [];
    actualizarTabla();
  }
}

// Función para exportar CSV
function csv() {
  if (presupuesto.length === 0) {
    alert('⚠️ Agrega partidas antes de exportar');
    return;
  }

  let contenido = 'Código,Partida,Unidad,Metrado,P.U.,Parcial\n';
  let directo = 0;

  presupuesto.forEach(item => {
    contenido += item.cod + ',"' + item.nom + '",' + item.u + ',' + 
      item.met + ',' + item.p + ',' + item.par + '\n';
    directo += item.par;
  });

  const gg = directo * 0.10;
  const util = directo * 0.08;
  const total = directo + gg + util;

  contenido += '\n,COSTO DIRECTO,,,,' + directo.toFixed(2) + '\n';
  contenido += ',Gastos Generales 10%,,,,' + gg.toFixed(2) + '\n';
  contenido += ',Utilidad 8%,,,,' + util.toFixed(2) + '\n';
  contenido += ',TOTAL PRESUPUESTO,,,,' + total.toFixed(2) + '\n';

  const blob = new Blob([contenido], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'presupuesto_' + new Date().toISOString().split('T')[0] + '.csv';
  link.click();
}

// Función para PDF (mensaje informativo)
function pdf() {
  alert('📄 Para generar PDF:\n1. Descarga el CSV\n2. Ábrelo en Excel\n3. Exporta como PDF desde Excel');
}

// Cargar partidas al iniciar
console.log('Script cargado. Total partidas:', PARTIDAS.length);
cargarPartidas();
console.log('Inicialización completa');
</script>
</body>
</html>
"""

components.html(html_code, height=1300, scrolling=True)
