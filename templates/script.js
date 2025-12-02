const API_URL = "https://sensor-ultrasonico.onrender.com/api/distancia";
// Reemplazar cuando tu app en Render esté activa

const tablaBody = document.getElementById("tabla-body");
const estadoTexto = document.getElementById("estado-texto");
const statusDot = document.querySelector(".status-dot");

async function cargarDatos() {
  try {
    const res = await fetch(API_URL, { cache: "no-cache" });

    if (!res.ok) throw new Error("Error al obtener datos");

    const data = await res.json();

    tablaBody.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
      tablaBody.innerHTML = "<tr><td colspan='2'>Sin datos aún</td></tr>";
      actualizarEstado(false);
      return;
    }

    actualizarEstado(true);

    data.slice().reverse().forEach(item => {
      const fila = document.createElement("tr");
      fila.classList.add("nueva-fila");
      fila.innerHTML = `
        <td>${item.fecha}</td>
        <td>${item.distancia} cm</td>
      `;
      tablaBody.appendChild(fila);

      // Animación
      setTimeout(() => fila.classList.remove("nueva-fila"), 300);
    });

  } catch (error) {
    console.warn("Fallo de conexión:", error);
    tablaBody.innerHTML = "<tr><td colspan='2'>Error al conectar con servidor</td></tr>";
    actualizarEstado(false);
  }
}

function actualizarEstado(conectado) {
  if (conectado) {
    statusDot.style.background = "#2ecc71"; // Verde
    estadoTexto.textContent = "Recibiendo datos...";
  } else {
    statusDot.style.background = "#e74c3c"; // Rojo
    estadoTexto.textContent = "Sin conexión";
  }
}

// Primera carga + actualización periódica
cargarDatos();
setInterval(cargarDatos, 4000);
