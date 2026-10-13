const states = [
  { id: "idle", label: "Reposo", frames: 6, description: "Respiración, parpadeo y energía tranquila." },
  { id: "running-right", label: "Carrera derecha", frames: 8, description: "Desplazamiento enérgico hacia la derecha." },
  { id: "running-left", label: "Carrera izquierda", frames: 8, description: "Desplazamiento enérgico hacia la izquierda." },
  { id: "waving", label: "Saludo", frames: 4, description: "Un saludo alegre y legible a tamaño pequeño." },
  { id: "jumping", label: "Salto", frames: 5, description: "Anticipación, impulso, ápice y aterrizaje." },
  { id: "failed", label: "Fallo", frames: 8, description: "Decepción breve con recuperación optimista." },
  { id: "waiting", label: "Espera", frames: 6, description: "Paciencia, curiosidad y atención al usuario." },
  { id: "running", label: "Trabajando", frames: 6, description: "Concentración y movimiento durante una tarea." },
  { id: "review", label: "Revisión", frames: 6, description: "Inspección y aprobación del resultado." },
  { id: "look-a", label: "Miradas A", frames: 8, description: "Direcciones de mirada entre 0° y 157.5°." },
  { id: "look-b", label: "Miradas B", frames: 8, description: "Direcciones de mirada entre 180° y 337.5°." }
];

const $ = selector => document.querySelector(selector);
const sprite = $("#sprite");
const stage = $("#stage");
const grid = $("#state-grid");
let active = states[0];
let frame = 0;
let playing = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let interval;

function framePath(state, index) {
  return `../assets/frames/${state}/${String(index).padStart(2, "0")}.png`;
}

function renderFrame() {
  sprite.src = framePath(active.id, frame);
  $("#frame").textContent = String(frame + 1).padStart(2, "0");
  $("#total").textContent = `/ ${String(active.frames).padStart(2, "0")}`;
}

function restart() {
  clearInterval(interval);
  $("#play").textContent = playing ? "❚❚" : "▶";
  $("#play").setAttribute("aria-label", playing ? "Pausar animación" : "Reproducir animación");
  if (playing) interval = setInterval(() => { frame = (frame + 1) % active.frames; renderFrame(); }, Number($("#speed").value));
}

function selectState(state) {
  active = state;
  frame = 0;
  document.querySelectorAll(".state-card").forEach(card => card.classList.toggle("active", card.dataset.state === state.id));
  $("#state-description").textContent = state.description;
  renderFrame();
  restart();
}

states.forEach(state => {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "state-card";
  button.dataset.state = state.id;
  button.innerHTML = `<img src="${framePath(state.id, 0)}" alt=""><span><strong>${state.label}</strong><small>${state.frames} frames</small></span>`;
  button.addEventListener("click", () => selectState(state));
  grid.append(button);
});

$("#play").addEventListener("click", () => { playing = !playing; restart(); });
$("#previous").addEventListener("click", () => { frame = (frame - 1 + active.frames) % active.frames; renderFrame(); });
$("#next").addEventListener("click", () => { frame = (frame + 1) % active.frames; renderFrame(); });
$("#speed").addEventListener("input", event => { $("#speed-value").textContent = `${event.target.value} ms`; restart(); });
$("#scale").addEventListener("input", event => { sprite.style.transform = `scale(${event.target.value})`; $("#scale-value").textContent = `${event.target.value}×`; });
$("#ground-toggle").addEventListener("change", event => { $(".ground").hidden = !event.target.checked; });
document.querySelectorAll(".swatch").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".swatch").forEach(item => item.classList.remove("active"));
  button.classList.add("active");
  stage.className = `stage ${button.dataset.background}`;
}));

selectState(states[0]);
