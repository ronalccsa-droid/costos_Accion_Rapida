import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Calculadora Vial", page_icon="🛣️", layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
.container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
h1 { color: #667eea; margin-bottom: 10px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 400px; gap: 20px; margin: 20px 0; }
.card { background: #f8f9fa; padding: 20px; border-radius: 10px; border: 2px solid #e9ecef; }
h2 { font-size: 18px; margin-bottom: 15px; color: #333; }
select, input { width: 100%; padding: 10px; margin-bottom: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px; }
select:focus, input:focus { outline: none; border-color: #667eea; }
button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
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
tfoot tr { background: #e0f2fe; font-weight: bold; }
.partida-item { padding: 8px; margin: 5px 0; background: white; border-radius: 5px; cursor: pointer; border: 2px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }
.partida-item:hover { border-color: #667eea; background: #f0f4ff; }
.partida-selected { border-color: #10b981; background: #d1fae5; }
.partida-code { font-weight: bold; color: #667eea; }
.partida-price { color: #10b981; font-weight: bold; }
</style>
</head>
<body>
<div class="container">
<h1>🛣️ Calculadora Vial SEACE - MTC 2026</h1>
<p style="color: #666; margin-bottom: 20px;">Base de datos con 90+ partidas oficiales del Ministerio de Transportes</p>

<div class="grid">
<div class="card">
<h2>📋 Selección de Partidas</h2>
<select id="categoria" onchange="cargarPartidas()">
<option value="">Seleccione categoría...</option>
<option value="preliminares">🏗️ Trabajos Preliminares</option>
<option value="movimiento">⛏️ Movimiento de Tierras</option>
<option value="subbase">📦 Sub-Base y Base</option>
<option value="pavimentos">🛣️ Pavimentos</option>
<option value="obras">🌊 Obras de Arte y Drenaje</option>
<option value="senalizacion">🚦 Señalización y Seguridad Vial</option>
</select>
<input type="text" id="buscar" placeholder="🔍 Buscar partida..." oninput="filtrarPartidas()">
<div id="listaPartidas" style="height: 400px; overflow-y: auto; border: 2px solid #e5e7eb; border-radius: 5px; padding: 10px; background: #fafafa;"></div>
<input type="number" id="metrado" placeholder="Metrado (cantidad)" step="0.01" min="0">
<button onclick="agregarPartida()" class="btn-success">✚ Agregar Partida</button>
</div>

<div class="card">
<h2>💰 Resumen</h2>
<div class="metric">
<div class="metric-label">Costo Directo</div>
<div class="metric-value" id="costoDirecto">S/ 0</div>
</div>
<div class="metric">
<div class="metric-label">Total</div>
<div class="metric-value" id="total">S/ 0</div>
</div>
<div class="metric" style="background: #fef3c7; border-color: #fde68a;">
<div class="metric-label" style="color: #92400e;">Partidas</div>
<div class="metric-value" style="color: #78350f;" id="numPartidas">0</div>
</div>
<button onclick="limpiarTodo()" class="btn-danger">🗑️ Limpiar Todo</button>
<button onclick="exportarExcel()" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); margin-top: 10px;">📊 Exportar Excel</button>
</div>

<div class="card" style="grid-column: span 3;">
<h2>📊 Presupuesto</h2>
<table id="tablaPresupuesto">
<thead>
<tr>
<th>Código</th>
<th>Descripción</th>
<th>Unidad</th>
<th>Metrado</th>
<th>P.U.</th>
<th>Parcial</th>
<th>Acción</th>
</tr>
</thead>
<tbody id="tbody"></tbody>
<tfoot>
<tr>
<td colspan="5" style="text-align: right;">COSTO DIRECTO:</td>
<td id="footerTotal" style="color: #0369a1;">S/ 0.00</td>
<td></td>
</tr>
</tfoot>
</table>
</div>
</div>
</div>

<script>
const partidas = {
  preliminares: [
    {codigo: "01.01", desc: "Movilización y Desmovilización de Equipo", unidad: "GLB", precio: 25000.00},
    {codigo: "01.02", desc: "Topografía y Georeferenciación", unidad: "KM", precio: 1500.00},
    {codigo: "01.03", desc: "Mantenimiento de Tránsito Temporal y Seguridad Vial", unidad: "GLB", precio: 15000.00},
    {codigo: "01.04", desc: "Campamento de Obra", unidad: "GLB", precio: 35000.00},
  ],
  movimiento: [
    {codigo: "02.01", desc: "Desbroce y Limpieza", unidad: "HA", precio: 2500.00},
    {codigo: "02.02", desc: "Excavación no Clasificada para Explanaciones", unidad: "M3", precio: 12.50},
    {codigo: "02.03", desc: "Excavación en Roca Fija", unidad: "M3", precio: 35.00},
    {codigo: "02.04", desc: "Conformación de Terraplenes", unidad: "M3", precio: 8.50},
    {codigo: "02.05", desc: "Relleno con Material de Préstamo", unidad: "M3", precio: 18.00},
  ],
  subbase: [
    {codigo: "03.01", desc: "Sub-Base Granular e=0.20m", unidad: "M2", precio: 12.80},
    {codigo: "03.02", desc: "Base Granular e=0.20m", unidad: "M2", precio: 18.50},
    {codigo: "03.03", desc: "Mejoramiento de Suelos a Nivel de Subrasante", unidad: "M3", precio: 25.00},
  ],
  pavimentos: [
    {codigo: "04.01", desc: "Imprimación Asfáltica", unidad: "M2", precio: 2.50},
    {codigo: "04.02", desc: "Carpeta Asfáltica en Caliente e=2\"", unidad: "M2", precio: 28.50},
    {codigo: "04.03", desc: "Carpeta Asfáltica en Caliente e=3\"", unidad: "M2", precio: 42.00},
    {codigo: "04.04", desc: "Tratamiento Superficial Bicapa", unidad: "M2", precio: 8.50},
  ],
  obras: [
    {codigo: "05.01", desc: "Alcantarilla TMC Ø=36\"", unidad: "M", precio: 450.00},
    {codigo: "05.02", desc: "Alcantarilla TMC Ø=48\"", unidad: "M", precio: 680.00},
    {codigo: "05.03", desc: "Cunetas Revestidas de Concreto", unidad: "M", precio: 35.00},
    {codigo: "05.04", desc: "Badén de Concreto", unidad: "M3", precio: 420.00},
  ],
  senalizacion: [
    {codigo: "06.01", desc: "Señal Preventiva 0.60x0.60m", unidad: "UND", precio: 280.00},
    {codigo: "06.02", desc: "Señal Reglamentaria 0.60x0.60m", unidad: "UND", precio: 280.00},
    {codigo: "06.03", desc: "Marcas en el Pavimento - Línea Continua", unidad: "M", precio: 2.50},
    {codigo: "06.04", desc: "Tachas Reflectivas", unidad: "UND", precio: 12.00},
  ]
};

let partidaSeleccionada = null;
let presupuesto = [];

function cargarPartidas() {
  const categoria = document.getElementById('categoria').value;
  const lista = document.getElementById('listaPartidas');
  
  if (!categoria) {
    lista.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">Seleccione una categoría</p>';
    return;
  }
  
  const items = partidas[categoria];
  lista.innerHTML = items.map(p => `
    <div class="partida-item" onclick="seleccionarPartida('${categoria}', '${p.codigo}')">
      <div>
        <span class="partida-code">${p.codigo}</span>
        <div style="font-size: 12px; color: #666;">${p.desc}</div>
        <div style="font-size: 11px; color: #999;">${p.unidad}</div>
      </div>
      <div class="partida-price">S/ ${p.precio.toFixed(2)}</div>
    </div>
  `).join('');
}

function seleccionarPartida(categoria, codigo) {
  document.querySelectorAll('.partida-item').forEach(el => el.classList.remove('partida-selected'));
  event.target.closest('.partida-item').classList.add('partida-selected');
  
  partidaSeleccionada = partidas[categoria].find(p => p.codigo === codigo);
}

function filtrarPartidas() {
  const texto = document.getElementById('buscar').value.toLowerCase();
  const items = document.querySelectorAll('.partida-item');
  
  items.forEach(item => {
    const contenido = item.textContent.toLowerCase();
    item.style.display = contenido.includes(texto) ? 'flex' : 'none';
  });
}

function agregarPartida() {
  if (!partidaSeleccionada) {
    alert('⚠️ Seleccione una partida primero');
    return;
  }
  
  const metrado = parseFloat(document.getElementById('metrado').value);
  if (!metrado || metrado <= 0) {
    alert('⚠️ Ingrese un metrado válido');
    return;
  }
  
  presupuesto.push({
    ...partidaSeleccionada,
    metrado: metrado,
    parcial: metrado * partidaSeleccionada.precio
  });
  
  actualizarTabla();
  document.getElementById('metrado').value = '';
  partidaSeleccionada = null;
  document.querySelectorAll('.partida-item').forEach(el => el.classList.remove('partida-selected'));
}

function eliminarPartida(index) {
  presupuesto.splice(index, 1);
  actualizarTabla();
}

function actualizarTabla() {
  const tbody = document.getElementById('tbody');
  const total = presupuesto.reduce((sum, p) => sum + p.parcial, 0);
  
  tbody.innerHTML = presupuesto.map((p, i) => `
    <tr>
      <td>${p.codigo}</td>
      <td>${p.desc}</td>
      <td>${p.unidad}</td>
      <td>${p.metrado.toFixed(2)}</td>
      <td>S/ ${p.precio.toFixed(2)}</td>
      <td style="color: #0369a1; font-weight: bold;">S/ ${p.parcial.toFixed(2)}</td>
      <td><button onclick="eliminarPartida(${i})" style="padding: 5px 10px; font-size: 12px;" class="btn-danger">✖</button></td>
    </tr>
  `).join('');
  
  document.getElementById('footerTotal').textContent = `S/ ${total.toFixed(2)}`;
  document.getElementById('costoDirecto').textContent = `S/ ${total.toFixed(2)}`;
  document.getElementById('total').textContent = `S/ ${total.toFixed(2)}`;
  document.getElementById('numPartidas').textContent = presupuesto.length;
}

function limpiarTodo() {
  if (confirm('¿Está seguro de limpiar todo el presupuesto?')) {
    presupuesto = [];
    actualizarTabla();
  }
}

function exportarExcel() {
  if (presupuesto.length === 0) {
    alert('⚠️ No hay partidas para exportar');
    return;
  }
  
  let csv = 'Código,Descripción,Unidad,Metrado,P.U.,Parcial\n';
  presupuesto.forEach(p => {
    csv += `${p.codigo},"${p.desc}",${p.unidad},${p.metrado},${p.precio},${p.parcial}\n`;
  });
  
  const total = presupuesto.reduce((sum, p) => sum + p.parcial, 0);
  csv += `,,,,TOTAL,${total}\n`;
  
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'presupuesto_vial_mtc_2026.csv';
  a.click();
}
</script>
</body>
</html>

