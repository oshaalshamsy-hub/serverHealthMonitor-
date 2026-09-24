from pathlib import Path
import textwrap, zipfile, json

base = Path("/mnt/data/ServerHealthMonitoring_Streamlit")
base.mkdir(exist_ok=True)

app = r'''import streamlit as st
import psutil
import platform
import socket
from datetime import datetime
from pathlib import Path

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="SERVERHub | Server Health Monitoring",
    page_icon="🖥️",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

pages = [
    "🏠 Dashboard",
    "ℹ️ System Info",
    "⚙️ CPU Monitor",
    "🧠 RAM Monitor",
    "💾 Disk Monitor",
    "🌐 Network Monitor",
    "📋 Processes",
    "💻 Operating Systems",
    "⚠️ Alerts",
    "📄 Reports",
    "🛠️ Admin Control"
]

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

if "site_name" not in st.session_state:
    st.session_state.site_name = "ServerHealthMonitoring"

if "cpu_warning" not in st.session_state:
    st.session_state.cpu_warning = 70

if "ram_warning" not in st.session_state:
    st.session_state.ram_warning = 70

if "disk_warning" not in st.session_state:
    st.session_state.disk_warning = 80

def go_to(page):
    st.session_state.page = page

def find_project_logo():
    preferred = [
        "serverhub_logo.png",
        "serverhub_logo.jpg",
        "serverhub_logo.jpeg",
        "logo.png",
        "logo.jpg"
    ]

    for filename in preferred:
        if Path(filename).exists():
            return filename

    return None

# =========================================================
# HELPERS
# =========================================================

def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception:
        return "Unavailable"

def get_status(value, warning, critical=90):
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "HEALTHY"

def status_message(name, value, warning, critical=90):
    status = get_status(value, warning, critical)

    if status == "CRITICAL":
        st.error(f"🔴 {name}: {value}% — CRITICAL")
    elif status == "WARNING":
        st.warning(f"🟠 {name}: {value}% — WARNING")
    else:
        st.success(f"🟢 {name}: {value}% — HEALTHY")

def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-company">SERVERHUB • SERVER HEALTH MONITORING</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-tags">
                ⚙️ CPU &nbsp;&nbsp;
                🧠 RAM &nbsp;&nbsp;
                💾 Disk &nbsp;&nbsp;
                🌐 Network &nbsp;&nbsp;
                ⚠️ Alerts
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def card(icon, title, text, color):
    st.markdown(
        f"""
        <div class="card {color}">
            <div class="card-title">{icon} {title}</div>
            <div class="card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>

/* MAIN */
.stApp {
    background:
        radial-gradient(circle at 88% 10%, rgba(59,130,246,.20), transparent 25%),
        radial-gradient(circle at 70% 80%, rgba(34,197,94,.12), transparent 30%),
        linear-gradient(135deg, #f8fbff 0%, #eef5ff 50%, #f8fafc 100%);
}

.block-container {
    padding-top: 1.3rem;
    padding-bottom: 3rem;
    max-width: 1250px;
    animation: fadeUp .55s ease;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eaf3ff 0%, #eef2ff 50%, #f8fafc 100%);
    border-right: 1px solid #dbeafe;
}

section[data-testid="stSidebar"] img {
    background: white;
    padding: 8px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(15,46,90,.10);
}

/* TITLES */
h1, h2, h3 {
    color: #102a56;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border: 0;
    border-radius: 14px;
    color: white;
    font-weight: 700;
    background: linear-gradient(90deg, #1677ff, #2563eb);
    box-shadow: 0 7px 18px rgba(37,99,235,.22);
    transition: transform .25s ease, box-shadow .25s ease;
}

.stButton > button:hover {
    color: white;
    transform: translateY(-4px);
    box-shadow: 0 13px 27px rgba(37,99,235,.32);
}

/* METRICS */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.92);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 27px rgba(30,64,175,.12);
    transition: all .25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 17px 35px rgba(37,99,235,.20);
}

div[data-testid="stAlert"] {
    border-radius: 17px;
}

/* HERO */
.hero {
    position: relative;
    overflow: hidden;
    padding: 32px 36px;
    margin-bottom: 24px;
    border-radius: 25px;
    background:
        radial-gradient(circle at 88% 25%, rgba(59,130,246,.75), transparent 27%),
        linear-gradient(115deg, #071b46 0%, #123d85 58%, #2563eb 100%);
    box-shadow: 0 16px 38px rgba(30,64,175,.25);
}

.hero::before {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    right: -65px;
    bottom: -140px;
    background: rgba(255,255,255,.11);
}

.hero::after {
    content: "";
    position: absolute;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    right: 70px;
    top: -60px;
    background: rgba(255,255,255,.08);
}

.hero-company {
    color: #bfdbfe;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero-title {
    color: white;
    font-size: 40px;
    line-height: 1.15;
    font-weight: 800;
    margin-top: 8px;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 19px;
    margin-top: 8px;
}

.hero-tags {
    color: #bfdbfe;
    font-size: 14px;
    margin-top: 22px;
}

/* CARDS */
.card {
    background: rgba(255,255,255,.84);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 20px;
    padding: 21px;
    min-height: 145px;
    margin-bottom: 15px;
    box-shadow: 0 8px 24px rgba(15,46,90,.09);
    transition: all .25s ease;
}

.card:hover {
    transform: translateY(-7px) scale(1.01);
    box-shadow: 0 16px 32px rgba(37,99,235,.17);
}

.card-blue { background: linear-gradient(135deg, #eff6ff, #dbeafe); }
.card-green { background: linear-gradient(135deg, #ecfdf5, #d1fae5); }
.card-purple { background: linear-gradient(135deg, #f5f3ff, #ede9fe); }
.card-orange { background: linear-gradient(135deg, #fff7ed, #ffedd5); }
.card-pink { background: linear-gradient(135deg, #fff1f2, #fce7f3); }
.card-cyan { background: linear-gradient(135deg, #ecfeff, #cffafe); }

.card-title {
    color: #102a56;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-text {
    color: #475569;
    font-size: 15px;
    line-height: 1.55;
}

.footer-box {
    margin-top: 25px;
    padding: 22px;
    border-radius: 20px;
    color: white;
    background: linear-gradient(100deg, #102a56, #164e9c, #2563eb);
    box-shadow: 0 10px 25px rgba(30,64,175,.18);
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

project_logo = find_project_logo()

if project_logo:
    st.sidebar.image(project_logo, width=190)
else:
    st.sidebar.markdown("## 🖥️ SERVERHub")

st.sidebar.markdown("## 🖥️ Server Console")

option = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
)

if option != st.session_state.page:
    st.session_state.page = option
    st.rerun()

st.sidebar.divider()
st.sidebar.caption(st.session_state.site_name)
st.sidebar.caption("Server Health Monitoring Project")

# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "🏠 Dashboard":

    hero(
        "🖥️ Server Health Monitoring",
        "Monitor. Analyze. Maintain."
    )

    cpu = psutil.cpu_percent(interval=0.4)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⚙️ CPU Usage", f"{cpu}%")
        status_message("CPU", cpu, st.session_state.cpu_warning)

    with c2:
        st.metric("🧠 RAM Usage", f"{ram}%")
        status_message("RAM", ram, st.session_state.ram_warning)

    with c3:
        st.metric("💾 Disk Usage", f"{disk}%")
        status_message("Disk", disk, st.session_state.disk_warning, 95)

    st.write("")
    st.markdown("## ⚡ Quick Access")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("⚙️ CPU Monitor", key="quick_cpu"):
            go_to("⚙️ CPU Monitor")
            st.rerun()

    with q2:
        if st.button("🧠 RAM Monitor", key="quick_ram"):
            go_to("🧠 RAM Monitor")
            st.rerun()

    with q3:
        if st.button("💾 Disk Monitor", key="quick_disk"):
            go_to("💾 Disk Monitor")
            st.rerun()

    with q4:
        if st.button("🌐 Network Monitor", key="quick_network"):
            go_to("🌐 Network Monitor")
            st.rerun()

    st.write("")
    st.markdown("## 🖥️ Monitoring Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        card("ℹ️", "System Info", "View operating system, hostname, processor, CPU cores and IP information.", "card-blue")
        if st.button("Open System Info →", key="card_system"):
            go_to("ℹ️ System Info")
            st.rerun()

    with c2:
        card("📋", "Processes", "View active processes and basic memory usage information.", "card-green")
        if st.button("Open Processes →", key="card_process"):
            go_to("📋 Processes")
            st.rerun()

    with c3:
        card("⚠️", "Alerts", "Review CPU, RAM and disk warning status using configurable thresholds.", "card-orange")
        if st.button("Open Alerts →", key="card_alerts"):
            go_to("⚠️ Alerts")
            st.rerun()

    c4, c5, c6 = st.columns(3)

    with c4:
        card("💻", "Operating Systems", "Show supported platforms including Windows, macOS, Linux, iOS and Android.", "card-purple")
        if st.button("Open Operating Systems →", key="card_os"):
            go_to("💻 Operating Systems")
            st.rerun()

    with c5:
        card("📄", "Reports", "Create a simple server health summary for presentation and documentation.", "card-cyan")
        if st.button("Open Reports →", key="card_report"):
            go_to("📄 Reports")
            st.rerun()

    with c6:
        card("🛠️", "Admin Control", "Change website name and health warning limits from one control page.", "card-pink")
        if st.button("Open Admin Control →", key="card_admin"):
            go_to("🛠️ Admin Control")
            st.rerun()

    st.markdown(
        """
        <div class="footer-box">
        <b>🖥️ ServerHealthMonitoring</b><br><br>
        Monitor CPU, RAM, disk, network information and system health from one dashboard.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# SYSTEM INFO
# =========================================================

elif st.session_state.page == "ℹ️ System Info":

    hero("ℹ️ System Information", "View the current server and operating system details.")

    info = {
        "Computer Name": socket.gethostname(),
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version(),
        "Processor": platform.processor() or "Unavailable",
        "CPU Cores": psutil.cpu_count(logical=True),
        "Total RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "IP Address": get_ip()
    }

    for key, value in info.items():
        st.write(f"**{key}:** {value}")

    if st.button("⬅ Back to Dashboard", key="back_system"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# CPU
# =========================================================

elif st.session_state.page == "⚙️ CPU Monitor":

    hero("⚙️ CPU Monitor", "Monitor processor utilization and CPU core information.")

    cpu = psutil.cpu_percent(interval=0.6)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("CPU Usage", f"{cpu}%")
    with c2:
        st.metric("Physical Cores", psutil.cpu_count(logical=False))
    with c3:
        st.metric("Logical Cores", psutil.cpu_count(logical=True))

    st.progress(int(cpu))
    status_message("CPU", cpu, st.session_state.cpu_warning)

    if st.button("⬅ Back to Dashboard", key="back_cpu"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# RAM
# =========================================================

elif st.session_state.page == "🧠 RAM Monitor":

    hero("🧠 RAM Monitor", "Monitor memory utilization and available RAM.")

    memory = psutil.virtual_memory()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("RAM Usage", f"{memory.percent}%")
    with c2:
        st.metric("Total RAM", f"{round(memory.total / (1024 ** 3), 2)} GB")
    with c3:
        st.metric("Available RAM", f"{round(memory.available / (1024 ** 3), 2)} GB")

    st.progress(int(memory.percent))
    status_message("RAM", memory.percent, st.session_state.ram_warning)

    if st.button("⬅ Back to Dashboard", key="back_ram"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# DISK
# =========================================================

elif st.session_state.page == "💾 Disk Monitor":

    hero("💾 Disk Monitor", "Monitor storage usage and available disk space.")

    disk = psutil.disk_usage("/")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Disk Usage", f"{disk.percent}%")
    with c2:
        st.metric("Total Disk", f"{round(disk.total / (1024 ** 3), 2)} GB")
    with c3:
        st.metric("Free Space", f"{round(disk.free / (1024 ** 3), 2)} GB")

    st.progress(int(disk.percent))
    status_message("Disk", disk.percent, st.session_state.disk_warning, 95)

    if st.button("⬅ Back to Dashboard", key="back_disk"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# NETWORK
# =========================================================

elif st.session_state.page == "🌐 Network Monitor":

    hero("🌐 Network Monitor", "View basic network and connection information.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Hostname", socket.gethostname())

    with c2:
        st.metric("IP Address", get_ip())

    with c3:
        st.metric("Status", "Connected")

    net = psutil.net_io_counters()

    st.markdown("### 📡 Network Traffic")

    n1, n2 = st.columns(2)

    with n1:
        st.metric("Data Sent", f"{round(net.bytes_sent / (1024 ** 2), 2)} MB")

    with n2:
        st.metric("Data Received", f"{round(net.bytes_recv / (1024 ** 2), 2)} MB")

    if st.button("⬅ Back to Dashboard", key="back_network"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# PROCESSES
# =========================================================

elif st.session_state.page == "📋 Processes":

    hero("📋 Running Processes", "Review active processes on the monitored system.")

    rows = []

    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            rows.append({
                "PID": process.info["pid"],
                "Process": process.info["name"],
                "Memory %": round(process.info["memory_percent"], 2)
            })

            if len(rows) >= 50:
                break

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    st.dataframe(rows, use_container_width=True)

    if st.button("⬅ Back to Dashboard", key="back_processes"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# OPERATING SYSTEMS
# =========================================================

elif st.session_state.page == "💻 Operating Systems":

    hero("💻 Operating Systems", "Supported operating system categories for the project.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card("🪟", "Windows", "Desktop and Windows Server monitoring.", "card-blue")
        card("📱", "iOS", "Mobile device operating system category.", "card-cyan")

    with c2:
        card("🍎", "macOS", "Apple desktop operating system category.", "card-purple")
        card("📱", "Android", "Android mobile and tablet category.", "card-green")

    with c3:
        card("🐧", "Linux", "Linux server and desktop monitoring.", "card-green")
        card("📱", "iPadOS", "Apple iPad operating system category.", "card-blue")

    with c4:
        card("⌚", "watchOS", "Apple Watch operating system category.", "card-orange")
        card("📺", "tvOS", "Apple TV operating system category.", "card-pink")

    st.info(f"Current host operating system: {platform.system()} {platform.release()}")

    if st.button("⬅ Back to Dashboard", key="back_os"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# ALERTS
# =========================================================

elif st.session_state.page == "⚠️ Alerts":

    hero("⚠️ System Alerts", "Review current CPU, RAM and disk health warnings.")

    cpu = psutil.cpu_percent(interval=0.4)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    status_message("CPU", cpu, st.session_state.cpu_warning)
    status_message("RAM", ram, st.session_state.ram_warning)
    status_message("Disk", disk, st.session_state.disk_warning, 95)

    if (
        cpu < st.session_state.cpu_warning
        and ram < st.session_state.ram_warning
        and disk < st.session_state.disk_warning
    ):
        st.success("✅ No active alerts. System is healthy.")

    if st.button("⬅ Back to Dashboard", key="back_alerts"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# REPORTS
# =========================================================

elif st.session_state.page == "📄 Reports":

    hero("📄 Server Health Report", "Generate a current system health summary.")

    cpu = psutil.cpu_percent(interval=0.4)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    overall = "HEALTHY"

    if cpu >= 90 or memory.percent >= 90 or disk.percent >= 95:
        overall = "CRITICAL"
    elif (
        cpu >= st.session_state.cpu_warning
        or memory.percent >= st.session_state.ram_warning
        or disk.percent >= st.session_state.disk_warning
    ):
        overall = "WARNING"

    report = f"""
SERVER HEALTH REPORT

Date & Time: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Computer Name: {socket.gethostname()}
Operating System: {platform.system()} {platform.release()}
IP Address: {get_ip()}

CPU Usage: {cpu}%
RAM Usage: {memory.percent}%
Disk Usage: {disk.percent}%

Overall Status: {overall}
"""

    st.code(report)

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("CPU", f"{cpu}%")

    with r2:
        st.metric("RAM", f"{memory.percent}%")

    with r3:
        st.metric("Disk", f"{disk.percent}%")

    if overall == "HEALTHY":
        st.success("🟢 Overall System Status: HEALTHY")
    elif overall == "WARNING":
        st.warning("🟠 Overall System Status: WARNING")
    else:
        st.error("🔴 Overall System Status: CRITICAL")

    if st.button("⬅ Back to Dashboard", key="back_reports"):
        go_to("🏠 Dashboard")
        st.rerun()

# =========================================================
# ADMIN CONTROL
# =========================================================

elif st.session_state.page == "🛠️ Admin Control":

    hero("🛠️ Admin Control", "Control the ServerHealthMonitoring dashboard settings.")

    st.markdown("### Website Settings")

    site_name = st.text_input(
        "Website Name",
        st.session_state.site_name
    )

    st.markdown("### Alert Thresholds")

    c1, c2, c3 = st.columns(3)

    with c1:
        cpu_warning = st.number_input(
            "CPU Warning %",
            min_value=1,
            max_value=100,
            value=int(st.session_state.cpu_warning)
        )

    with c2:
        ram_warning = st.number_input(
            "RAM Warning %",
            min_value=1,
            max_value=100,
            value=int(st.session_state.ram_warning)
        )

    with c3:
        disk_warning = st.number_input(
            "Disk Warning %",
            min_value=1,
            max_value=100,
            value=int(st.session_state.disk_warning)
        )

    if st.button("💾 Save Admin Settings"):
        st.session_state.site_name = site_name
        st.session_state.cpu_warning = int(cpu_warning)
        st.session_state.ram_warning = int(ram_warning)
        st.session_state.disk_warning = int(disk_warning)

        st.success("✅ Admin settings saved for this session.")

    st.info(
        "Admin Control changes the project settings while this Streamlit session is running."
    )

    if st.button("⬅ Back to Dashboard", key="back_admin"):
        go_to("🏠 Dashboard")
        st.rerun()
'''

requirements = '''streamlit
psutil
'''

readme = '''# ServerHealthMonitoring

Streamlit server health monitoring dashboard.

## Features
- Dashboard
- System Info
- CPU Monitor
- RAM Monitor
- Disk Monitor
- Network Monitor
- Processes
- Operating Systems
- Alerts
- Reports
- Admin Control

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
