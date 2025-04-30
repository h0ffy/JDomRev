from pathlib import Path

base_path = Path("/opt/jenny/DoMoBjecT/data/firefox-portable")

# Estructura de directorios a crear
estructura = {
    "firefox-portable/defaults/pref": ["autoconfig.js"],
    "": ["mozilla.cfg", "run.py", "panel.html"]
}

# Crear contenido de autoconfig.js
autoconfig_js = 'pref("general.config.filename", "mozilla.cfg");\npref("general.config.obscure_value", 0);'

# Crear contenido de mozilla.cfg
mozilla_cfg = '''// Configuración inicial de Firefox con inyección JS
var {Services} = ChromeUtils.import("resource://gre/modules/Services.jsm");
Services.obs.addObserver(function () {
  Services.console.logStringMessage("JS inyectado desde mozilla.cfg");

  let panelPath = Services.dirsvc.get("ProfD", Ci.nsIFile).path + "/panel.html";
  let panelUri = Services.io.newFileURI(new FileUtils.File(panelPath)).spec;

  Services.obs.addObserver(function(window) {
    if (window.location.href === "about:blank") {
      let doc = window.document;
      let iframe = doc.createElement("iframe");
      iframe.style = "position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;";
      iframe.src = panelUri;
      doc.body.appendChild(iframe);
    }
  }, "chrome-document-global-created");
}, "profile-after-change");
'''

# Crear contenido de run.py
run_py = '''import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pathlib import Path

geckodriver_autoinstaller.install()

firefox_path = Path("./firefox-portable/firefox").resolve()

options = Options()
options.binary_location = str(firefox_path)

driver = webdriver.Firefox(options=options)
driver.get("about:blank")
'''

# Leer el contenido del panel HTML subido
with open("/opt/jenny/DoMoBjecT/data/jennypanel.html", "r", encoding="utf-8") as f:
    panel_html = f.read()

# Crear archivos con contenido en la estructura especificada
for dir_path, files in estructura.items():
    full_dir = base_path / dir_path
    full_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        file_path = full_dir / file
        if file == "autoconfig.js":
            file_path.write_text(autoconfig_js, encoding="utf-8")
        elif file == "mozilla.cfg":
            file_path.write_text(mozilla_cfg, encoding="utf-8")
        elif file == "run.py":
            file_path.write_text(run_py, encoding="utf-8")
        elif file == "panel.html":
            file_path.write_text(panel_html, encoding="utf-8")

import shutil
shutil.make_archive("/opt/jenny/DoMoBjecT/data/firefox-injector", 'zip', base_path)

"/opt/jenny/DoMoBjecT/data/data/firefox-injector.zip"
