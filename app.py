import streamlit as st
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


# =========================================================
# FUNCTIONS
# =========================================================

def go_to(page):
    st.session_state.page = page


def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unavailable"


def get_status(value, warning, critical=90):

    if value >= critical:
        return "CRITICAL"

    elif value >= warning:
        return "WARNING"

    else:
        return "HEALTHY"


def status_box(title, value, warning, critical=90):

    status = get_status(
        value,
        warning,
        critical
    )

    if status == "CRITICAL":

        st.error(
            f"🔴 {title}: {value}% — CRITICAL"
        )

    elif status == "WARNING":

        st.warning(
            f"🟠 {title}: {value}% — WARNING"
        )

    else:

        st.success(
            f"🟢 {title}: {value}% — HEALTHY"
        )


def hero(title, subtitle):

    html = f"""
    <div class="hero">

        <div class="hero-company">
            SERVERHub • Server Health Monitoring
        </div>

        <div class="hero-title">
            {title}
        </div>

        <div class="hero-subtitle">
            {subtitle}
        </div>

        <div class="hero-tags">

            ⚙️ CPU &nbsp;&nbsp;

            🧠 RAM &nbsp;&nbsp;

            💾 Disk &nbsp;&nbsp;

            🌐 Network &nbsp;&nbsp;

            ⚠️ Alerts

        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def card(
    icon,
    title,
    text,
    color
):

    html = f"""
    <div class="card {color}">

        <div class="card-title">
            {icon} {title}
        </div>

        <div class="card-text">
            {text}
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>

/* FIX TEXT COLORS */

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp div {
    color: #0f172a;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #102a56 !important;
}

/* Radio menu */
div[role="radiogroup"] label {
    color: #102a56 !important;
}

/* Input labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    color: #102a56 !important;
    font-weight: 600 !important;
}

/* Input text */
.stTextInput input,
.stNumberInput input {
    color: #0f172a !important;
    background: white !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: white !important;
    color: #0f172a !important;
}

/* Metric text */
div[data-testid="stMetric"] * {
    color: #102a56 !important;
}

/* Keep button text white */
.stButton > button,
.stButton > button * {
    color: white !important;
}

/* Keep hero text white */
.hero,
.hero *,
.hero-title,
.hero-company,
.hero-subtitle,
.hero-tags {
    color: white !important;
}

/* Cards */
.card-title {
    color: #102a56 !important;
}

.card-text {
    color: #475569 !important;
}

/* Alerts */
div[data-testid="stAlert"] * {
    color: #0f172a !important;
}

/* =========================================================
   MAIN BACKGROUND
========================================================= */

.stApp {

    background:

        radial-gradient(
            circle at 88% 10%,
            rgba(59,130,246,.20),
            transparent 25%
        ),

        radial-gradient(
            circle at 70% 80%,
            rgba(139,92,246,.16),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef5ff 50%,
            #faf7ff 100%
        );
}


.block-container {

    padding-top: 1.3rem;

    padding-bottom: 3rem;

    max-width: 1250px;

    animation:
        fadeUp .55s ease;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    background:

        linear-gradient(
            180deg,
            #eaf3ff 0%,
            #eef2ff 50%,
            #f5f3ff 100%
        );

    border-right:
        1px solid #dbeafe;
}


section[data-testid="stSidebar"] img {

    background: white;

    padding: 8px;

    border-radius: 18px;

    box-shadow:
        0 8px 22px
        rgba(15,46,90,.10);
}


/* =========================================================
   TITLES
========================================================= */

h1,
h2,
h3 {

    color:
        #102a56;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {

    width: 100%;

    min-height: 46px;

    border: 0;

    border-radius: 14px;

    color: white;

    font-weight: 700;

    background:

        linear-gradient(
            90deg,
            #1677ff,
            #7047eb
        );

    box-shadow:

        0 7px 18px
        rgba(37,99,235,.22);

    transition:

        transform .25s ease,

        box-shadow .25s ease;
}


.stButton > button:hover {

    color: white;

    transform:
        translateY(-4px);

    box-shadow:

        0 13px 27px
        rgba(109,74,255,.32);
}


/* =========================================================
   METRIC CARDS
========================================================= */

div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,.90);

    border:
        1px solid
        rgba(255,255,255,.95);

    border-radius:
        20px;

    padding:
        20px;

    box-shadow:

        0 10px 27px
        rgba(30,64,175,.12);

    transition:
        all .25s ease;
}


div[data-testid="stMetric"]:hover {

    transform:
        translateY(-6px);

    box-shadow:

        0 17px 35px
        rgba(37,99,235,.20);
}


/* =========================================================
   ALERTS
========================================================= */

div[data-testid="stAlert"] {

    border-radius:
        17px;
}


/* =========================================================
   INPUTS
========================================================= */

div[data-baseweb="input"] {

    border-radius:
        14px;
}


/* =========================================================
   HERO
========================================================= */

.hero {

    position:
        relative;

    overflow:
        hidden;

    padding:
        32px 36px;

    margin-bottom:
        24px;

    border-radius:
        25px;

    background:

        radial-gradient(
            circle at 88% 25%,
            rgba(59,130,246,.75),
            transparent 27%
        ),

        linear-gradient(
            115deg,
            #071b46 0%,
            #123d85 58%,
            #7047eb 100%
        );

    box-shadow:

        0 16px 38px
        rgba(30,64,175,.25);
}


.hero::before {

    content: "";

    position:
        absolute;

    width:
        230px;

    height:
        230px;

    border-radius:
        50%;

    right:
        -65px;

    bottom:
        -140px;

    background:
        rgba(255,255,255,.11);
}


.hero::after {

    content: "";

    position:
        absolute;

    width:
        120px;

    height:
        120px;

    border-radius:
        50%;

    right:
        70px;

    top:
        -60px;

    background:
        rgba(255,255,255,.08);
}


.hero-company {

    color:
        #bfdbfe;

    font-size:
        15px;

    font-weight:
        700;

    letter-spacing:
        1px;
}


.hero-title {

    color:
        white;

    font-size:
        40px;

    line-height:
        1.15;

    font-weight:
        800;

    margin-top:
        8px;
}


.hero-subtitle {

    color:
        #dbeafe;

    font-size:
        19px;

    margin-top:
        8px;
}


.hero-tags {

    color:
        #bfdbfe;

    font-size:
        14px;

    margin-top:
        22px;
}


/* =========================================================
   CARDS
========================================================= */

.card {

    background:
        rgba(255,255,255,.82);

    border:
        1px solid
        rgba(255,255,255,.95);

    border-radius:
        20px;

    padding:
        21px;

    min-height:
        145px;

    margin-bottom:
        15px;

    box-shadow:

        0 8px 24px
        rgba(15,46,90,.09);

    transition:
        all .25s ease;
}


.card:hover {

    transform:
        translateY(-7px)
        scale(1.01);

    box-shadow:

        0 16px 32px
        rgba(37,99,235,.17);
}


/* BLUE */

.card-blue {

    background:

        linear-gradient(
            135deg,
            #eff6ff,
            #dbeafe
        );
}


/* GREEN */

.card-green {

    background:

        linear-gradient(
            135deg,
            #ecfdf5,
            #d1fae5
        );
}


/* PURPLE */

.card-purple {

    background:

        linear-gradient(
            135deg,
            #f5f3ff,
            #ede9fe
        );
}


/* ORANGE */

.card-orange {

    background:

        linear-gradient(
            135deg,
            #fff7ed,
            #ffedd5
        );
}


/* PINK */

.card-pink {

    background:

        linear-gradient(
            135deg,
            #fff1f2,
            #fce7f3
        );
}


/* CYAN */

.card-cyan {

    background:

        linear-gradient(
            135deg,
            #ecfeff,
            #cffafe
        );
}


.card-title {

    color:
        #102a56;

    font-size:
        19px;

    font-weight:
        800;

    margin-bottom:
        8px;
}


.card-text {

    color:
        #475569;

    font-size:
        15px;

    line-height:
        1.55;
}


/* =========================================================
   QUICK ACCESS
========================================================= */

.quick-title {

    font-size:
        18px;

    font-weight:
        800;

    color:
        #102a56;

    margin-top:
        5px;

    margin-bottom:
        12px;
}


/* =========================================================
   FOOTER
========================================================= */

.footer-box {

    margin-top:
        25px;

    padding:
        22px;

    border-radius:
        20px;

    color:
        white;

    background:

        linear-gradient(
            100deg,
            #102a56,
            #164e9c,
            #6339d7
        );

    box-shadow:

        0 10px 25px
        rgba(30,64,175,.18);
}


/* =========================================================
   ANIMATION
========================================================= */

@keyframes fadeUp {

    from {

        opacity:
            0;

        transform:
            translateY(14px);
    }

    to {

        opacity:
            1;

        transform:
            translateY(0);
    }
}

</style>
""",
unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

# ---------------------------------------------------------
# PROJECT LOGO - TOP
# ---------------------------------------------------------

if Path("sever hub.png").exists():

    st.sidebar.image(
        "sever hub.png",
        width=190
    )

else:

    st.sidebar.markdown(
        "## 🖥️ SERVERHub"
    )


st.sidebar.markdown(
    "## 🖥️ Server Console"
)


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

option = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(
        st.session_state.page
    )
)


if option != st.session_state.page:

    st.session_state.page = option

    st.rerun()


# ---------------------------------------------------------
# COMPANY LOGO - BOTTOM
# ---------------------------------------------------------

st.sidebar.divider()


if Path("intertec.jpg").exists():

    st.sidebar.image(
        "intertec.jpg",
        width=150
    )


st.sidebar.caption(
    "INTERTEC SYSTEMS LLC"
)


st.sidebar.caption(
    "Server Health Monitoring Project"
)


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "🏠 Dashboard":

    hero(
        "🖥️ Server Health Monitoring",
        "Monitor. Analyze. Maintain."
    )


    cpu = psutil.cpu_percent(
        interval=0.4
    )


    ram = (
        psutil
        .virtual_memory()
        .percent
    )


    disk = (
        psutil
        .disk_usage("/")
        .percent
    )


    # -----------------------------------------------------
    # QUICK ACCESS
    # -----------------------------------------------------

    st.markdown(
        '<div class="quick-title">'
        '⚡ Quick Access'
        '</div>',
        unsafe_allow_html=True
    )


    q1, q2, q3, q4 = (
        st.columns(4)
    )


    with q1:

        st.metric(
            "⚙️ CPU Monitor",
            f"{cpu}%",
            "Live"
        )


        if st.button(
            "⚙️ Open CPU",
            key="quick_cpu"
        ):

            go_to(
                "⚙️ CPU Monitor"
            )

            st.rerun()


    with q2:

        st.metric(
            "🧠 RAM Monitor",
            f"{ram}%",
            "Live"
        )


        if st.button(
            "🧠 Open RAM",
            key="quick_ram"
        ):

            go_to(
                "🧠 RAM Monitor"
            )

            st.rerun()


    with q3:

        st.metric(
            "💾 Disk Monitor",
            f"{disk}%",
            "Live"
        )


        if st.button(
            "💾 Open Disk",
            key="quick_disk"
        ):

            go_to(
                "💾 Disk Monitor"
            )

            st.rerun()


    with q4:

        st.metric(
            "🌐 Network",
            "Connected",
            "Online"
        )


        if st.button(
            "🌐 Open Network",
            key="quick_network"
        ):

            go_to(
                "🌐 Network Monitor"
            )

            st.rerun()


    st.write("")


    # -----------------------------------------------------
    # MONITORING FEATURES
    # -----------------------------------------------------

    st.markdown(
        "## 🖥️ Monitoring Features"
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        card(
            "ℹ️",
            "System Information",
            "View computer name, operating system, processor, CPU cores, RAM and IP address.",
            "card-blue"
        )


        if st.button(
            "Open System Info →",
            key="card_system"
        ):

            go_to(
                "ℹ️ System Info"
            )

            st.rerun()


    with c2:

        card(
            "📋",
            "Processes",
            "Review active processes and basic memory usage information.",
            "card-green"
        )


        if st.button(
            "Open Processes →",
            key="card_processes"
        ):

            go_to(
                "📋 Processes"
            )

            st.rerun()


    with c3:

        card(
            "⚠️",
            "Alerts",
            "Review CPU, RAM and disk health warnings.",
            "card-orange"
        )


        if st.button(
            "Open Alerts →",
            key="card_alerts"
        ):

            go_to(
                "⚠️ Alerts"
            )

            st.rerun()


    c4, c5, c6 = (
        st.columns(3)
    )


    with c4:

        card(
            "💻",
            "Operating Systems",
            "Windows, macOS, Linux, Android, iOS, iPadOS, watchOS and tvOS.",
            "card-purple"
        )


        if st.button(
            "Open Operating Systems →",
            key="card_os"
        ):

            go_to(
                "💻 Operating Systems"
            )

            st.rerun()


    with c5:

        card(
            "📄",
            "Reports",
            "Generate a simple current server health report.",
            "card-cyan"
        )


        if st.button(
            "Open Reports →",
            key="card_reports"
        ):

            go_to(
                "📄 Reports"
            )

            st.rerun()


    with c6:

        card(
            "🛠️",
            "Admin Control",
            "Control website name and system warning thresholds.",
            "card-pink"
        )


        if st.button(
            "Open Admin Control →",
            key="card_admin"
        ):

            go_to(
                "🛠️ Admin Control"
            )

            st.rerun()


    st.markdown(
        """
        <div class="footer-box">

        <b>🖥️ SERVERHub</b>

        <br><br>

        Smart Server Health & Performance Monitoring

        <br><br>

        Monitor • Analyze • Maintain

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SYSTEM INFO
# =========================================================

elif st.session_state.page == "ℹ️ System Info":

    hero(
        "ℹ️ System Information",
        "View the current device and operating system information."
    )


    c1, c2 = st.columns(2)


    with c1:

        card(
            "🖥️",
            "Computer",
            socket.gethostname(),
            "card-blue"
        )


        card(
            "💻",
            "Operating System",
            f"{platform.system()} {platform.release()}",
            "card-purple"
        )


        card(
            "🌐",
            "IP Address",
            get_ip(),
            "card-cyan"
        )


    with c2:

        card(
            "⚙️",
            "Processor",
            platform.processor()
            or
            "Unavailable",
            "card-green"
        )


        card(
            "🔢",
            "CPU Cores",
            str(
                psutil.cpu_count(
                    logical=True
                )
            ),
            "card-orange"
        )


        card(
            "🧠",
            "Total RAM",
            f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
            "card-pink"
        )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_system"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# CPU
# =========================================================

elif st.session_state.page == "⚙️ CPU Monitor":

    hero(
        "⚙️ CPU Monitor",
        "Monitor processor usage and CPU core information."
    )


    cpu = psutil.cpu_percent(
        interval=0.5
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        st.metric(
            "⚙️ CPU Usage",
            f"{cpu}%"
        )


    with c2:

        st.metric(
            "Physical Cores",
            psutil.cpu_count(
                logical=False
            )
        )


    with c3:

        st.metric(
            "Logical Cores",
            psutil.cpu_count(
                logical=True
            )
        )


    st.progress(
        int(cpu)
    )


    status_box(
        "CPU",
        cpu,
        st.session_state.cpu_warning
    )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_cpu"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# RAM
# =========================================================

elif st.session_state.page == "🧠 RAM Monitor":

    hero(
        "🧠 RAM Monitor",
        "Monitor memory usage and available RAM."
    )


    memory = (
        psutil
        .virtual_memory()
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        st.metric(
            "🧠 RAM Usage",
            f"{memory.percent}%"
        )


    with c2:

        st.metric(
            "Total RAM",
            f"{round(memory.total / (1024 ** 3), 2)} GB"
        )


    with c3:

        st.metric(
            "Available RAM",
            f"{round(memory.available / (1024 ** 3), 2)} GB"
        )


    st.progress(
        int(memory.percent)
    )


    status_box(
        "RAM",
        memory.percent,
        st.session_state.ram_warning
    )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_ram"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# DISK
# =========================================================

elif st.session_state.page == "💾 Disk Monitor":

    hero(
        "💾 Disk Monitor",
        "Monitor storage usage and available disk space."
    )


    disk = psutil.disk_usage(
        "/"
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        st.metric(
            "💾 Disk Usage",
            f"{disk.percent}%"
        )


    with c2:

        st.metric(
            "Total Disk",
            f"{round(disk.total / (1024 ** 3), 2)} GB"
        )


    with c3:

        st.metric(
            "Free Space",
            f"{round(disk.free / (1024 ** 3), 2)} GB"
        )


    st.progress(
        int(disk.percent)
    )


    status_box(
        "Disk",
        disk.percent,
        st.session_state.disk_warning,
        95
    )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_disk"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# NETWORK
# =========================================================

elif st.session_state.page == "🌐 Network Monitor":

    hero(
        "🌐 Network Monitor",
        "View network and connection information."
    )


    net = (
        psutil
        .net_io_counters()
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        st.metric(
            "Computer",
            socket.gethostname()
        )


    with c2:

        st.metric(
            "IP Address",
            get_ip()
        )


    with c3:

        st.metric(
            "Status",
            "Connected"
        )


    st.markdown(
        "### 📡 Network Traffic"
    )


    n1, n2 = (
        st.columns(2)
    )


    with n1:

        st.metric(
            "Data Sent",
            f"{round(net.bytes_sent / (1024 ** 2), 2)} MB"
        )


    with n2:

        st.metric(
            "Data Received",
            f"{round(net.bytes_recv / (1024 ** 2), 2)} MB"
        )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_network"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# PROCESSES
# =========================================================

elif st.session_state.page == "📋 Processes":

    hero(
        "📋 Running Processes",
        "Review active processes on the monitored device."
    )


    processes = []


    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "memory_percent"
        ]
    ):

        try:

            processes.append(
                {
                    "PID":
                    process.info[
                        "pid"
                    ],

                    "Process":
                    process.info[
                        "name"
                    ],

                    "Memory %":
                    round(
                        process.info[
                            "memory_percent"
                        ],
                        2
                    )
                }
            )


            if len(processes) >= 50:

                break


        except:

            pass


    st.dataframe(
        processes,
        use_container_width=True
    )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_processes"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# OPERATING SYSTEMS
# =========================================================

elif st.session_state.page == "💻 Operating Systems":

    hero(
        "💻 Operating Systems",
        "Supported operating system categories."
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        card(
            "🪟",
            "Windows",
            "Windows desktop and server monitoring.",
            "card-blue"
        )


        card(
            "📱",
            "iOS",
            "Apple mobile operating system.",
            "card-cyan"
        )


    with c2:

        card(
            "🍎",
            "macOS",
            "Apple desktop operating system.",
            "card-purple"
        )


        card(
            "🤖",
            "Android",
            "Android phones and tablets.",
            "card-green"
        )


    with c3:

        card(
            "🐧",
            "Linux",
            "Linux desktop and server monitoring.",
            "card-green"
        )


        card(
            "📱",
            "iPadOS",
            "Apple iPad operating system.",
            "card-blue"
        )


    with c4:

        card(
            "⌚",
            "watchOS",
            "Apple Watch operating system.",
            "card-orange"
        )


        card(
            "📺",
            "tvOS",
            "Apple TV operating system.",
            "card-pink"
        )


    st.info(
        f"Current Operating System: "
        f"{platform.system()} "
        f"{platform.release()}"
    )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_os"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# ALERTS
# =========================================================

elif st.session_state.page == "⚠️ Alerts":

    hero(
        "⚠️ System Alerts",
        "Review CPU, RAM and disk health warnings."
    )


    cpu = psutil.cpu_percent(
        interval=0.4
    )


    ram = (
        psutil
        .virtual_memory()
        .percent
    )


    disk = (
        psutil
        .disk_usage("/")
        .percent
    )


    status_box(
        "CPU",
        cpu,
        st.session_state.cpu_warning
    )


    status_box(
        "RAM",
        ram,
        st.session_state.ram_warning
    )


    status_box(
        "Disk",
        disk,
        st.session_state.disk_warning,
        95
    )


    if (
        cpu
        <
        st.session_state.cpu_warning
        and
        ram
        <
        st.session_state.ram_warning
        and
        disk
        <
        st.session_state.disk_warning
    ):

        st.success(
            "✅ No active alerts. "
            "System is healthy."
        )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_alerts"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# REPORTS
# =========================================================

elif st.session_state.page == "📄 Reports":

    hero(
        "📄 Server Health Report",
        "Current server health summary."
    )


    cpu = psutil.cpu_percent(
        interval=0.4
    )


    memory = (
        psutil
        .virtual_memory()
    )


    disk = psutil.disk_usage(
        "/"
    )


    overall_status = "HEALTHY"


    if (
        cpu >= 90
        or
        memory.percent >= 90
        or
        disk.percent >= 95
    ):

        overall_status = (
            "CRITICAL"
        )


    elif (
        cpu
        >=
        st.session_state.cpu_warning

        or

        memory.percent
        >=
        st.session_state.ram_warning

        or

        disk.percent
        >=
        st.session_state.disk_warning
    ):

        overall_status = (
            "WARNING"
        )


    report = f"""
SERVER HEALTH REPORT

Date & Time:
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Computer Name:
{socket.gethostname()}

Operating System:
{platform.system()} {platform.release()}

IP Address:
{get_ip()}

CPU Usage:
{cpu}%

RAM Usage:
{memory.percent}%

Disk Usage:
{disk.percent}%

Overall Status:
{overall_status}
"""


    st.code(
        report
    )


    r1, r2, r3 = (
        st.columns(3)
    )


    with r1:

        st.metric(
            "CPU",
            f"{cpu}%"
        )


    with r2:

        st.metric(
            "RAM",
            f"{memory.percent}%"
        )


    with r3:

        st.metric(
            "Disk",
            f"{disk.percent}%"
        )


    if overall_status == "HEALTHY":

        st.success(
            "🟢 Overall System Status: HEALTHY"
        )


    elif overall_status == "WARNING":

        st.warning(
            "🟠 Overall System Status: WARNING"
        )


    else:

        st.error(
            "🔴 Overall System Status: CRITICAL"
        )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_reports"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()


# =========================================================
# ADMIN CONTROL
# =========================================================

elif st.session_state.page == "🛠️ Admin Control":

    hero(
        "🛠️ Admin Control",
        "Control your ServerHealthMonitoring settings."
    )


    c1, c2 = (
        st.columns(2)
    )


    with c1:

        st.markdown(
            "### 🌐 Website Settings"
        )


        site_name = st.text_input(
            "Website Name",
            st.session_state.site_name
        )


        st.info(
            "Current Project: "
            "SERVERHub Server Health Monitoring"
        )


    with c2:

        st.markdown(
            "### ⚠️ Alert Settings"
        )


        cpu_warning = st.number_input(
            "CPU Warning %",
            min_value=1,
            max_value=100,
            value=int(
                st.session_state.cpu_warning
            )
        )


        ram_warning = st.number_input(
            "RAM Warning %",
            min_value=1,
            max_value=100,
            value=int(
                st.session_state.ram_warning
            )
        )


        disk_warning = st.number_input(
            "Disk Warning %",
            min_value=1,
            max_value=100,
            value=int(
                st.session_state.disk_warning
            )
        )


    if st.button(
        "💾 Save Changes"
    ):

        st.session_state.site_name = (
            site_name
        )


        st.session_state.cpu_warning = (
            int(cpu_warning)
        )


        st.session_state.ram_warning = (
            int(ram_warning)
        )


        st.session_state.disk_warning = (
            int(disk_warning)
        )


        st.success(
            "✅ Settings saved successfully."
        )


    st.markdown(
        "### 🖥️ Current Settings"
    )


    a1, a2, a3 = (
        st.columns(3)
    )


    with a1:

        st.metric(
            "CPU Warning",
            f"{st.session_state.cpu_warning}%"
        )


    with a2:

        st.metric(
            "RAM Warning",
            f"{st.session_state.ram_warning}%"
        )


    with a3:

        st.metric(
            "Disk Warning",
            f"{st.session_state.disk_warning}%"
        )


    if st.button(
        "⬅ Back to Dashboard",
        key="back_admin"
    ):

        go_to(
            "🏠 Dashboard"
        )

        st.rerun()
