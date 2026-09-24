from flask import Flask, jsonify, request, render_template_string
import psutil
import platform
import socket
import os
import json
from datetime import datetime

app = Flask(__name__)

# =========================================================
# SETTINGS
# =========================================================

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "website_name": "ServerHealthMonitor2",
    "theme": "dark",
    "main_color": "blue",
    "refresh_time": 5,

    "cpu_limit": 70,
    "ram_limit": 70,
    "disk_limit": 80,

    "show_dashboard": True,
    "show_system": True,
    "show_cpu": True,
    "show_ram": True,
    "show_disk": True,
    "show_network": True,
    "show_processes": True,
    "show_os": True,
    "show_alerts": True,
    "show_reports": True
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        with open(SETTINGS_FILE, "w") as file:
            json.dump(DEFAULT_SETTINGS, file, indent=4)

        return DEFAULT_SETTINGS.copy()

    try:

        with open(SETTINGS_FILE, "r") as file:
            saved = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(saved)

        return settings

    except:

        return DEFAULT_SETTINGS.copy()


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:

        json.dump(
            settings,
            file,
            indent=4
        )


# =========================================================
# SYSTEM FUNCTIONS
# =========================================================

def get_ip():

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

        s.close()

        return ip

    except:

        try:

            return socket.gethostbyname(
                socket.gethostname()
            )

        except:

            return "Unavailable"


def status(value, warning, critical):

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "HEALTHY"


# =========================================================
# MAIN WEBSITE HTML
# =========================================================

MAIN_PAGE = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>ServerHealthMonitor2</title>


<style>

*{
box-sizing:border-box;
margin:0;
padding:0;
}

:root{

--background:#0f172a;
--sidebar:#111827;
--card:#1e293b;
--text:#f8fafc;
--muted:#94a3b8;
--border:#334155;
--accent:#2563eb;

--green:#22c55e;
--orange:#f59e0b;
--red:#ef4444;

}


body{

font-family:Arial,sans-serif;

background:var(--background);

color:var(--text);

min-height:100vh;

}


body.green{

--accent:#16a34a;

}


body.purple{

--accent:#7c3aed;

}


body.light{

--background:#f1f5f9;

--sidebar:#e2e8f0;

--card:white;

--text:#0f172a;

--muted:#64748b;

--border:#cbd5e1;

}


/* ================= SIDEBAR ================= */

.sidebar{

position:fixed;

left:0;

top:0;

bottom:0;

width:240px;

background:var(--sidebar);

padding:20px;

overflow-y:auto;

}


.logo{

font-size:28px;

font-weight:bold;

margin-bottom:5px;

color:white;

}


.logo span{

color:#3b82f6;

}


.logo-sub{

font-size:11px;

color:var(--muted);

margin-bottom:30px;

}


.menu-title{

font-size:11px;

color:var(--muted);

margin-bottom:10px;

font-weight:bold;

}


.sidebar button{

width:100%;

border:none;

background:transparent;

color:var(--text);

padding:12px;

margin-bottom:6px;

text-align:left;

border-radius:10px;

cursor:pointer;

font-size:14px;

}


.sidebar button:hover{

background:var(--accent);

color:white;

}


.admin-button{

display:block;

margin-top:20px;

padding:12px;

border:1px solid var(--border);

border-radius:10px;

text-decoration:none;

color:var(--text);

text-align:center;

}


.admin-button:hover{

background:var(--accent);

color:white;

}


/* ================= MAIN ================= */

.main{

margin-left:240px;

min-height:100vh;

}


.topbar{

background:var(--card);

padding:20px 30px;

display:flex;

align-items:center;

justify-content:space-between;

border-bottom:1px solid var(--border);

}


.topbar h1{

font-size:25px;

}


.topbar p{

font-size:12px;

color:var(--muted);

margin-top:5px;

}


.refresh{

background:var(--accent);

border:none;

color:white;

padding:11px 20px;

border-radius:9px;

cursor:pointer;

}


.page{

display:none;

padding:30px;

}


.page.active{

display:block;

}


.page-title{

margin-bottom:25px;

}


.page-title p{

color:var(--muted);

margin-top:5px;

}


/* ================= CARDS ================= */

.cards{

display:grid;

grid-template-columns:repeat(3,1fr);

gap:18px;

}


.card{

background:var(--card);

padding:22px;

border-radius:16px;

border:1px solid var(--border);

}


.card-title{

color:var(--muted);

font-size:14px;

}


.card-value{

font-size:36px;

font-weight:bold;

margin:12px 0;

}


.progress{

width:100%;

height:9px;

background:var(--border);

border-radius:20px;

overflow:hidden;

margin-bottom:10px;

}


.progress div{

height:100%;

background:var(--accent);

width:0%;

transition:.4s;

}


.details{

display:grid;

grid-template-columns:repeat(3,1fr);

gap:18px;

margin-top:18px;

}


.detail{

background:var(--card);

padding:20px;

border-radius:15px;

border:1px solid var(--border);

}


.detail h3{

font-size:14px;

color:var(--muted);

margin-bottom:10px;

}


/* ================= STATUS ================= */

.HEALTHY{

color:var(--green);

font-weight:bold;

}


.WARNING{

color:var(--orange);

font-weight:bold;

}


.CRITICAL{

color:var(--red);

font-weight:bold;

}


/* ================= INFO ================= */

.info{

background:var(--card);

padding:25px;

border-radius:16px;

border:1px solid var(--border);

margin-top:20px;

}


.info p{

padding:12px 0;

border-bottom:1px solid var(--border);

}


.info p:last-child{

border:none;

}


/* ================= LARGE MONITOR ================= */

.large-monitor{

background:var(--card);

max-width:600px;

padding:40px;

border-radius:18px;

border:1px solid var(--border);

text-align:center;

margin-top:20px;

}


.large-monitor h1{

font-size:75px;

color:var(--accent);

}


/* ================= OS ================= */

.os-grid{

display:grid;

grid-template-columns:repeat(4,1fr);

gap:15px;

margin-top:20px;

}


.os-box{

background:var(--card);

border:1px solid var(--border);

padding:25px;

border-radius:15px;

text-align:center;

font-weight:bold;

}


/* ================= PROCESSES ================= */

.process{

background:var(--card);

padding:12px 15px;

margin-bottom:8px;

border-radius:10px;

border:1px solid var(--border);

display:flex;

justify-content:space-between;

}


.process span{

color:var(--muted);

}


/* ================= MOBILE ================= */

@media(max-width:800px){

.sidebar{

position:static;

width:100%;

}

.main{

margin-left:0;

}

.cards,

.details{

grid-template-columns:1fr;

}

.os-grid{

grid-template-columns:1fr 1fr;

}

.topbar{

flex-direction:column;

align-items:flex-start;

gap:12px;

}

.refresh{

width:100%;

}

}

</style>

</head>


<body>

<div class="sidebar">

<div class="logo">
SERVER<span>Hub</span>
</div>

<div class="logo-sub">
Smart Server Monitoring
</div>

<div class="menu-title">
MONITORING
</div>


<button data-setting="show_dashboard"
onclick="showPage('dashboard')">
Dashboard
</button>


<button data-setting="show_system"
onclick="showPage('system')">
System Info
</button>


<button data-setting="show_cpu"
onclick="showPage('cpu')">
CPU Monitor
</button>


<button data-setting="show_ram"
onclick="showPage('ram')">
RAM Monitor
</button>


<button data-setting="show_disk"
onclick="showPage('disk')">
Disk Monitor
</button>


<button data-setting="show_network"
onclick="showPage('network')">
Network Monitor
</button>


<button data-setting="show_processes"
onclick="showProcesses()">
Processes
</button>


<button data-setting="show_os"
onclick="showPage('os')">
Operating Systems
</button>


<button data-setting="show_alerts"
onclick="showPage('alerts')">
Alerts
</button>


<button data-setting="show_reports"
onclick="showPage('reports')">
Reports
</button>


<a href="/admin"
class="admin-button">
Admin Control
</a>

</div>


<div class="main">

<header class="topbar">

<div>

<h1 id="websiteTitle">
ServerHealthMonitor2
</h1>

<p>
Smart Server Health & Performance Monitoring
</p>

</div>


<button class="refresh"
onclick="loadSystem()">

Refresh

</button>

</header>


<!-- ================= DASHBOARD ================= -->

<section id="dashboard"
class="page active">


<div class="page-title">

<h2>
System Dashboard
</h2>

<p>
Live system health overview
</p>

</div>


<div class="cards">


<div class="card">

<div class="card-title">
CPU Usage
</div>

<div id="cpuValue"
class="card-value">
0%
</div>

<div class="progress">
<div id="cpuBar"></div>
</div>

<div id="cpuStatus">
Loading...
</div>

</div>



<div class="card">

<div class="card-title">
RAM Usage
</div>

<div id="ramValue"
class="card-value">
0%
</div>

<div class="progress">
<div id="ramBar"></div>
</div>

<div id="ramStatus">
Loading...
</div>

</div>



<div class="card">

<div class="card-title">
Disk Usage
</div>

<div id="diskValue"
class="card-value">
0%
</div>

<div class="progress">
<div id="diskBar"></div>
</div>

<div id="diskStatus">
Loading...
</div>

</div>

</div>


<div class="details">


<div class="detail">

<h3>
Operating System
</h3>

<p id="osValue">
Loading...
</p>

</div>


<div class="detail">

<h3>
Computer Name
</h3>

<p id="computerValue">
Loading...
</p>

</div>


<div class="detail">

<h3>
IP Address
</h3>

<p id="ipValue">
Loading...
</p>

</div>


</div>

</section>



<!-- ================= SYSTEM ================= -->

<section id="system"
class="page">

<h2>
System Information
</h2>

<div class="info">

<p>
<strong>Computer Name:</strong>
<span id="systemComputer"></span>
</p>

<p>
<strong>Operating System:</strong>
<span id="systemOS"></span>
</p>

<p>
<strong>OS Version:</strong>
<span id="systemVersion"></span>
</p>

<p>
<strong>Processor:</strong>
<span id="systemProcessor"></span>
</p>

<p>
<strong>CPU Cores:</strong>
<span id="systemCores"></span>
</p>

<p>
<strong>Total RAM:</strong>
<span id="systemRAM"></span>
</p>

<p>
<strong>IP Address:</strong>
<span id="systemIP"></span>
</p>

</div>

</section>



<!-- ================= CPU ================= -->

<section id="cpu"
class="page">

<h2>
CPU Monitor
</h2>

<div class="large-monitor">

<h1 id="cpuLarge">
0%
</h1>

<p>
Current CPU Usage
</p>

</div>

</section>



<!-- ================= RAM ================= -->

<section id="ram"
class="page">

<h2>
RAM Monitor
</h2>

<div class="large-monitor">

<h1 id="ramLarge">
0%
</h1>

<p>
Current RAM Usage
</p>

</div>

</section>



<!-- ================= DISK ================= -->

<section id="disk"
class="page">

<h2>
Disk Monitor
</h2>

<div class="large-monitor">

<h1 id="diskLarge">
0%
</h1>

<p>
Disk Usage
</p>

<br>

<p>
Total:
<span id="diskTotal"></span>
</p>

<p>
Free:
<span id="diskFree"></span>
</p>

</div>

</section>



<!-- ================= NETWORK ================= -->

<section id="network"
class="page">

<h2>
Network Monitor
</h2>

<div class="info">

<p>
<strong>Computer:</strong>
<span id="networkComputer"></span>
</p>

<p>
<strong>IP Address:</strong>
<span id="networkIP"></span>
</p>

<p>
<strong>Status:</strong>
Connected
</p>

</div>

</section>



<!-- ================= PROCESSES ================= -->

<section id="processes"
class="page">

<h2>
Running Processes
</h2>

<br>

<button class="refresh"
onclick="loadProcesses()">

Refresh Processes

</button>

<br><br>

<div id="processList">
</div>

</section>



<!-- ================= OPERATING SYSTEMS ================= -->

<section id="os"
class="page">

<h2>
Operating Systems
</h2>

<div class="os-grid">

<div class="os-box">
Windows
</div>

<div class="os-box">
macOS
</div>

<div class="os-box">
Linux
</div>

<div class="os-box">
Android
</div>

<div class="os-box">
iOS
</div>

<div class="os-box">
iPadOS
</div>

<div class="os-box">
watchOS
</div>

<div class="os-box">
tvOS
</div>

</div>

</section>



<!-- ================= ALERTS ================= -->

<section id="alerts"
class="page">

<h2>
Alerts
</h2>

<div class="info">

<p id="alertText">

No alerts.

</p>

</div>

</section>



<!-- ================= REPORTS ================= -->

<section id="reports"
class="page">

<h2>
Reports
</h2>

<div class="info">

<p>
<strong>Date:</strong>
<span id="reportDate"></span>
</p>

<p>
<strong>CPU:</strong>
<span id="reportCPU"></span>
</p>

<p>
<strong>RAM:</strong>
<span id="reportRAM"></span>
</p>

<p>
<strong>Disk:</strong>
<span id="reportDisk"></span>
</p>

<p>
<strong>Operating System:</strong>
<span id="reportOS"></span>
</p>

</div>

</section>


</div>



<script>

let settings = {};

let refreshTimer;


/* ================= PAGE CONTROL ================= */

function showPage(id){

document
.querySelectorAll(".page")
.forEach(page=>{

page.classList.remove("active");

});

document
.getElementById(id)
.classList.add("active");

}


/* ================= SETTINGS ================= */

async function loadSettings(){

const response =
await fetch("/api/settings");

settings =
await response.json();


document.title =
settings.website_name;


document
.getElementById("websiteTitle")
.innerText =
settings.website_name;


document.body.className = "";


if(settings.theme === "light"){

document.body.classList.add("light");

}


if(settings.main_color === "green"){

document.body.classList.add("green");

}


if(settings.main_color === "purple"){

document.body.classList.add("purple");

}


document
.querySelectorAll("[data-setting]")
.forEach(button=>{

const key =
button.dataset.setting;

button.style.display =
settings[key]
? "block"
: "none";

});


if(refreshTimer){

clearInterval(refreshTimer);

}


refreshTimer =
setInterval(

loadSystem,

Number(settings.refresh_time) * 1000

);

}


/* ================= SYSTEM DATA ================= */

async function loadSystem(){

const response =
await fetch("/api/system");

const data =
await response.json();


document
.getElementById("cpuValue")
.innerText =
data.cpu + "%";


document
.getElementById("ramValue")
.innerText =
data.ram + "%";


document
.getElementById("diskValue")
.innerText =
data.disk + "%";


document
.getElementById("cpuBar")
.style.width =
data.cpu + "%";


document
.getElementById("ramBar")
.style.width =
data.ram + "%";


document
.getElementById("diskBar")
.style.width =
data.disk + "%";


setStatus(
"cpuStatus",
data.cpu_status
);


setStatus(
"ramStatus",
data.ram_status
);


setStatus(
"diskStatus",
data.disk_status
);


document
.getElementById("osValue")
.innerText =
data.os + " " + data.os_release;


document
.getElementById("computerValue")
.innerText =
data.computer;


document
.getElementById("ipValue")
.innerText =
data.ip;


/* SYSTEM INFO */


document
.getElementById("systemComputer")
.innerText =
data.computer;


document
.getElementById("systemOS")
.innerText =
data.os;


document
.getElementById("systemVersion")
.innerText =
data.os_release;


document
.getElementById("systemProcessor")
.innerText =
data.processor;


document
.getElementById("systemCores")
.innerText =
data.cpu_cores;


document
.getElementById("systemRAM")
.innerText =
data.ram_total + " GB";


document
.getElementById("systemIP")
.innerText =
data.ip;


/* LARGE VALUES */


document
.getElementById("cpuLarge")
.innerText =
data.cpu + "%";


document
.getElementById("ramLarge")
.innerText =
data.ram + "%";


document
.getElementById("diskLarge")
.innerText =
data.disk + "%";


document
.getElementById("diskTotal")
.innerText =
data.disk_total + " GB";


document
.getElementById("diskFree")
.innerText =
data.disk_free + " GB";


/* NETWORK */


document
.getElementById("networkComputer")
.innerText =
data.computer;


document
.getElementById("networkIP")
.innerText =
data.ip;


/* ALERTS */


let alerts = [];


if(
data.cpu_status !== "HEALTHY"
){

alerts.push(
"CPU: " +
data.cpu_status
);

}


if(
data.ram_status !== "HEALTHY"
){

alerts.push(
"RAM: " +
data.ram_status
);

}


if(
data.disk_status !== "HEALTHY"
){

alerts.push(
"Disk: " +
data.disk_status
);

}


document
.getElementById("alertText")
.innerText =

alerts.length

?

alerts.join(" | ")

:

"No active alerts. System is healthy.";


/* REPORT */


document
.getElementById("reportDate")
.innerText =
data.date_time;


document
.getElementById("reportCPU")
.innerText =
data.cpu + "%";


document
.getElementById("reportRAM")
.innerText =
data.ram + "%";


document
.getElementById("reportDisk")
.innerText =
data.disk + "%";


document
.getElementById("reportOS")
.innerText =
data.os + " " + data.os_release;

}


function setStatus(
element,
value
){

const item =
document.getElementById(element);

item.innerText =
value;

item.className =
value;

}


/* ================= PROCESSES ================= */

async function showProcesses(){

showPage("processes");

loadProcesses();

}


async function loadProcesses(){

const response =
await fetch("/api/processes");

const processes =
await response.json();


const list =
document.getElementById(
"processList"
);


list.innerHTML = "";


processes.forEach(process=>{

const row =
document.createElement("div");


row.className =
"process";


row.innerHTML =

"<strong>" +

process.name +

"</strong>" +

"<span>" +

"PID: " +

process.pid +

" | RAM: " +

process.memory +

"%" +

"</span>";


list.appendChild(row);

});

}


/* START */

async function start(){

await loadSettings();

await loadSystem();

}


start();

</script>


</body>

</html>
"""


# =========================================================
# ADMIN CONTROL HTML
# =========================================================

ADMIN_PAGE = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Admin Control
</title>


<style>

*{

box-sizing:border-box;

}


body{

margin:0;

font-family:Arial;

background:#0f172a;

color:white;

}


.container{

max-width:1000px;

margin:auto;

padding:35px 20px;

}


.header{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:30px;

}


.header p{

color:#94a3b8;

}


.back{

background:#2563eb;

color:white;

padding:12px 18px;

border-radius:9px;

text-decoration:none;

}


.grid{

display:grid;

grid-template-columns:1fr 1fr;

gap:20px;

}


.card{

background:#1e293b;

padding:25px;

border-radius:16px;

}


.card h2{

margin-top:0;

}


label{

display:block;

margin-top:15px;

margin-bottom:6px;

}


input,

select{

width:100%;

padding:12px;

border-radius:8px;

border:1px solid #475569;

background:#0f172a;

color:white;

}


.features{

grid-column:1/-1;

}


.checkbox{

display:grid;

grid-template-columns:1fr 1fr;

gap:10px;

}


.checkbox label{

background:#0f172a;

padding:12px;

border-radius:8px;

}


.checkbox input{

width:auto;

margin-right:8px;

}


.save{

margin-top:20px;

background:#2563eb;

color:white;

border:none;

padding:14px 25px;

border-radius:10px;

font-size:16px;

cursor:pointer;

}


.message{

color:#22c55e;

margin-top:12px;

}


@media(max-width:700px){

.grid{

grid-template-columns:1fr;

}


.features{

grid-column:auto;

}


.checkbox{

grid-template-columns:1fr;

}


.header{

flex-direction:column;

align-items:flex-start;

gap:15px;

}

}

</style>

</head>


<body>

<div class="container">


<div class="header">

<div>

<h1>
SERVERHub Admin Control
</h1>

<p>
Control your website from here.
</p>

</div>


<a href="/"
class="back">

Back to Website

</a>

</div>


<div class="grid">


<div class="card">

<h2>
Website Settings
</h2>


<label>
Website Name
</label>

<input
id="website_name"
type="text">


<label>
Theme
</label>

<select id="theme">

<option value="dark">
Dark
</option>

<option value="light">
Light
</option>

</select>


<label>
Main Color
</label>

<select id="main_color">

<option value="blue">
Blue
</option>

<option value="green">
Green
</option>

<option value="purple">
Purple
</option>

</select>


<label>
Refresh Time
</label>

<input
id="refresh_time"
type="number"
min="2"
max="60">

</div>



<div class="card">

<h2>
Alert Limits
</h2>


<label>
CPU Warning %
</label>

<input
id="cpu_limit"
type="number">


<label>
RAM Warning %
</label>

<input
id="ram_limit"
type="number">


<label>
Disk Warning %
</label>

<input
id="disk_limit"
type="number">

</div>



<div class="card features">

<h2>
Show / Hide Features
</h2>


<div class="checkbox">


<label>
<input
type="checkbox"
id="show_dashboard">
Dashboard
</label>


<label>
<input
type="checkbox"
id="show_system">
System Info
</label>


<label>
<input
type="checkbox"
id="show_cpu">
CPU Monitor
</label>


<label>
<input
type="checkbox"
id="show_ram">
RAM Monitor
</label>


<label>
<input
type="checkbox"
id="show_disk">
Disk Monitor
</label>


<label>
<input
type="checkbox"
id="show_network">
Network Monitor
</label>


<label>
<input
type="checkbox"
id="show_processes">
Processes
</label>


<label>
<input
type="checkbox"
id="show_os">
Operating Systems
</label>


<label>
<input
type="checkbox"
id="show_alerts">
Alerts
</label>


<label>
<input
type="checkbox"
id="show_reports">
Reports
</label>


</div>

</div>


</div>


<button
class="save"
onclick="saveSettings()">

Save Changes

</button>


<div
id="message"
class="message">

</div>


</div>


<script>


const fields = [

"website_name",

"theme",

"main_color",

"refresh_time",

"cpu_limit",

"ram_limit",

"disk_limit",

"show_dashboard",

"show_system",

"show_cpu",

"show_ram",

"show_disk",

"show_network",

"show_processes",

"show_os",

"show_alerts",

"show_reports"

];


async function loadSettings(){

const response =
await fetch("/api/settings");


const settings =
await response.json();


fields.forEach(id=>{

const element =
document.getElementById(id);


if(
element.type === "checkbox"
){

element.checked =
Boolean(settings[id]);

}

else{

element.value =
settings[id];

}

});

}


async function saveSettings(){

let settings = {};


fields.forEach(id=>{

const element =
document.getElementById(id);


if(
element.type === "checkbox"
){

settings[id] =
element.checked;

}

else{

settings[id] =
element.value;

}

});


const response =
await fetch(

"/api/settings",

{

method:"POST",

headers:{

"Content-Type":
"application/json"

},

body:
JSON.stringify(settings)

}

);


const result =
await response.json();


document
.getElementById("message")
.innerText =
result.message;

}


loadSettings();

</script>


</body>

</html>
"""


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        MAIN_PAGE
    )


@app.route("/admin")
def admin():

    return render_template_string(
        ADMIN_PAGE
    )


# =========================================================
# SYSTEM API
# =========================================================

@app.route("/api/system")
def system_api():

    settings = load_settings()

    cpu = psutil.cpu_percent(
        interval=0.3
    )

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage(
        os.path.abspath(os.sep)
    )

    return jsonify({

        "computer":
        socket.gethostname(),

        "os":
        platform.system(),

        "os_release":
        platform.release(),

        "processor":
        platform.processor()
        or
        "Unavailable",

        "cpu":
        cpu,

        "cpu_cores":
        psutil.cpu_count(
            logical=True
        ),

        "ram":
        memory.percent,

        "ram_total":
        round(
            memory.total /
            (1024 ** 3),
            2
        ),

        "disk":
        disk.percent,

        "disk_total":
        round(
            disk.total /
            (1024 ** 3),
            2
        ),

        "disk_free":
        round(
            disk.free /
            (1024 ** 3),
            2
        ),

        "ip":
        get_ip(),

        "cpu_status":
        status(
            cpu,
            int(settings["cpu_limit"]),
            90
        ),

        "ram_status":
        status(
            memory.percent,
            int(settings["ram_limit"]),
            90
        ),

        "disk_status":
        status(
            disk.percent,
            int(settings["disk_limit"]),
            95
        ),

        "date_time":
        datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    })


# =========================================================
# PROCESSES API
# =========================================================

@app.route("/api/processes")
def processes_api():

    process_list = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "memory_percent"
        ]
    ):

        try:

            process_list.append({

                "pid":
                process.info["pid"],

                "name":
                process.info["name"],

                "memory":
                round(
                    process.info[
                        "memory_percent"
                    ],
                    2
                )

            })


            if len(process_list) >= 50:

                break


        except:

            pass


    return jsonify(
        process_list
    )


# =========================================================
# SETTINGS API
# =========================================================

@app.route(
    "/api/settings",
    methods=[
        "GET",
        "POST"
    ]
)
def settings_api():

    settings = load_settings()


    if request.method == "GET":

        return jsonify(
            settings
        )


    data = request.get_json(
        silent=True
    ) or {}


    for key in DEFAULT_SETTINGS:

        if key in data:

            settings[key] = data[key]


    settings["refresh_time"] = max(
        2,
        min(
            60,
            int(
                settings[
                    "refresh_time"
                ]
            )
        )
    )


    settings["cpu_limit"] = max(
        1,
        min(
            100,
            int(
                settings[
                    "cpu_limit"
                ]
            )
        )
    )


    settings["ram_limit"] = max(
        1,
        min(
            100,
            int(
                settings[
                    "ram_limit"
                ]
            )
        )
    )


    settings["disk_limit"] = max(
        1,
        min(
            100,
            int(
                settings[
                    "disk_limit"
                ]
            )
        )
    )


    save_settings(
        settings
    )


    return jsonify({

        "success":
        True,

        "message":
        "Settings saved successfully"

    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
