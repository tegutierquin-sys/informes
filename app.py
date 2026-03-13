import streamlit as st
import yaml
from pathlib import Path

LOGO_B64 = "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"

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
section.main > div { padding-left: 0 !important; padding-right: 0 !important; }

/* Márgenes en contenido */
.contenido-interior {
    padding-left: 72px !important;
    padding-right: 72px !important;
}

/* ── LOGIN: fondo degradado institucional ── */
.tarjeta-login {
    background: white;
    border-radius: 12px;
    padding: 40px 48px;
    max-width: 480px;
    margin: 40px auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    text-align: center;
}
.logo-container { text-align: center; margin-bottom: 24px; }
.separador-amarillo {
    border: none;
    border-top: 2px solid #F2C811;
    margin: 16px 0 24px 0;
}
.login-titulo-inst {
    font-size: 1.3rem; font-weight: 700; color: #003366;
    text-align: center; line-height: 1.4; margin-bottom: 4px;
}
.login-subtitulo-inst {
    font-size: 1rem; color: #005A9C;
    text-align: center; font-weight: 600; margin-bottom: 8px;
}
.login-label { font-size: 0.85rem; color: #666; margin-bottom: 8px; text-align: center; }
.login-pie { text-align: center; font-size: 0.75rem; color: rgba(255,255,255,0.7); margin-top: 16px; }

/* ── CABECERA PORTAL ── */
.portal-header {
    background: linear-gradient(160deg, #003366 0%, #005A9C 60%, #F2C811 100%);
    padding: 20px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #F2C811;
}

.portal-header-left {
    display: flex;
    align-items: center;
    gap: 24px;
}

.portal-header-logo img {
    height: 48px;
    display: block;
}

.portal-header-text {
    display: flex;
    flex-direction: column;
}

.portal-ministerio-label {
    font-family: 'Syne', sans-serif;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.65);
    margin-bottom: 2px;
}

.portal-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
}

.portal-subtitulo {
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    font-weight: 300;
    margin-top: 1px;
}

/* ── CONTENIDO PRINCIPAL ── */
.portal-body {
    padding: 32px 60px 48px 80px;
}

.seccion-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #ddd;
}

/* ── TARJETAS DE MONOGRÁFICO ── */
.card-mono {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 20px;
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
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.card-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #0d1b2a;
    margin-bottom: 6px;
}

.card-desc {
    font-size: 11px;
    color: #777;
    line-height: 1.5;
    margin-bottom: 12px;
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
    background: linear-gradient(160deg, #003366 0%, #005A9C 60%, #F2C811 100%);
    padding: 28px 48px;
    position: relative;
    overflow: hidden;
    border-bottom: 3px solid #F2C811;
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
    padding: 32px 60px 48px 80px;
}

.edicion-card {
    background: white;
    border-radius: 16px;
    padding: 20px 32px;
    border: 1px solid #e8e4df;
    margin-bottom: 20px;
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
    background: #ffffff;
    color: #003366 !important;
    border: 2px solid #003366;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
    letter-spacing: 0.5px;
    transition: all 0.2s;
}

.btn-acceder:hover {
    background: #003366;
    color: white !important;
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

.extra-links-row {
    margin-top: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.btn-extra {
    display: inline-block;
    background: #fff8e1;
    color: #7a5500 !important;
    border: 1px solid #F2C811;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.3px;
    transition: all 0.2s;
}

.btn-extra:hover {
    background: #F2C811;
    color: #003366 !important;
    text-decoration: none;
}

/* Streamlit input override */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    -webkit-text-security: disc !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 18px !important;
    font-size: 14px !important;
    caret-color: #000000 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(0,0,0,0.3) !important;
    -webkit-text-security: none !important;
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

/* ── FOOTER INSTITUCIONAL ── */
.footer-institucional {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid #e0e0e0;
    padding: 8px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 9998;
    gap: 16px;
}

.footer-bloque {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}

.footer-sep {
    width: 1px;
    height: 36px;
    background: #ccc;
    flex-shrink: 0;
}

.footer-texto {
    font-size: 9px;
    color: #444;
    line-height: 1.3;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.footer-texto strong {
    display: block;
    font-size: 10px;
    color: #003366;
}

.footer-estrella {
    color: #003399;
    font-size: 18px;
    letter-spacing: -2px;
}

.footer-eu-text {
    font-size: 9px;
    color: #333;
    line-height: 1.4;
}

.footer-eu-text strong {
    font-size: 10px;
    color: #003399;
    display: block;
}

.footer-prtr {
    font-size: 9px;
    color: #c0392b;
    font-weight: 700;
    line-height: 1.3;
    text-transform: uppercase;
}

/* Espacio para que el footer no tape contenido */
.stApp > div:last-child {
    padding-bottom: 60px;
}

/* Botón cerrar sesión flotante */
.cerrar-sesion-flotante {
    position: fixed;
    top: 16px;
    right: 24px;
    z-index: 9999;
}

.btn-cerrar {
    background: rgba(255,255,255,0.15);
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    backdrop-filter: blur(10px);
    letter-spacing: 0.5px;
}

.btn-cerrar:hover {
    background: rgba(255,255,255,0.25);
}

div[data-testid="stAlert"] {
    background: rgba(220,50,50,0.15) !important;
    border: 1px solid rgba(220,50,50,0.3) !important;
    border-radius: 10px !important;
    color: #ff8080 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Footer institucional (se muestra siempre) ──────────────────
FOOTER_HTML = """
<div class="footer-institucional">
    <div class="footer-bloque">
        <span style="font-size:20px">🇪🇸</span>
        <div>
            <div class="footer-texto"><strong>Gobierno de España</strong></div>
            <div class="footer-texto" style="font-size:8px;color:#888">Agenda 2030</div>
        </div>
    </div>
    <div class="footer-sep"></div>
    <div class="footer-bloque">
        <div class="footer-texto">
            <strong>Ministerio para la Transformación Digital</strong>
            y de la Función Pública
        </div>
    </div>
    <div class="footer-sep"></div>
    <div class="footer-bloque">
        <div class="footer-texto">
            <strong>Secretaría de Estado de Telecomunicaciones</strong>
            e Infraestructuras Digitales
        </div>
    </div>
    <div class="footer-sep"></div>
    <div class="footer-bloque">
        <div class="footer-estrella">★ ★ ★<br>★ ★ ★<br>★ ★ ★</div>
        <div class="footer-eu-text">
            <strong>Financiado por la<br>Unión Europea</strong>
            NextGenerationEU
        </div>
    </div>
    <div class="footer-sep"></div>
    <div class="footer-bloque">
        <div style="background:#c0392b;color:white;font-weight:700;font-size:8px;padding:4px 8px;border-radius:3px;line-height:1.4;text-align:center">
            Plan de Recuperación,<br>Transformación y Resiliencia
        </div>
    </div>
</div>
"""

# ── Cargar configuración ──────────────────────────────────────
@st.cache_data(ttl=0)
def cargar_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = cargar_config()
monograficos = config["monograficos"]

# ── Mostrar footer siempre ───────────────────────────────────
st.markdown(FOOTER_HTML, unsafe_allow_html=True)

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
    # Fondo degradado institucional
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(160deg, #003366 0%, #005A9C 60%, #F2C811 100%) !important; }
    header[data-testid="stHeader"] { background: transparent; }
    .stButton > button {
        background-color: #003366 !important; color: white !important;
        border: none !important; border-radius: 6px !important;
        font-weight: 600 !important; padding: 10px !important; width: 100%;
    }
    .stButton > button:hover { background-color: #005A9C !important; }
    div[data-testid="stTextInput"] input {
        padding: 6px 12px !important;
        font-size: 13px !important;
        height: 36px !important;
        min-height: 36px !important;
    }
    div[data-baseweb="input"] {
        min-height: 36px !important;
        height: 36px !important;
    }
    div[data-baseweb="base-input"] {
        min-height: 36px !important;
        height: 36px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="tarjeta-login">
            <div class="logo-container">
                <img src="data:image/png;base64,{LOGO_B64}" width="320" />
            </div>
            <hr class="separador-amarillo"/>
            <p class="login-titulo-inst">Biblioteca de Monográficos</p>
            <p class="login-subtitulo-inst">Subdirección General de Análisis de Mercado y Evolución Tecnológica</p>
            <p class="login-label">Introduce la clave para acceder</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        clave = st.text_input("Clave", type="password",
                              label_visibility="collapsed",
                              placeholder="Contraseña...")
        if st.button("Entrar", use_container_width=True):
            clave_correcta = st.secrets.get("ACCESS_PASSWORD", "demo1234")
            if clave == clave_correcta:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Contacta con tu equipo.")

    st.markdown('<p class="login-pie">S.G. de Análisis del Mercado y Evolución Tecnológica</p>', unsafe_allow_html=True)
    st.stop()

# ────────────────────────────────────────────────────────────────
# PORTAL — CATÁLOGO
# ────────────────────────────────────────────────────────────────
if st.session_state.vista == "catalogo":

    # Cabecera
    st.markdown(f"""
    <div class="portal-header">
        <div class="portal-header-left">
            <div class="portal-header-logo">
                <img src="data:image/png;base64,{LOGO_B64}" />
            </div>
            <div class="portal-header-text">
                <div class="portal-ministerio-label">Ministerio para la Transformación Digital y de la Función Pública</div>
                <div class="portal-titulo">Biblioteca de Monográficos</div>
                <div class="portal-subtitulo">Subdirección General de Análisis de Mercado y Evolución Tecnológica</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botón cerrar sesión flotante
    st.markdown('<div class="cerrar-sesion-flotante">', unsafe_allow_html=True)
    if st.button("🔒 Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Cuerpo
    st.markdown('<div class="portal-body"><div class="contenido-interior">', unsafe_allow_html=True)
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

    st.markdown('</div></div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
# PORTAL — DETALLE DE MONOGRÁFICO
# ────────────────────────────────────────────────────────────────
elif st.session_state.vista == "detalle":
    mono = monograficos[st.session_state.mono_seleccionado]

    # Cabecera del detalle
    icono = mono['icono']
    titulo = mono['titulo']
    descripcion = mono['descripcion']
    st.markdown(f"""
    <div class="detalle-header" data-icono="{icono}">
        <div class="portal-header-left" style="margin-bottom:20px;">
            <div class="portal-header-logo">
                <img src="data:image/png;base64,{LOGO_B64}" />
            </div>
            <div class="portal-header-text">
                <div class="portal-ministerio-label">Ministerio para la Transformación Digital y de la Función Pública</div>
                <div class="portal-titulo">Biblioteca de Monográficos</div>
                <div class="portal-subtitulo">Subdirección General de Análisis de Mercado y Evolución Tecnológica</div>
            </div>
        </div>
        <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 20px;">
            <div class="detalle-icono-titulo">
                <span class="detalle-icono">{icono}</span>
                <div>
                    <div class="detalle-titulo">{titulo}</div>
                </div>
            </div>
            <div class="detalle-desc">{descripcion}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_b, _ = st.columns([1, 5])
    with col_b:
        if st.button("← Volver al catálogo"):
            st.session_state.vista = "catalogo"
            st.rerun()

    # Ediciones
    st.markdown('<div class="detalle-body"><div class="contenido-interior">', unsafe_allow_html=True)
    st.markdown('<div class="seccion-titulo">Ediciones disponibles</div>', unsafe_allow_html=True)

    total = len(mono["ediciones"])
    for j, ed in enumerate(reversed(mono["ediciones"])):
        es_ultima = (j == 0)
        num_real = total - j

        latest_badge = '<span class="latest-badge">Última edición</span>' if es_ultima else ""

        tiene_url = bool(ed.get('sharepoint_url', '').strip())
        url = ed.get('sharepoint_url', '')
        extra_links = ed.get('extra_links', [])
        nombre_ed = ed['nombre']
        fecha_ed = ed['fecha']

        if tiene_url:
            botones_html = (
                '<a href="' + url + '" target="_blank" class="btn-acceder">Ver documento ↗</a>'
            )
        else:
            botones_html = '<span class="badge-proximamente">🔒 Próximamente</span>'

        extras_html = ''.join(
            '<a href="' + ex["url"] + '" target="_blank" class="btn-extra">' + ex["etiqueta"] + '</a>'
            for ex in extra_links
        )
        extras_row = '<div class="extra-links-row">' + extras_html + '</div>' if extras_html else ''

        extra_section = (
            '<div class="extra-links-row" style="margin-top:10px;padding-top:10px;border-top:1px solid #eee;width:100%">'
            + extras_html + '</div>'
        ) if extras_html else ''

        card_html = (
            '<div class="edicion-card" style="flex-wrap:wrap;">'
            '<div class="edicion-card-left">'
            '<div class="edicion-numero">0' + str(num_real) + '</div>'
            '<div>'
            '<div class="edicion-info-nombre">' + nombre_ed + ' ' + latest_badge + '</div>'
            '<div class="edicion-info-fecha">Publicado en ' + fecha_ed + '</div>'
            '</div>'
            '</div>'
            '<div>' + botones_html + '</div>'
            + extra_section +
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
