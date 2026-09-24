import customtkinter as ctk
import psutil
import platform
import socket
import os
from datetime import datetime
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ServerHealthMonitor2")
app.geometry("1200x750")

BG = "#0f172a"
SIDEBAR = "#111827"
CARD = "#1e293b"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
GREEN = "#22c55e"
ORANGE = "#f59e0b"
RED = "#ef4444"

app.configure(fg_color=BG)

def clear_main():
    for widget in main_frame.winfo_children():
        widget.destroy()

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unavailable"

def get_status(value):
    if value >= 90:
        return "CRITICAL", RED
    elif value >= 70:
        return "WARNING", ORANGE
    else:
        return "HEALTHY", GREEN

def make_card(parent, title, value, color=TEXT):
    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=15)
    card.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(
        card,
        text=title,
        font=("Segoe UI", 16, "bold"),
        text_color=MUTED
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        card,
        text=value,
        font=("Segoe UI", 25, "bold"),
        text_color=color
    ).pack(pady=(5, 20))

def show_dashboard():
    clear_main()

    ctk.CTkLabel(
        main_frame,
        text="Dashboard",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(anchor="w", padx=30, pady=(25, 10))

    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage(os.path.abspath(os.sep)).percent

    cpu_status, cpu_color = get_status(cpu)
    ram_status, ram_color = get_status(ram)
    disk_status, disk_color = get_status(disk)

    row1 = ctk.CTkFrame(main_frame, fg_color="transparent")
    row1.pack(fill="x", padx=20)

    make_card(row1, "CPU Usage", f"{cpu}%\n{cpu_status}", cpu_color)
    make_card(row1, "RAM Usage", f"{ram}%\n{ram_status}", ram_color)
    make_card(row1, "Disk Usage", f"{disk}%\n{disk_status}", disk_color)

    row2 = ctk.CTkFrame(main_frame, fg_color="transparent")
    row2.pack(fill="x", padx=20)

    make_card(row2, "Operating System", platform.system())
    make_card(row2, "Computer Name", socket.gethostname())
    make_card(row2, "IP Address", get_ip())

def show_system_info():
    clear_main()

    ctk.CTkLabel(
        main_frame,
        text="System Information",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(anchor="w", padx=30, pady=25)

    info = [
        ("Computer Name", socket.gethostname()),
        ("Operating System", platform.system()),
        ("OS Version", platform.version()),
        ("CPU Cores", psutil.cpu_count()),
        ("RAM", f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"),
        ("IP Address", get_ip())
    ]

    for name, value in info:
        box = ctk.CTkFrame(main_frame, fg_color=CARD, corner_radius=12)
        box.pack(fill="x", padx=30, pady=6)

        ctk.CTkLabel(
            box,
            text=f"{name}:",
            width=180,
            anchor="w",
            font=("Segoe UI", 15, "bold"),
            text_color=MUTED
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(
            box,
            text=str(value),
            font=("Segoe UI", 15),
            text_color=TEXT
        ).pack(side="left", padx=10)

def show_cpu():
    clear_main()
    cpu = psutil.cpu_percent(interval=0.5)
    status, color = get_status(cpu)

    ctk.CTkLabel(
        main_frame,
        text="CPU Monitor",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=30)

    make_card(main_frame, "CPU Usage", f"{cpu}% - {status}", color)

def show_ram():
    clear_main()
    ram = psutil.virtual_memory()
    status, color = get_status(ram.percent)

    ctk.CTkLabel(
        main_frame,
        text="RAM Monitor",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=30)

    make_card(main_frame, "RAM Usage", f"{ram.percent}% - {status}", color)

def show_disk():
    clear_main()
    disk = psutil.disk_usage(os.path.abspath(os.sep))
    status, color = get_status(disk.percent)

    ctk.CTkLabel(
        main_frame,
        text="Disk Monitor",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=30)

    make_card(main_frame, "Disk Usage", f"{disk.percent}% - {status}", color)

def show_network():
    clear_main()

    ctk.CTkLabel(
        main_frame,
        text="Network Monitor",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=30)

    make_card(main_frame, "IP Address", get_ip())

def show_processes():
    clear_main()

    ctk.CTkLabel(
        main_frame,
        text="Processes",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=20)

    box = ctk.CTkTextbox(main_frame)
    box.pack(fill="both", expand=True, padx=30, pady=20)

    count = 0
    for process in psutil.process_iter(["pid", "name"]):
        try:
            box.insert("end", f"{process.info['pid']}   {process.info['name']}\n")
            count += 1
            if count >= 50:
                break
        except:
            pass

def show_os():
    clear_main()

    ctk.CTkLabel(
        main_frame,
        text="Operating Systems",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=25)

    systems = [
        "Windows",
        "macOS",
        "Linux",
        "iOS",
        "Android",
        "iPadOS",
        "watchOS",
        "tvOS"
    ]

    for system in systems:
        ctk.CTkButton(
            main_frame,
            text=system,
            width=220,
            height=45
        ).pack(pady=6)

def show_alerts():
    clear_main()

    cpu = psutil.cpu_percent(interval=0.4)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage(os.path.abspath(os.sep)).percent

    alerts = []

    if cpu >= 70:
        alerts.append(f"High CPU usage: {cpu}%")
    if ram >= 70:
        alerts.append(f"High RAM usage: {ram}%")
    if disk >= 80:
        alerts.append(f"High Disk usage: {disk}%")

    if not alerts:
        alerts.append("No alerts. System is healthy.")

    ctk.CTkLabel(
        main_frame,
        text="Alerts",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=25)

    for alert in alerts:
        ctk.CTkLabel(
            main_frame,
            text=alert,
            font=("Segoe UI", 18),
            text_color=GREEN if "No alerts" in alert else ORANGE
        ).pack(pady=10)

def show_reports():
    clear_main()

    report = f"""
ServerHealthMonitor2 Report

Date:
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Operating System:
{platform.system()}

Computer Name:
{socket.gethostname()}

CPU:
{psutil.cpu_percent()}%

RAM:
{psutil.virtual_memory().percent}%

Disk:
{psutil.disk_usage(os.path.abspath(os.sep)).percent}%

IP:
{get_ip()}
"""

    ctk.CTkLabel(
        main_frame,
        text="Reports",
        font=("Segoe UI", 30, "bold"),
        text_color=TEXT
    ).pack(pady=20)

    box = ctk.CTkTextbox(main_frame)
    box.pack(fill="both", expand=True, padx=30, pady=20)
    box.insert("1.0", report)

# HEADER
header = ctk.CTkFrame(
    app,
    height=90,
    fg_color="white",
    corner_radius=0
)
header.pack(fill="x")
header.pack_propagate(False)

try:
    logo_image = ctk.CTkImage(
        light_image=Image.open("logo.png"),
        dark_image=Image.open("logo.png"),
        size=(240, 75)
    )

    logo_label = ctk.CTkLabel(
        header,
        image=logo_image,
        text=""
    )
    logo_label.pack(side="left", padx=15, pady=5)

except:
    ctk.CTkLabel(
        header,
        text="SERVERHub",
        font=("Segoe UI", 28, "bold"),
        text_color="#0b2a6b"
    ).pack(side="left", padx=25)

ctk.CTkLabel(
    header,
    text="ServerHealthMonitor2",
    font=("Segoe UI", 24, "bold"),
    text_color="#0f172a"
).pack(side="left", padx=15)

# BODY
body = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
body.pack(fill="both", expand=True)

sidebar = ctk.CTkFrame(
    body,
    width=230,
    fg_color=SIDEBAR,
    corner_radius=0
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main_frame = ctk.CTkFrame(
    body,
    fg_color=BG,
    corner_radius=0
)
main_frame.pack(side="left", fill="both", expand=True)

menu = [
    ("Dashboard", show_dashboard),
    ("System Info", show_system_info),
    ("CPU Monitor", show_cpu),
    ("RAM Monitor", show_ram),
    ("Disk Monitor", show_disk),
    ("Network Monitor", show_network),
    ("Processes", show_processes),
    ("Operating Systems", show_os),
    ("Alerts", show_alerts),
    ("Reports", show_reports)
]

for name, command in menu:
    ctk.CTkButton(
        sidebar,
        text=name,
        command=command,
        width=190,
        height=42,
        anchor="w"
    ).pack(padx=20, pady=6)

show_dashboard()

app.mainloop()

from flask import Flask, render_template, jsonify, request
import psutil
import platform
import socket

app = Flask(__name__)

settings = {
    "website_name": "ServerHealthMonitor2",
    "main_color": "blue",
    "theme": "dark",
    "refresh_time": 5,
    "cpu_limit": 70,
    "ram_limit": 70,
    "disk_limit": 80,
    "show_dashboard": True,
    "show_cpu": True,
    "show_ram": True,
    "show_disk": True,
    "show_network": True,
    "show_alerts": True,
    "show_reports": True
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/api/system")
def system_data():
    return jsonify({
        "cpu": psutil.cpu_percent(interval=0.5),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "os": platform.system(),
        "computer": socket.gethostname()
    })


@app.route("/api/settings", methods=["GET", "POST"])
def website_settings():
    global settings

    if request.method == "POST":
        new_settings = request.get_json()

        settings.update(new_settings)

        return jsonify({
            "success": True,
            "message": "Settings saved successfully"
        })

    return jsonify(settings)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ServerHealthMonitor2</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

<div class="layout">

    <aside class="sidebar">

        <div class="logo-area">
            <img src="/static/logo.png" alt="logo">
        </div>

        <h3>SERVER MONITOR</h3>

        <a href="#" onclick="showPage('dashboard')">Dashboard</a>
        <a href="#" onclick="showPage('system')">System Info</a>
        <a href="#" onclick="showPage('cpu')">CPU Monitor</a>
        <a href="#" onclick="showPage('ram')">RAM Monitor</a>
        <a href="#" onclick="showPage('disk')">Disk Monitor</a>
        <a href="#" onclick="showPage('network')">Network</a>
        <a href="#" onclick="showPage('os')">Operating Systems</a>
        <a href="#" onclick="showPage('alerts')">Alerts</a>
        <a href="/admin">Admin Control</a>

    </aside>


    <div class="main">

        <header class="topbar">

            <div>
                <h1>ServerHealthMonitor2</h1>
                <p>Smart Server Health & Performance Monitoring</p>
            </div>

            <button onclick="loadData()">Refresh</button>

        </header>


        <section id="dashboard" class="page active">

            <div class="welcome">
                <h2>System Dashboard</h2>
                <p>Monitor your server performance in real time</p>
            </div>

            <div class="cards">

                <div class="card">
                    <span>CPU Usage</span>
                    <h2 id="cpu">0%</h2>
                    <div class="progress">
                        <div id="cpu-bar"></div>
                    </div>
                </div>

                <div class="card">
                    <span>RAM Usage</span>
                    <h2 id="ram">0%</h2>
                    <div class="progress">
                        <div id="ram-bar"></div>
                    </div>
                </div>

                <div class="card">
                    <span>Disk Usage</span>
                    <h2 id="disk">0%</h2>
                    <div class="progress">
                        <div id="disk-bar"></div>
                    </div>
                </div>

            </div>


            <div class="details">

                <div class="detail-card">
                    <h3>Operating System</h3>
                    <p id="os-name">Loading...</p>
                </div>

                <div class="detail-card">
                    <h3>Computer Name</h3>
                    <p id="computer-name">Loading...</p>
                </div>

                <div class="detail-card">
                    <h3>System Status</h3>
                    <p id="status" class="healthy">HEALTHY</p>
                </div>

            </div>

        </section>


        <section id="system" class="page">
            <h2>System Information</h2>

            <div class="info-panel">
                <p><strong>Computer:</strong> <span id="sys-computer"></span></p>
                <p><strong>Operating System:</strong> <span id="sys-os"></span></p>
            </div>
        </section>


        <section id="cpu" class="page">
            <h2>CPU Monitor</h2>
            <div class="big-monitor">
                <h1 id="cpu-large">0%</h1>
                <p>Current CPU Usage</p>
            </div>
        </section>


        <section id="ram" class="page">
            <h2>RAM Monitor</h2>
            <div class="big-monitor">
                <h1 id="ram-large">0%</h1>
                <p>Current RAM Usage</p>
            </div>
        </section>


        <section id="disk" class="page">
            <h2>Disk Monitor</h2>
            <div class="big-monitor">
                <h1 id="disk-large">0%</h1>
                <p>Current Disk Usage</p>
            </div>
        </section>


        <section id="network" class="page">
            <h2>Network Monitor</h2>
            <div class="info-panel">
                <p>Network Status: Connected</p>
            </div>
        </section>


        <section id="os" class="page">
            <h2>Operating Systems</h2>

            <div class="os-grid">
                <div>Windows</div>
                <div>macOS</div>
                <div>Linux</div>
                <div>Android</div>
                <div>iOS</div>
                <div>iPadOS</div>
                <div>watchOS</div>
                <div>tvOS</div>
            </div>
        </section>


        <section id="alerts" class="page">
            <h2>Alerts</h2>
            <div class="info-panel">
                <p id="alert-text">No active alerts</p>
            </div>
        </section>

    </div>

</div>


<script>

function showPage(id) {
    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });

    document.getElementById(id).classList.add("active");
}


async function loadData() {

    const response = await fetch("/api/system");
    const data = await response.json();

    document.getElementById("cpu").innerText = data.cpu + "%";
    document.getElementById("ram").innerText = data.ram + "%";
    document.getElementById("disk").innerText = data.disk + "%";

    document.getElementById("cpu-large").innerText = data.cpu + "%";
    document.getElementById("ram-large").innerText = data.ram + "%";
    document.getElementById("disk-large").innerText = data.disk + "%";

    document.getElementById("os-name").innerText = data.os;
    document.getElementById("computer-name").innerText = data.computer;

    document.getElementById("sys-computer").innerText = data.computer;
    document.getElementById("sys-os").innerText = data.os;

    document.getElementById("cpu-bar").style.width = data.cpu + "%";
    document.getElementById("ram-bar").style.width = data.ram + "%";
    document.getElementById("disk-bar").style.width = data.disk + "%";

    let status = "HEALTHY";

    if (data.cpu > 85 || data.ram > 85 || data.disk > 90) {
        status = "WARNING";
    }

    document.getElementById("status").innerText = status;

    document.getElementById("alert-text").innerText =
        status === "HEALTHY"
        ? "No active alerts"
        : "System resource usage is high";
}

loadSettings();
loadData();
setInterval(loadSettings, 3000);

setInterval(loadData, 5000);

</script>

</body>
</html>

async function loadSettings() {

    const response = await fetch("/api/settings");
    const settings = await response.json();

    document.title = settings.website_name;

    const title = document.querySelector(".topbar h1");

    if (title) {
        title.innerText = settings.website_name;
    }

    const sidebarLinks = document.querySelectorAll(".sidebar a");

    sidebarLinks.forEach(link => {

        const text = link.innerText.trim();

        if (text === "Dashboard") {
            link.style.display = settings.show_dashboard ? "block" : "none";
        }

        if (text === "CPU Monitor") {
            link.style.display = settings.show_cpu ? "block" : "none";
        }

        if (text === "RAM Monitor") {
            link.style.display = settings.show_ram ? "block" : "none";
        }

        if (text === "Disk Monitor") {
            link.style.display = settings.show_disk ? "block" : "none";
        }

        if (text === "Network") {
            link.style.display = settings.show_network ? "block" : "none";
        }

        if (text === "Alerts") {
            link.style.display = settings.show_alerts ? "block" : "none";
        }

    });

    document.body.classList.remove(
        "theme-dark",
        "theme-light",
        "color-blue",
        "color-green",
        "color-purple"
    );

    document.body.classList.add(
        "theme-" + settings.theme,
        "color-" + settings.main_color
    );
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #0f172a;
    color: white;
}

.layout {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 240px;
    background: #111827;
    padding: 25px 15px;
}

.logo-area {
    text-align: center;
    margin-bottom: 20px;
}

.logo-area img {
    width: 150px;
    max-height: 70px;
    object-fit: contain;
}

.sidebar h3 {
    color: #94a3b8;
    font-size: 12px;
    margin-bottom: 15px;
}

.sidebar a {
    display: block;
    text-decoration: none;
    color: white;
    padding: 13px 15px;
    margin-bottom: 8px;
    border-radius: 10px;
    background: #1e293b;
}

.sidebar a:hover {
    background: #2563eb;
}

.main {
    flex: 1;
}

.topbar {
    background: white;
    color: #0f172a;
    padding: 20px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.topbar h1 {
    font-size: 24px;
}

.topbar p {
    color: #64748b;
    font-size: 13px;
}

.topbar button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
}

.page {
    display: none;
    padding: 30px;
}

.page.active {
    display: block;
}

.welcome {
    margin-bottom: 25px;
}

.welcome p {
    color: #94a3b8;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 16px;
}

.card span {
    color: #94a3b8;
}

.card h2 {
    font-size: 36px;
    margin: 12px 0;
}

.progress {
    width: 100%;
    height: 10px;
    background: #334155;
    border-radius: 10px;
    overflow: hidden;
}

.progress div {
    height: 100%;
    background: #3b82f6;
    width: 0%;
}

.details {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 20px;
}

.detail-card,
.info-panel,
.big-monitor {
    background: #1e293b;
    padding: 25px;
    border-radius: 16px;
}

.healthy {
    color: #22c55e;
    font-weight: bold;
}

.big-monitor {
    margin-top: 20px;
    text-align: center;
}

.big-monitor h1 {
    font-size: 70px;
    color: #3b82f6;
}

.os-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-top: 20px;
}

.os-grid div {
    background: #1e293b;
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    font-weight: bold;
}

/* PHONE */
@media (max-width: 700px) {

    .layout {
        display: block;
    }

    .sidebar {
        width: 100%;
    }

    .sidebar a {
        display: inline-block;
        width: 48%;
        margin: 1%;
        text-align: center;
    }

    .topbar {
        flex-direction: column;
        gap: 10px;
        align-items: flex-start;
    }

    .cards,
    .details {
        grid-template-columns: 1fr;
    }

    .os-grid {
        grid-template-columns: 1fr 1fr;
    }

    .page {
        padding: 15px;
    }
}

.theme-light {
    background: #f1f5f9;
    color: #0f172a;
}

.theme-light .sidebar {
    background: #e2e8f0;
}

.theme-light .sidebar a {
    background: white;
    color: #0f172a;
}

.theme-light .card,
.theme-light .detail-card,
.theme-light .info-panel,
.theme-light .big-monitor {
    background: white;
    color: #0f172a;
}

.color-blue .sidebar a:hover,
.color-blue .topbar button {
    background: #2563eb;
}

.color-green .sidebar a:hover,
.color-green .topbar button {
    background: #16a34a;
}

.color-purple .sidebar a:hover,
.color-purple .topbar button {
    background: #7c3aed;
}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Control Panel</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

<div class="admin-container">

    <h1>SERVERHub Admin Control Panel</h1>

    <div class="admin-card">

        <label>Website Name</label>
        <input type="text" id="websiteName" value="ServerHealthMonitor2">

        <label>Main Color</label>
        <select id="mainColor">
            <option value="blue">Blue</option>
            <option value="green">Green</option>
            <option value="purple">Purple</option>
        </select>

        <label>Theme</label>
        <select id="theme">
            <option value="dark">Dark</option>
            <option value="light">Light</option>
        </select>

        <label>Refresh Time</label>
        <select id="refreshTime">
            <option value="3">3 seconds</option>
            <option value="5" selected>5 seconds</option>
            <option value="10">10 seconds</option>
        </select>

        <label>CPU Warning Limit</label>
        <input type="number" id="cpuLimit" value="70">

        <label>RAM Warning Limit</label>
        <input type="number" id="ramLimit" value="70">

        <label>Disk Warning Limit</label>
        <input type="number" id="diskLimit" value="80">

        <h3>Show / Hide Features</h3>

        <label>
            <input type="checkbox" id="showDashboard" checked>
            Dashboard
        </label>

        <label>
            <input type="checkbox" id="showCPU" checked>
            CPU Monitor
        </label>

        <label>
            <input type="checkbox" id="showRAM" checked>
            RAM Monitor
        </label>

        <label>
            <input type="checkbox" id="showDisk" checked>
            Disk Monitor
        </label>

        <label>
            <input type="checkbox" id="showNetwork" checked>
            Network Monitor
        </label>

        <label>
            <input type="checkbox" id="showAlerts" checked>
            Alerts
        </label>

        <label>
            <input type="checkbox" id="showReports" checked>
            Reports
        </label>

        <button onclick="saveSettings()">Save Changes</button>

        <p id="saveMessage"></p>

    </div>

</div>

<script>

async function saveSettings() {

    const settings = {
        website_name: document.getElementById("websiteName").value,
        main_color: document.getElementById("mainColor").value,
        theme: document.getElementById("theme").value,
        refresh_time: document.getElementById("refreshTime").value,
        cpu_limit: document.getElementById("cpuLimit").value,
        ram_limit: document.getElementById("ramLimit").value,
        disk_limit: document.getElementById("diskLimit").value,

        show_dashboard: document.getElementById("showDashboard").checked,
        show_cpu: document.getElementById("showCPU").checked,
        show_ram: document.getElementById("showRAM").checked,
        show_disk: document.getElementById("showDisk").checked,
        show_network: document.getElementById("showNetwork").checked,
        show_alerts: document.getElementById("showAlerts").checked,
        show_reports: document.getElementById("showReports").checked
    };

    const response = await fetch("/api/settings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(settings)
    });

    const result = await response.json();

    document.getElementById("saveMessage").innerText =
        result.message;
}

</script>

</body>
</html>
