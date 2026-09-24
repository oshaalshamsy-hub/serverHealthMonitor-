<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ServerHealthMonitor2</title>

<style>

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

:root{
    --bg:#0f172a;
    --sidebar:#111827;
    --card:#1e293b;
    --text:#ffffff;
    --muted:#94a3b8;
    --border:#334155;
    --accent:#2563eb;
    --green:#22c55e;
    --orange:#f59e0b;
    --red:#ef4444;
}

body{
    font-family:Arial, sans-serif;
    background:var(--bg);
    color:var(--text);
    min-height:100vh;
}

body.light{
    --bg:#f1f5f9;
    --sidebar:#e2e8f0;
    --card:#ffffff;
    --text:#0f172a;
    --muted:#64748b;
    --border:#cbd5e1;
}

body.green{
    --accent:#16a34a;
}

body.purple{
    --accent:#7c3aed;
}


/* =========================
   LAYOUT
========================= */

.layout{
    display:flex;
    min-height:100vh;
}


/* =========================
   SIDEBAR
========================= */

.sidebar{
    width:240px;
    background:var(--sidebar);
    padding:22px 15px;
    position:fixed;
    top:0;
    bottom:0;
    left:0;
    overflow-y:auto;
}

.logo{
    font-size:28px;
    font-weight:bold;
    margin-bottom:4px;
}

.logo span{
    color:#3b82f6;
}

.logo-sub{
    color:var(--muted);
    font-size:11px;
    margin-bottom:25px;
}

.menu-title{
    color:var(--muted);
    font-size:11px;
    font-weight:bold;
    margin-bottom:10px;
}

.sidebar button{
    width:100%;
    border:none;
    background:transparent;
    color:var(--text);
    padding:12px 14px;
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
    margin-top:18px !important;
    border:1px solid var(--border) !important;
}


/* =========================
   MAIN
========================= */

.main{
    margin-left:240px;
    width:calc(100% - 240px);
}

.topbar{
    background:var(--card);
    padding:20px 30px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-bottom:1px solid var(--border);
}

.topbar h1{
    font-size:25px;
}

.topbar p{
    color:var(--muted);
    font-size:12px;
    margin-top:5px;
}

.refresh-btn{
    background:var(--accent);
    border:none;
    color:white;
    padding:11px 20px;
    border-radius:9px;
    cursor:pointer;
}


/* =========================
   PAGES
========================= */

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


/* =========================
   CARDS
========================= */

.cards{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:18px;
}

.card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:22px;
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
    height:10px;
    width:100%;
    background:var(--border);
    border-radius:20px;
    overflow:hidden;
    margin-bottom:10px;
}

.progress div{
    height:100%;
    background:var(--accent);
    width:0%;
    transition:0.4s;
}

.details{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:18px;
    margin-top:18px;
}

.detail{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:15px;
    padding:20px;
}

.detail h3{
    color:var(--muted);
    font-size:14px;
    margin-bottom:10px;
}


/* =========================
   STATUS
========================= */

.healthy{
    color:var(--green);
    font-weight:bold;
}

.warning{
    color:var(--orange);
    font-weight:bold;
}

.critical{
    color:var(--red);
    font-weight:bold;
}


/* =========================
   INFO
========================= */

.info-box{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:25px;
    margin-top:20px;
}

.info-box p{
    padding:12px 0;
    border-bottom:1px solid var(--border);
}

.info-box p:last-child{
    border:none;
}


/* =========================
   BIG MONITOR
========================= */

.big-monitor{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:18px;
    padding:40px;
    max-width:600px;
    text-align:center;
    margin-top:20px;
}

.big-monitor h1{
    font-size:75px;
    color:var(--accent);
}


/* =========================
   OS
========================= */

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


/* =========================
   PROCESSES
========================= */

.process-item{
    background:var(--card);
    border:1px solid var(--border);
    padding:13px 15px;
    margin-bottom:8px;
    border-radius:10px;
    display:flex;
    justify-content:space-between;
}

.process-item span{
    color:var(--muted);
}


/* =========================
   ADMIN
========================= */

.admin-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:18px;
    margin-top:20px;
}

.admin-card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:25px;
}

.admin-card label{
    display:block;
    margin-top:15px;
    margin-bottom:6px;
}

.admin-card input,
.admin-card select{
    width:100%;
    padding:11px;
    border-radius:8px;
    border:1px solid var(--border);
    background:var(--bg);
    color:var(--text);
}

.feature-list{
    margin-top:15px;
}

.feature-list label{
    padding:10px;
    border:1px solid var(--border);
    border-radius:8px;
    margin-bottom:8px;
}

.feature-list input{
    width:auto;
    margin-right:8px;
}

.save-btn{
    background:var(--accent);
    color:white;
    border:none;
    padding:13px 24px;
    border-radius:10px;
    cursor:pointer;
    margin-top:20px;
}

.save-message{
    color:var(--green);
    margin-top:12px;
}


/* =========================
   MOBILE
========================= */

@media(max-width:800px){

    .layout{
        display:block;
    }

    .sidebar{
        position:static;
        width:100%;
    }

    .main{
        margin-left:0;
        width:100%;
    }

    .cards,
    .details{
        grid-template-columns:1fr;
    }

    .os-grid{
        grid-template-columns:1fr 1fr;
    }

    .admin-grid{
        grid-template-columns:1fr;
    }

    .topbar{
        flex-direction:column;
        align-items:flex-start;
        gap:12px;
    }

    .refresh-btn{
        width:100%;
    }

    .page{
        padding:18px;
    }
}

</style>
</head>

<body>

<div class="layout">


<!-- =========================
     SIDEBAR
========================= -->

<aside class="sidebar">

    <div class="logo">
        SERVER<span>Hub</span>
    </div>

    <div class="logo-sub">
        Smart Server Monitoring
    </div>

    <div class="menu-title">
        MONITORING
    </div>

    <button id="menuDashboard" onclick="showPage('dashboard')">
        Dashboard
    </button>

    <button id="menuSystem" onclick="showPage('system')">
        System Info
    </button>

    <button id="menuCPU" onclick="showPage('cpu')">
        CPU Monitor
    </button>

    <button id="menuRAM" onclick="showPage('ram')">
        RAM Monitor
    </button>

    <button id="menuDisk" onclick="showPage('disk')">
        Disk Monitor
    </button>

    <button id="menuNetwork" onclick="showPage('network')">
        Network Monitor
    </button>

    <button id="menuProcesses" onclick="showPage('processes')">
        Processes
    </button>

    <button id="menuOS" onclick="showPage('os')">
        Operating Systems
    </button>

    <button id="menuAlerts" onclick="showPage('alerts')">
        Alerts
    </button>

    <button id="menuReports" onclick="showPage('reports')">
        Reports
    </button>

    <button class="admin-button" onclick="showPage('admin')">
        Admin Control
    </button>

</aside>


<!-- =========================
     MAIN
========================= -->

<main class="main">


<header class="topbar">

    <div>

        <h1 id="websiteTitle">
            ServerHealthMonitor2
        </h1>

        <p>
            Smart Server Health & Performance Monitoring
        </p>

    </div>

    <button class="refresh-btn" onclick="refreshData()">
        Refresh
    </button>

</header>


<!-- =========================
     DASHBOARD
========================= -->

<section id="dashboard" class="page active">

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

            <div id="cpuValue" class="card-value">
                24%
            </div>

            <div class="progress">
                <div id="cpuBar"></div>
            </div>

            <div id="cpuStatus" class="healthy">
                HEALTHY
            </div>

        </div>


        <div class="card">

            <div class="card-title">
                RAM Usage
            </div>

            <div id="ramValue" class="card-value">
                46%
            </div>

            <div class="progress">
                <div id="ramBar"></div>
            </div>

            <div id="ramStatus" class="healthy">
                HEALTHY
            </div>

        </div>


        <div class="card">

            <div class="card-title">
                Disk Usage
            </div>

            <div id="diskValue" class="card-value">
                58%
            </div>

            <div class="progress">
                <div id="diskBar"></div>
            </div>

            <div id="diskStatus" class="healthy">
                HEALTHY
            </div>

        </div>


    </div>


    <div class="details">


        <div class="detail">

            <h3>
                Operating System
            </h3>

            <p>
                Windows 11
            </p>

        </div>


        <div class="detail">

            <h3>
                Computer Name
            </h3>

            <p>
                SERVERHub-PC
            </p>

        </div>


        <div class="detail">

            <h3>
                IP Address
            </h3>

            <p>
                192.168.1.10
            </p>

        </div>


    </div>

</section>


<!-- =========================
     SYSTEM INFO
========================= -->

<section id="system" class="page">

    <h2>
        System Information
    </h2>

    <div class="info-box">

        <p>
            <strong>Computer Name:</strong>
            SERVERHub-PC
        </p>

        <p>
            <strong>Operating System:</strong>
            Windows 11
        </p>

        <p>
            <strong>Processor:</strong>
            Intel Processor
        </p>

        <p>
            <strong>CPU Cores:</strong>
            8
        </p>

        <p>
            <strong>Total RAM:</strong>
            16 GB
        </p>

        <p>
            <strong>IP Address:</strong>
            192.168.1.10
        </p>

    </div>

</section>


<!-- =========================
     CPU
========================= -->

<section id="cpu" class="page">

    <h2>
        CPU Monitor
    </h2>

    <div class="big-monitor">

        <h1 id="cpuLarge">
            24%
        </h1>

        <p>
            Current CPU Usage
        </p>

    </div>

</section>


<!-- =========================
     RAM
========================= -->

<section id="ram" class="page">

    <h2>
        RAM Monitor
    </h2>

    <div class="big-monitor">

        <h1 id="ramLarge">
            46%
        </h1>

        <p>
            Current RAM Usage
        </p>

    </div>

</section>


<!-- =========================
     DISK
========================= -->

<section id="disk" class="page">

    <h2>
        Disk Monitor
    </h2>

    <div class="big-monitor">

        <h1 id="diskLarge">
            58%
        </h1>

        <p>
            Current Disk Usage
        </p>

        <br>

        <p>
            Total Disk: 512 GB
        </p>

        <p>
            Free Space: 215 GB
        </p>

    </div>

</section>


<!-- =========================
     NETWORK
========================= -->

<section id="network" class="page">

    <h2>
        Network Monitor
    </h2>

    <div class="info-box">

        <p>
            <strong>Computer:</strong>
            SERVERHub-PC
        </p>

        <p>
            <strong>IP Address:</strong>
            192.168.1.10
        </p>

        <p>
            <strong>Network Status:</strong>
            Connected
        </p>

        <p>
            <strong>Connection:</strong>
            Wi-Fi
        </p>

    </div>

</section>


<!-- =========================
     PROCESSES
========================= -->

<section id="processes" class="page">

    <h2>
        Running Processes
    </h2>

    <br>

    <div class="process-item">

        <strong>
            Google Chrome
        </strong>

        <span>
            PID 1024
        </span>

    </div>


    <div class="process-item">

        <strong>
            Python
        </strong>

        <span>
            PID 2025
        </span>

    </div>


    <div class="process-item">

        <strong>
            Windows Explorer
        </strong>

        <span>
            PID 3040
        </span>

    </div>


    <div class="process-item">

        <strong>
            Microsoft Edge
        </strong>

        <span>
            PID 4080
        </span>

    </div>

</section>


<!-- =========================
     OPERATING SYSTEMS
========================= -->

<section id="os" class="page">

    <h2>
        Supported Operating Systems
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


<!-- =========================
     ALERTS
========================= -->

<section id="alerts" class="page">

    <h2>
        Alerts
    </h2>

    <div class="info-box">

        <p id="alertsText" class="healthy">
            No active alerts. System is healthy.
        </p>

    </div>

</section>


<!-- =========================
     REPORTS
========================= -->

<section id="reports" class="page">

    <h2>
        System Report
    </h2>

    <div class="info-box">

        <p>
            <strong>System:</strong>
            SERVERHub-PC
        </p>

        <p>
            <strong>CPU:</strong>
            <span id="reportCPU">24%</span>
        </p>

        <p>
            <strong>RAM:</strong>
            <span id="reportRAM">46%</span>
        </p>

        <p>
            <strong>Disk:</strong>
            <span id="reportDisk">58%</span>
        </p>

        <p>
            <strong>Status:</strong>
            <span class="healthy">HEALTHY</span>
        </p>

    </div>

</section>


<!-- =========================
     ADMIN CONTROL
========================= -->

<section id="admin" class="page">

    <div class="page-title">

        <h2>
            SERVERHub Admin Control
        </h2>

        <p>
            Control your website from here
        </p>

    </div>


    <div class="admin-grid">


        <div class="admin-card">

            <h3>
                Website Settings
            </h3>

            <label>
                Website Name
            </label>

            <input
                type="text"
                id="adminWebsiteName"
                value="ServerHealthMonitor2"
            >


            <label>
                Theme
            </label>

            <select id="adminTheme">

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

            <select id="adminColor">

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

        </div>


        <div class="admin-card">

            <h3>
                Alert Settings
            </h3>

            <label>
                CPU Warning %
            </label>

            <input
                type="number"
                id="cpuLimit"
                value="70"
            >


            <label>
                RAM Warning %
            </label>

            <input
                type="number"
                id="ramLimit"
                value="70"
            >


            <label>
                Disk Warning %
            </label>

            <input
                type="number"
                id="diskLimit"
                value="80"
            >

        </div>


        <div class="admin-card">

            <h3>
                Show / Hide Features
            </h3>

            <div class="feature-list">

                <label>
                    <input id="showCPU" type="checkbox" checked>
                    CPU Monitor
                </label>

                <label>
                    <input id="showRAM" type="checkbox" checked>
                    RAM Monitor
                </label>

                <label>
                    <input id="showDisk" type="checkbox" checked>
                    Disk Monitor
                </label>

                <label>
                    <input id="showNetwork" type="checkbox" checked>
                    Network Monitor
                </label>

                <label>
                    <input id="showProcesses" type="checkbox" checked>
                    Processes
                </label>

                <label>
                    <input id="showAlerts" type="checkbox" checked>
                    Alerts
                </label>

                <label>
                    <input id="showReports" type="checkbox" checked>
                    Reports
                </label>

            </div>

        </div>


    </div>


    <button class="save-btn" onclick="saveAdminSettings()">
        Save Changes
    </button>

    <p id="saveMessage" class="save-message"></p>

</section>


</main>

</div>


<script>

/* =========================
   PAGE NAVIGATION
========================= */

function showPage(pageID){

    document
    .querySelectorAll(".page")
    .forEach(page => {

        page.classList.remove("active");

    });

    document
    .getElementById(pageID)
    .classList.add("active");

}


/* =========================
   DEMO MONITORING
========================= */

let cpu = 24;
let ram = 46;
let disk = 58;


function refreshData(){

    cpu =
        Math.floor(
            Math.random() * 60
        ) + 15;

    ram =
        Math.floor(
            Math.random() * 45
        ) + 35;

    disk =
        Math.floor(
            Math.random() * 25
        ) + 50;


    updateDisplay();

}


function updateDisplay(){

    document.getElementById("cpuValue").innerText =
        cpu + "%";

    document.getElementById("ramValue").innerText =
        ram + "%";

    document.getElementById("diskValue").innerText =
        disk + "%";


    document.getElementById("cpuLarge").innerText =
        cpu + "%";

    document.getElementById("ramLarge").innerText =
        ram + "%";

    document.getElementById("diskLarge").innerText =
        disk + "%";


    document.getElementById("cpuBar").style.width =
        cpu + "%";

    document.getElementById("ramBar").style.width =
        ram + "%";

    document.getElementById("diskBar").style.width =
        disk + "%";


    document.getElementById("reportCPU").innerText =
        cpu + "%";

    document.getElementById("reportRAM").innerText =
        ram + "%";

    document.getElementById("reportDisk").innerText =
        disk + "%";


    updateStatus(
        "cpuStatus",
        cpu,
        Number(
            localStorage.getItem("cpuLimit") || 70
        )
    );


    updateStatus(
        "ramStatus",
        ram,
        Number(
            localStorage.getItem("ramLimit") || 70
        )
    );


    updateStatus(
        "diskStatus",
        disk,
        Number(
            localStorage.getItem("diskLimit") || 80
        )
    );


    updateAlerts();

}


function updateStatus(
    elementID,
    value,
    warningLimit
){

    const element =
        document.getElementById(elementID);


    if(value >= 90){

        element.innerText =
            "CRITICAL";

        element.className =
            "critical";

    }

    else if(value >= warningLimit){

        element.innerText =
            "WARNING";

        element.className =
            "warning";

    }

    else{

        element.innerText =
            "HEALTHY";

        element.className =
            "healthy";

    }

}


function updateAlerts(){

    const cpuLimit =
        Number(
            localStorage.getItem("cpuLimit") || 70
        );

    const ramLimit =
        Number(
            localStorage.getItem("ramLimit") || 70
        );

    const diskLimit =
        Number(
            localStorage.getItem("diskLimit") || 80
        );


    let alerts = [];


    if(cpu >= cpuLimit){

        alerts.push(
            "CPU usage is high"
        );

    }


    if(ram >= ramLimit){

        alerts.push(
            "RAM usage is high"
        );

    }


    if(disk >= diskLimit){

        alerts.push(
            "Disk usage is high"
        );

    }


    const alertsText =
        document.getElementById(
            "alertsText"
        );


    if(alerts.length === 0){

        alertsText.innerText =
            "No active alerts. System is healthy.";

        alertsText.className =
            "healthy";

    }

    else{

        alertsText.innerText =
            alerts.join(" | ");

        alertsText.className =
            "warning";

    }

}


/* =========================
   ADMIN CONTROL
========================= */

function saveAdminSettings(){

    const websiteName =
        document
        .getElementById(
            "adminWebsiteName"
        )
        .value;


    const theme =
        document
        .getElementById(
            "adminTheme"
        )
        .value;


    const color =
        document
        .getElementById(
            "adminColor"
        )
        .value;


    const cpuLimit =
        document
        .getElementById(
            "cpuLimit"
        )
        .value;


    const ramLimit =
        document
        .getElementById(
            "ramLimit"
        )
        .value;


    const diskLimit =
        document
        .getElementById(
            "diskLimit"
        )
        .value;


    localStorage.setItem(
        "websiteName",
        websiteName
    );


    localStorage.setItem(
        "theme",
        theme
    );


    localStorage.setItem(
        "color",
        color
    );


    localStorage.setItem(
        "cpuLimit",
        cpuLimit
    );


    localStorage.setItem(
        "ramLimit",
        ramLimit
    );


    localStorage.setItem(
        "diskLimit",
        diskLimit
    );


    localStorage.setItem(
        "showCPU",
        document.getElementById("showCPU").checked
    );


    localStorage.setItem(
        "showRAM",
        document.getElementById("showRAM").checked
    );


    localStorage.setItem(
        "showDisk",
        document.getElementById("showDisk").checked
    );


    localStorage.setItem(
        "showNetwork",
        document.getElementById("showNetwork").checked
    );


    localStorage.setItem(
        "showProcesses",
        document.getElementById("showProcesses").checked
    );


    localStorage.setItem(
        "showAlerts",
        document.getElementById("showAlerts").checked
    );


    localStorage.setItem(
        "showReports",
        document.getElementById("showReports").checked
    );


    applySettings();


    document
    .getElementById("saveMessage")
    .innerText =
        "Settings saved successfully!";

}


/* =========================
   APPLY SETTINGS
========================= */

function applySettings(){

    const websiteName =
        localStorage.getItem(
            "websiteName"
        ) || "ServerHealthMonitor2";


    const theme =
        localStorage.getItem(
            "theme"
        ) || "dark";


    const color =
        localStorage.getItem(
            "color"
        ) || "blue";


    document.title =
        websiteName;


    document
    .getElementById(
        "websiteTitle"
    )
    .innerText =
        websiteName;


    document
    .getElementById(
        "adminWebsiteName"
    )
    .value =
        websiteName;


    document
    .getElementById(
        "adminTheme"
    )
    .value =
        theme;


    document
    .getElementById(
        "adminColor"
    )
    .value =
        color;


    document.body.className =
        "";


    if(theme === "light"){

        document.body.classList.add(
            "light"
        );

    }


    if(color === "green"){

        document.body.classList.add(
            "green"
        );

    }


    if(color === "purple"){

        document.body.classList.add(
            "purple"
        );

    }


    loadCheckbox(
        "showCPU",
        "menuCPU"
    );


    loadCheckbox(
        "showRAM",
        "menuRAM"
    );


    loadCheckbox(
        "showDisk",
        "menuDisk"
    );


    loadCheckbox(
        "showNetwork",
        "menuNetwork"
    );


    loadCheckbox(
        "showProcesses",
        "menuProcesses"
    );


    loadCheckbox(
        "showAlerts",
        "menuAlerts"
    );


    loadCheckbox(
        "showReports",
        "menuReports"
    );


    document
    .getElementById("cpuLimit")
    .value =
        localStorage.getItem(
            "cpuLimit"
        ) || 70;


    document
    .getElementById("ramLimit")
    .value =
        localStorage.getItem(
            "ramLimit"
        ) || 70;


    document
    .getElementById("diskLimit")
    .value =
        localStorage.getItem(
            "diskLimit"
        ) || 80;


    updateDisplay();

}


function loadCheckbox(
    storageName,
    menuID
){

    const stored =
        localStorage.getItem(
            storageName
        );


    const enabled =
        stored === null
        ?
        true
        :
        stored === "true";


    document
    .getElementById(storageName)
    .checked =
        enabled;


    document
    .getElementById(menuID)
    .style.display =
        enabled
        ?
        "block"
        :
        "none";

}


/* =========================
   START
========================= */

applySettings();

updateDisplay();

setInterval(
    refreshData,
    5000
);

</script>

</body>
</html>
