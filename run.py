import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pathlib import Path

geckodriver_autoinstaller.install()

firefox_path = Path("./firefox-portable/firefox").resolve()

options = Options()
options.binary_location = str(firefox_path)

driver = webdriver.Firefox(options=options)
driver.get("about:blank")
