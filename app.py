import streamlit as st
import yaml
from pathlib import Path

# ── Configuración de página ──────────────────────────────────
st.set_page_config(
    page_title="Monográficos | Transformación Digital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Estilos CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* Reset y base */
* { box-sizing: border-box; }

.stApp {
    background: #f4f1ec;
    font-family: 'Inter', sans-serif;
}

/* Ocultar elementos de Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Forzar fondo de toda la app en login */
.stApp { background: #0d1b2a !important; }

/* ── LOGIN ── */
.login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    position: relative;
    overflow: hidden;
}

.login-wrapper::before {
    content: '';
    position: fixed;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,90,160,0.3) 0%, transparent 70%);
    top: -100px; left: -100px;
    pointer-events: none;
    z-index: 0;
}

.login-wrapper::after {
    content: '';
    position: fixed;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,160,120,0.2) 0%, transparent 70%);
    bottom: -50px; right: -50px;
    pointer-events: none;
    z-index: 0;
}

.login-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 56px 48px;
    width: 420px;
    position: relative;
    z-index: 1;
    text-align: center;
}

.login-ministerio {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 8px;
}

.login-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
    line-height: 1.3;
}

.login-subtitulo {
    font-size: 12px;
    color: rgba(255,255,255,0.35);
    margin-bottom: 40px;
    font-weight: 300;
}

.login-divider {
    width: 40px;
    height: 2px;
    background: #005aa0;
    margin: 0 auto 40px;
}

/* ── CABECERA PORTAL ── */
.portal-header {
    background: #0d1b2a;
    padding: 28px 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid #005aa0;
}

.portal-header-left {
    display: flex;
    flex-direction: column;
}

.portal-ministerio-label {
    font-family: 'Syne', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 4px;
}

.portal-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
}

.portal-subtitulo {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    font-weight: 300;
    margin-top: 2px;
}

/* ── CONTENIDO PRINCIPAL ── */
.portal-body {
    padding: 48px 60px;
}

.seccion-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 32px;
    padding-bottom: 12px;
    border-bottom: 1px solid #ddd;
}

/* ── TARJETAS DE MONOGRÁFICO ── */
.card-mono {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px 28px;
    border: 1px solid #e8e4df;
    transition: all 0.3s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.card-mono::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--card-color, #005aa0);
}

.card-mono:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    border-color: var(--card-color, #005aa0);
}

.card-icono {
    font-size: 40px;
    margin-bottom: 16px;
    display: block;
}

.card-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #0d1b2a;
    margin-bottom: 10px;
}

.card-desc {
    font-size: 13px;
    color: #777;
    line-height: 1.6;
    margin-bottom: 20px;
    font-weight: 300;
}

.card-ediciones-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #aaa;
    margin-bottom: 8px;
}

.badge-edicion {
    display: inline-block;
    background: #f4f1ec;
    border: 1px solid #e0dbd4;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 500;
    color: #555;
    margin-right: 6px;
    margin-bottom: 6px;
}

.badge-edicion-latest {
    background: var(--card-color, #005aa0);
    color: white;
    border-color: var(--card-color, #005aa0);
}

/* ── DETALLE MONOGRÁFICO ── */
.detalle-header {
    background: #0d1b2a;
    padding: 40px 60px;
    position: relative;
    overflow: hidden;
}

.detalle-header::after {
    content: attr(data-icono);
    position: absolute;
    right: 60px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 120px;
    opacity: 0.08;
}

.detalle-back {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 1px;
    margin-bottom: 16px;
    cursor: pointer;
}

.detalle-icono-titulo {
    display: flex;
    align-items: center;
    gap: 20px;
}

.detalle-icono {
    font-size: 52px;
}

.detalle-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: white;
}

.detalle-desc {
    font-size: 14px;
    color: rgba(255,255,255,0.5);
    margin-top: 12px;
    font-weight: 300;
    max-width: 600px;
    line-height: 1.7;
}

.detalle-body {
    padding: 48px 60px;
}

.edicion-card {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    border: 1px solid #e8e4df;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s ease;
}

.edicion-card:hover {
    border-color: #005aa0;
    box-shadow: 0 8px 30px rgba(0,90,160,0.08);
}

.edicion-card-left {
    display: flex;
    align-items: center;
    gap: 20px;
}

.edicion-numero {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #e8e4df;
    min-width: 40px;
}

.edicion-info-nombre {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #0d1b2a;
}

.edicion-info-fecha {
    font-size: 12px;
    color: #aaa;
    margin-top: 2px;
}

.latest-badge {
    background: #005aa0;
    color: white;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 10px;
}

.btn-acceder {
    display: inline-block;
    background: #0d1b2a;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.5px;
    transition: background 0.2s;
}

.btn-acceder:hover {
    background: #005aa0;
    color: white;
    text-decoration: none;
}

.btn-descargar {
    display: inline-block;
    background: transparent;
    color: #005aa0;
    border: 1px solid #005aa0;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.5px;
    margin-left: 8px;
    transition: all 0.2s;
}

.btn-descargar:hover {
    background: #005aa0;
    color: white;
    text-decoration: none;
}

.badge-proximamente {
    display: inline-block;
    background: #f4f1ec;
    border: 1px dashed #ccc;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 500;
    color: #aaa;
    letter-spacing: 0.5px;
}

/* Streamlit input override */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 18px !important;
    font-size: 14px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255,255,255,0.2) !important;
}

div[data-testid="stTextInput"] label {
    color: rgba(255,255,255,0.4) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stButton"] button {
    background: #005aa0 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}

div[data-testid="stButton"] button:hover {
    background: #004080 !important;
}

div[data-testid="stAlert"] {
    background: rgba(220,50,50,0.15) !important;
    border: 1px solid rgba(220,50,50,0.3) !important;
    border-radius: 10px !important;
    color: #ff8080 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Cargar configuración ──────────────────────────────────────
@st.cache_data
def cargar_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = cargar_config()
monograficos = config["monograficos"]

# ── Estado de sesión ──────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "vista" not in st.session_state:
    st.session_state.vista = "catalogo"
if "mono_seleccionado" not in st.session_state:
    st.session_state.mono_seleccionado = None

# ────────────────────────────────────────────────────────────────
# PANTALLA DE LOGIN
# ────────────────────────────────────────────────────────────────
if not st.session_state.autenticado:
    # Fondo oscuro para toda la app durante el login
    st.markdown("""
    <style>
    .stApp { background: #0d1b2a !important; }
    .stAppViewContainer { background: #0d1b2a !important; }
    section[data-testid="stAppViewContainer"] { background: #0d1b2a !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div class="login-card">
            <div class="login-ministerio">Ministerio para la Transformación Digital y de la Función Pública</div>
            <div class="login-titulo">Biblioteca de<br>Monográficos</div>
            <div class="login-subtitulo">Subdirección General de Análisis de Mercado<br>y Evolución Tecnológica</div>
            <div class="login-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        clave = st.text_input("CLAVE DE ACCESO", type="password", placeholder="••••••••••")

        if st.button("ACCEDER"):
            clave_correcta = st.secrets.get("ACCESS_PASSWORD", "demo1234")
            if clave == clave_correcta:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Contacta con tu equipo.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ────────────────────────────────────────────────────────────────
# PORTAL — CATÁLOGO
# ────────────────────────────────────────────────────────────────
if st.session_state.vista == "catalogo":

    # Cabecera
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("""
        <div class="portal-header">
            <div class="portal-header-left">
                <div class="portal-ministerio-label">Ministerio para la Transformación Digital y de la Función Pública</div>
                <div class="portal-titulo">Biblioteca de Monográficos</div>
                <div class="portal-subtitulo">Subdirección General de Análisis de Mercado y Evolución Tecnológica</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Botón cerrar sesión
    with col_h2:
        st.markdown("<div style='padding-top:36px'>", unsafe_allow_html=True)
        if st.button("🔒 Cerrar sesión"):
            st.session_state.autenticado = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Cuerpo
    st.markdown('<div class="portal-body">', unsafe_allow_html=True)
    st.markdown('<div class="seccion-titulo">Monográficos disponibles</div>', unsafe_allow_html=True)

    # Grid de tarjetas
    cols = st.columns(3, gap="large")
    for i, mono in enumerate(monograficos):
        with cols[i % 3]:
            n_ediciones = len(mono["ediciones"])
            ultima = mono["ediciones"][-1]

            badges_html = ""
            for j, ed in enumerate(mono["ediciones"]):
                clase = "badge-edicion-latest" if j == len(mono["ediciones"]) - 1 else ""
                badges_html += f'<span class="badge-edicion {clase}" style="--card-color:{mono["color"]}">{ed["nombre"]} · {ed["fecha"]}</span>'

            st.markdown(f"""
            <div class="card-mono" style="--card-color:{mono['color']}">
                <span class="card-icono">{mono['icono']}</span>
                <div class="card-titulo">{mono['titulo']}</div>
                <div class="card-desc">{mono['descripcion']}</div>
                <div class="card-ediciones-label">{n_ediciones} edición{"es" if n_ediciones > 1 else ""}</div>
                {badges_html}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Ver monográfico →", key=f"btn_{i}"):
                st.session_state.mono_seleccionado = i
                st.session_state.vista = "detalle"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# PORTAL — DETALLE DE MONOGRÁFICO
# ────────────────────────────────────────────────────────────────
elif st.session_state.vista == "detalle":
    mono = monograficos[st.session_state.mono_seleccionado]

    # Cabecera del detalle
    st.markdown(f"""
    <div class="detalle-header" data-icono="{mono['icono']}">
        <div class="detalle-back">← Biblioteca de Monográficos</div>
        <div class="detalle-icono-titulo">
            <span class="detalle-icono">{mono['icono']}</span>
            <div>
                <div class="detalle-titulo">{mono['titulo']}</div>
            </div>
        </div>
        <div class="detalle-desc">{mono['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)

    col_b, _ = st.columns([1, 5])
    with col_b:
        if st.button("← Volver al catálogo"):
            st.session_state.vista = "catalogo"
            st.rerun()

    # Ediciones
    st.markdown('<div class="detalle-body">', unsafe_allow_html=True)
    st.markdown('<div class="seccion-titulo">Ediciones disponibles</div>', unsafe_allow_html=True)

    total = len(mono["ediciones"])
    for j, ed in enumerate(reversed(mono["ediciones"])):
        es_ultima = (j == 0)
        num_real = total - j

        latest_badge = '<span class="latest-badge">Última edición</span>' if es_ultima else ""

        tiene_url = bool(ed.get('sharepoint_url', '').strip())

        if tiene_url:
            botones_html = f"""
                <a href="{ed['sharepoint_url']}" target="_blank" class="btn-acceder">Ver documento ↗</a>
                <a href="{ed['sharepoint_url']}&download=1" target="_blank" class="btn-descargar">⬇ Descargar</a>
            """
        else:
            botones_html = '<span class="badge-proximamente">🔒 Próximamente</span>'

        st.markdown(f"""
        <div class="edicion-card">
            <div class="edicion-card-left">
                <div class="edicion-numero">0{num_real}</div>
                <div>
                    <div class="edicion-info-nombre">{ed['nombre']} {latest_badge}</div>
                    <div class="edicion-info-fecha">Publicado en {ed['fecha']}</div>
                </div>
            </div>
            <div>
                {botones_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
