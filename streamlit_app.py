import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import requests

import os
from dotenv import load_dotenv

load_dotenv()
VAPI_PUBLIC_KEY = os.getenv("VAPI_PUBLIC_KEY")       # Frontend only
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")   # Frontend only


# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
API_URL           = "https://mop-aged-lining.ngrok-free.dev"


# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dubai Hospital – AI Appointments",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #EFF3F8 !important;
}

/* Kill Streamlit chrome */
#MainMenu, footer, header { display: none !important; }

/* Kill ALL default Streamlit padding */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div:first-child {
    padding: 0 !important;
}

/* ── Design tokens ── */
:root {
    --blue:       #1A56DB;
    --blue-dk:    #1447B6;
    --blue-lt:    #EBF2FF;
    --teal:       #0694A2;
    --teal-lt:    #E0F7FA;
    --surface:    #FFFFFF;
    --bg:         #EFF3F8;
    --border:     #DDE3ED;
    --text:       #0F172A;
    --text-2:     #475569;
    --text-3:     #94A3B8;
    --green-bg:   #F0FFF4;
    --green:      #166534;
    --red-bg:     #FFF5F5;
    --red:        #9B2C2C;
    --r-sm:  8px;
    --r-md:  12px;
    --r-lg:  16px;
    --r-xl:  20px;
    --sh:    0 1px 4px rgba(0,0,0,.06);
    --sh-md: 0 4px 20px rgba(0,0,0,.09);
}

/* ── TOPBAR ── */
.topbar {
    height: 62px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    /* Use same horizontal padding as the body content */
    padding: 0 40px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 200;
}
.topbar-logo  { font-size: 19px; font-weight: 700; color: var(--blue); letter-spacing: -.4px; }
.topbar-sep   { color: var(--border); font-size: 20px; margin: 0 4px; }
.topbar-sub   { font-size: 14px; color: var(--text-3); font-weight: 400; }
.topbar-pill  {
    margin-left: auto;
    background: var(--teal-lt);
    color: var(--teal);
    font-size: 12px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 20px;
    letter-spacing: .3px;
}

/* ── OUTER wrapper — provides margins ── */
.outer-wrap {
    padding: 28px 40px;          /* ← LEFT + RIGHT MARGIN */
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 24px;
    align-items: start;
    max-width: 1440px;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    box-shadow: var(--sh);
    padding: 28px 30px;
}
.card-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Alert ── */
.alert {
    border-radius: var(--r-sm);
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 500;
    margin-top: 14px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
}
.alert-ok  { background: var(--green-bg); color: var(--green); }
.alert-err { background: var(--red-bg);   color: var(--red); }

/* ── Appointment result card ── */
.appt-card {
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 10px;
    background: var(--surface);
    transition: box-shadow .12s;
}
.appt-card:hover { box-shadow: var(--sh-md); }
.appt-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.appt-id  { font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-3); background:var(--bg); padding:3px 8px; border-radius:6px; }
.appt-status { font-size:11px; font-weight:700; letter-spacing:.4px; border-radius:20px; padding:4px 12px; }
.s-active   { background:var(--green-bg); color:var(--green); }
.s-canceled { background:var(--red-bg);   color:var(--red); }
.appt-name { font-size:15px; font-weight:600; color:var(--text); }
.appt-meta { font-size:13px; color:var(--text-3); margin-top:4px; display:flex; gap:16px; flex-wrap:wrap; }

/* ── Empty ── */
.empty { text-align:center; padding:36px 16px; color:var(--text-3); font-size:14px; }
.empty-ico { font-size:30px; margin-bottom:8px; }

/* ──────────────────────────────────────────
   STREAMLIT WIDGET OVERRIDES
   ────────────────────────────────────────── */

/* Labels */
label[data-testid="stWidgetLabel"] > div,
.stTextInput label, .stDateInput label,
.stNumberInput label, .stRadio label {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: var(--text-2) !important;
    text-transform: uppercase !important;
    letter-spacing: .6px !important;
}

/* Text inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 11px 14px !important;
    background: var(--bg) !important;
    color: var(--text) !important;
    box-shadow: none !important;
    transition: border-color .15s, background .15s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--blue) !important;
    background: var(--surface) !important;
    box-shadow: 0 0 0 3px rgba(26,86,219,.1) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder {
    color: var(--text-3) !important;
    font-size: 14px !important;
}

/* Date input */
.stDateInput > div > div > input {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    font-size: 15px !important;
    padding: 11px 14px !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* Number input */
.stNumberInput > div > div { gap: 6px !important; }

/* Primary button */
.stButton > button {
    background: var(--blue) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 11px 22px !important;
    width: 100% !important;
    letter-spacing: .2px !important;
    box-shadow: 0 2px 6px rgba(26,86,219,.28) !important;
    transition: opacity .12s, transform .1s !important;
    margin-top: 6px !important;
}
.stButton > button:hover  { opacity: .88 !important; }
.stButton > button:active { transform: scale(.98) !important; }

/* Radio */
.stRadio > div { flex-direction: row !important; flex-wrap: wrap !important; gap: 8px !important; }
.stRadio > div label {
    font-size: 14px !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--text-2) !important;
    cursor: pointer !important;
}
/* Tab-style radio pills */
.stRadio > div > label {
    border: 1.5px solid var(--border) !important;
    border-radius: 24px !important;
    padding: 6px 18px !important;
    background: var(--surface) !important;
    transition: all .12s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: var(--blue) !important;
    background: var(--blue-lt) !important;
    color: var(--blue) !important;
}

/* Spacing helpers */
div[data-testid="column"] { padding: 0 !important; }
.stMarkdown { margin: 0 !important; }

/* Remove Streamlit's own column gap (we use gap in outer-wrap) */
div[data-testid="stHorizontalBlock"] {
    gap: 16px !important;
    align-items: start !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def alert(msg, kind="ok"):
    cls = "alert-ok" if kind == "ok" else "alert-err"
    ico = "✓" if kind == "ok" else "✕"
    st.markdown(f"<div class='alert {cls}'><span>{ico}</span><span>{msg}</span></div>",
                unsafe_allow_html=True)

def appt_card(a):
    canceled  = a.get("canceled", False)
    status_cls = "s-canceled" if canceled else "s-active"
    status_txt = "Canceled"   if canceled else "Active"
    try:
        dt_fmt = datetime.fromisoformat(a["start_time"]).strftime("%d %b %Y · %H:%M")
    except Exception:
        dt_fmt = a.get("start_time", "—")
    st.markdown(f"""
    <div class="appt-card">
        <div class="appt-top">
            <span class="appt-id">#{a['id']}</span>
            <span class="appt-status {status_cls}">{status_txt}</span>
        </div>
        <div class="appt-name">{a['patient_name']}</div>
        <div class="appt-meta">
            <span>🗓 {dt_fmt}</span>
            <span>📋 {a['reason']}</span>
        </div>
    </div>""", unsafe_allow_html=True)

def api_post(path, payload):
    try:
        return requests.post(f"{API_URL}{path}", json=payload, timeout=10)
    except Exception:
        return None

def api_get(path):
    try:
        return requests.get(f"{API_URL}{path}", timeout=10)
    except Exception:
        return None

# ─────────────────────────────────────────────
#  TOPBAR  (full width, padded internally)
# ─────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <span style="font-size:30px">🏥</span>
    <span class="topbar-logo">Dubai Hospital</span>
    <span class="topbar-sep">|</span>
    <span class="topbar-sub">Appointment Management System</span>
    <span class="topbar-pill">🤖 Adam AI Active</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SPACER so content starts below sticky bar
# ─────────────────────────────────────────────
st.markdown("<div style='height:0'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TWO-COLUMN LAYOUT
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 0.46], gap="large")

# ════════════════════════════════════════════
#  LEFT  –  Appointment management
# ════════════════════════════════════════════
with left_col:
    # Add left margin via padding on a wrapper div
    st.markdown("<div style='padding-left:8px;'>", unsafe_allow_html=True)

    # Tab radio
    tab = st.radio(
        "tab",
        ["📝 Schedule", "❌ Cancel", "📅 List", "🔎 Search"],
        horizontal=True,
        label_visibility="collapsed",
        key="main_tab",
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── SCHEDULE ──────────────────────────────
    if tab == "📝 Schedule":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>📝 Schedule New Appointment</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            patient_name = st.text_input("Patient Full Name",
                placeholder="e.g. Ahmed Al Mansouri", key="s_name")
        with c2:
            reason = st.text_input("Reason / Department",
                placeholder="e.g. Cardiology Checkup", key="s_reason")

        start_time = st.text_input(
            "Date & Time  (YYYY-MM-DD HH:MM)",
            placeholder="2026-06-15  09:30", key="s_time")

        if st.button("Confirm Appointment →", key="btn_sched"):
            if not patient_name or not reason or not start_time:
                alert("Please fill in all fields.", "err")
            else:
                try:
                    dt_obj = datetime.strptime(start_time.strip(), "%Y-%m-%d %H:%M")
                    resp = api_post("/schedule_appointment/", {
                        "patient_name": patient_name,
                        "reason": reason,
                        "start_time": dt_obj.isoformat(),
                    })
                    if resp is None:
                        alert("Cannot reach server. Check API_URL.", "err")
                    elif resp.status_code == 200:
                        alert(f"Appointment confirmed. ID: {resp.json().get('id','—')}")
                    else:
                        alert(resp.json().get("detail", "Unknown error"), "err")
                except ValueError:
                    alert("Invalid format — use YYYY-MM-DD HH:MM", "err")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── CANCEL ────────────────────────────────
    elif tab == "❌ Cancel":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>❌ Cancel Appointment</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            cancel_name = st.text_input("Patient Name", key="c_name")
        with c2:
            cancel_date = st.date_input("Appointment Date", key="c_date")

        if st.button("Cancel Appointment →", key="btn_cancel"):
            if not cancel_name:
                alert("Please enter the patient name.", "err")
            else:
                resp = api_post("/cancel_appointment/", {
                    "patient_name": cancel_name,
                    "date": cancel_date.isoformat(),
                })
                if resp is None:
                    alert("Cannot reach server.", "err")
                elif resp.status_code == 200:
                    n = resp.json().get("canceled_count", 0)
                    alert(f"{n} appointment(s) successfully canceled.")
                else:
                    alert(resp.json().get("detail", "Error"), "err")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── LIST ──────────────────────────────────
    elif tab == "📅 List":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>📅 Appointments by Date</div>", unsafe_allow_html=True)

        list_date = st.date_input("Select Date", key="l_date")

        if st.button("Load Appointments →", key="btn_list"):
            resp = api_post("/list_appointments/", {"date": list_date.isoformat()})
            if resp is None:
                alert("Cannot reach server.", "err")
            elif resp.status_code == 200:
                data = resp.json()
                if not data:
                    st.markdown("<div class='empty'><div class='empty-ico'>📭</div>No appointments on this date.</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size:12px;font-weight:700;color:var(--text-3);text-transform:uppercase;letter-spacing:.5px;margin:14px 0 10px;'>{len(data)} Appointment(s) Found</div>",
                                unsafe_allow_html=True)
                    for a in data:
                        appt_card(a)
            else:
                alert(resp.json().get("detail", "Error"), "err")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── SEARCH ────────────────────────────────
    elif tab == "🔎 Search":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>🔎 Search Appointments</div>", unsafe_allow_html=True)

        mode = st.radio("Search by", ["ID", "Patient Name", "Date"],
                        horizontal=True, key="s_mode")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if mode == "ID":
            appt_id = st.number_input("Appointment ID", min_value=1, step=1, key="s_id")
            if st.button("Search →", key="btn_sid"):
                resp = api_get(f"/appointments/{int(appt_id)}")
                if resp is None:
                    alert("Cannot reach server.", "err")
                elif resp.status_code == 200:
                    appt_card(resp.json())
                else:
                    alert(resp.json().get("detail", "Not found"), "err")

        elif mode == "Patient Name":
            s_name = st.text_input("Patient name", key="s_pname")
            if st.button("Search →", key="btn_sname"):
                resp = api_post("/search_appointments/", {"patient_name": s_name})
                if resp is None:
                    alert("Cannot reach server.", "err")
                elif resp.status_code == 200:
                    results = resp.json()
                    if not results:
                        st.markdown("<div class='empty'><div class='empty-ico'>🔍</div>No results found.</div>",
                                    unsafe_allow_html=True)
                    else:
                        for a in results:
                            appt_card(a)
                else:
                    alert(resp.json().get("detail", "Error"), "err")

        else:
            s_date = st.date_input("Date", key="s_date2")
            if st.button("Search →", key="btn_sdate"):
                resp = api_post("/list_appointments/", {"date": s_date.isoformat()})
                if resp is None:
                    alert("Cannot reach server.", "err")
                elif resp.status_code == 200:
                    results = resp.json()
                    if not results:
                        st.markdown("<div class='empty'><div class='empty-ico'>📭</div>No results on this date.</div>",
                                    unsafe_allow_html=True)
                    else:
                        for a in results:
                            appt_card(a)
                else:
                    alert(resp.json().get("detail", "Error"), "err")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close padding-left wrapper

# ════════════════════════════════════════════
#  RIGHT  –  AI Voice Assistant (Adam)
# ════════════════════════════════════════════
with right_col:
    # Add right margin via padding
    st.markdown("<div style='padding-right:8px;'>", unsafe_allow_html=True)

    # ── Agent identity card ──
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1A56DB 0%, #0694A2 100%);
        border-radius: 18px;
        padding: 18px 20px;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(26,86,219,.25);
    ">
        <div style="
            width: 50px; height: 50px;
            background: rgba(255,255,255,.2);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; flex-shrink: 0;
        ">🤖</div>
        <div style="flex:1; min-width:0;">
            <div style="font-size:17px; font-weight:700; letter-spacing:-.2px;">Adam</div>
            <div style="font-size:12px; opacity:.85; margin-top:2px;">
                Dubai Hospital · AI Receptionist
            </div>
        </div>
        <div style="
            background: rgba(255,255,255,.22);
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .5px;
            flex-shrink: 0;
        ">● LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats strip ──
    st.markdown("""
    <div style="
        display: grid;
        grid-template-columns: repeat(3,1fr);
        gap: 10px;
        margin-bottom: 16px;
    ">
        <div style="background:#fff;border:1px solid #DDE3ED;border-radius:12px;
                    padding:12px 8px;text-align:center;">
            <div style="font-size:20px;font-weight:700;color:#1A56DB;line-height:1;">24/7</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;text-transform:uppercase;
                        letter-spacing:.5px;margin-top:4px;">Available</div>
        </div>
        <div style="background:#fff;border:1px solid #DDE3ED;border-radius:12px;
                    padding:12px 8px;text-align:center;">
            <div style="font-size:20px;font-weight:700;color:#1A56DB;line-height:1;">&lt;1s</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;text-transform:uppercase;
                        letter-spacing:.5px;margin-top:4px;">Response</div>
        </div>
        <div style="background:#fff;border:1px solid #DDE3ED;border-radius:12px;
                    padding:12px 8px;text-align:center;">
            <div style="font-size:20px;font-weight:700;color:#0694A2;line-height:1;">AR/EN</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;text-transform:uppercase;
                        letter-spacing:.5px;margin-top:4px;">Language</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Vapi widget ──
    vapi_html = f"""
<style>
  html, body {{ margin:0; padding:0; overflow:hidden; background:#EFF3F8; }}
  .wrap {{
    width: 100%; height: 100%;
    background: #EFF3F8;
    border-radius: 16px;
    overflow: hidden;
    display: flex; flex-direction: column;
  }}
  vapi-widget {{
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    flex: 1;
  }}
</style>
<div class="wrap">
  <script src="https://unpkg.com/@vapi-ai/client-sdk-react/dist/embed/widget.umd.js" defer></script>
  <vapi-widget
      public-key="{VAPI_PUBLIC_KEY}"
      assistant-id="{VAPI_ASSISTANT_ID}"
      mode="voice"
      theme="light"
      size="full"
      radius="large"
      main-label="Adam – AI Receptionist"
      start-button-text="📞 Start Call"
      end-button-text="End Call"
      empty-voice-message="Hello! I'm Adam from Dubai Hospital. How can I help you today?">
  </vapi-widget>
</div>"""
    components.html(vapi_html, height=320, scrolling=False)

    # ── Tips ──
    st.markdown("""
    <div style="
        background: #fff;
        border: 1px solid #DDE3ED;
        border-radius: 14px;
        padding: 16px 18px;
        margin-top: 14px;
    ">
        <div style="font-size:11px;font-weight:700;color:#475569;
                    text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;">
            💬 Try saying to Adam
        </div>
        <div style="font-size:13px;color:#64748B;line-height:2;">
            · "Book an appointment for Ahmed on June 20"<br>
            · "I need to cancel my appointment"<br>
            · "Is Dr. Hassan available tomorrow?"<br>
            · "Reschedule my appointment to next week"
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close padding-right wrapper