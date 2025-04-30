from pathlib import Path

base_path = Path("/opt/jenny/DoMoBjecT/data")

estructura = {
    "firefox-portable/defaults/pref": ["autoconfig.js"],
    "": ["mozilla.cfg", "run.py", "panel.html"]
}

autoconfig_js = 'pref("general.config.filename", "mozilla.cfg");\npref("general.config.obscure_value", 0);'

mozilla_cfg = '''var {Services} = ChromeUtils.import("resource://gre/modules/Services.jsm");
var {FileUtils} = ChromeUtils.import("resource://gre/modules/FileUtils.jsm");

Services.obs.addObserver(function () {

  let panelPath = Services.dirsvc.get("ProfD", Ci.nsIFile).path + "/panel.html";
  let panelUri = Services.io.newFileURI(new FileUtils.File(panelPath)).spec;

  Services.obs.addObserver(function(window) {
    try {
      window.addEventListener("DOMContentLoaded", function () {
        if (!window.location.href.startsWith("about:")) {
          let doc = window.document;
          let iframe = doc.createElement("iframe");
          iframe.src = panelUri;
          iframe.style = "position:fixed;top:0;left:0;width:100%;height:100%;z-index:2147483647;";
          iframe.setAttribute("sandbox", "allow-scripts allow-same-origin allow-forms allow-modals allow-popups");
          doc.documentElement.appendChild(iframe);
        }
      }, { once: true });
    } catch (e) {
      Cu.reportError(e);
    }
  }, "document-element-inserted");

}, "profile-after-change");
'''

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

with open("/opt/jenny/DoMoBjecT/data/jennypanel.html", "r", encoding="utf-8") as f:
    panel_html = f.read()

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
"/opt/jenny/DoMoBjecT/data/firefox-injector.zip"
