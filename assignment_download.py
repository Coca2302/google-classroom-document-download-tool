import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

EMAIL = "your_mail"
PASSWORD = "your_password"
COURSE_URL = "assignment_url"
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

print("[+] Opening Google Classroom login page...")
driver.get("https://accounts.google.com/")

time.sleep(2)
driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
driver.find_element(By.ID, "identifierId").send_keys(Keys.ENTER)

time.sleep(3)
driver.find_element(By.NAME, "Passwd").send_keys(PASSWORD)
driver.find_element(By.NAME, "Passwd").send_keys(Keys.ENTER)

time.sleep(5)

driver.get(COURSE_URL)
time.sleep(5)

# Lấy cookie từ Selenium để dùng với requests
cookies = {c['name']: c['value'] for c in driver.get_cookies()}
session = requests.Session()
for name, value in cookies.items():
    session.cookies.set(name, value)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "drive.google.com" in href:
        links.append(href)

print(f"[+] Found {len(links)} document links.")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def download_from_drive(session, file_id, dest_path):
    """Download file từ Google Drive (xử lý confirm token + cảnh báo quét virus)."""
    URL = "https://drive.google.com/uc?export=download"

    response = session.get(URL, params={"id": file_id}, stream=True)

    # Nếu bị trả về trang cảnh báo virus => parse link tải thật
    if "text/html" in response.headers.get("content-type", ""):
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", {"id": "download-form"})
        if form:
            action = form["action"]
            inputs = {inp["name"]: inp["value"] for inp in form.find_all("input", {"type": "hidden"})}
            response = session.get(action, params=inputs, stream=True)

    # Lấy tên file từ header
    disposition = response.headers.get("content-disposition", "")
    if "filename=" in disposition:
        filename = disposition.split("filename=")[-1].strip('"').strip("'")
    else:
        filename = f"{file_id}.bin"

    filename = sanitize_filename(filename)
    filepath = os.path.join(dest_path, filename)

    # Ghi file nhị phân
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    print(f"    -> Downloaded: {filename}")
    return filepath

# Tải tất cả file
for i, link in enumerate(links, 1):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', link) or re.search(r'id=([a-zA-Z0-9_-]+)', link)
    if not match:
        print(f"[{i}] Skipped invalid link: {link}")
        continue

    file_id = match.group(1)
    print(f"[{i}/{len(links)}] Downloading file ID: {file_id}")

    try:
        download_from_drive(session, file_id, DOWNLOAD_DIR)
    except Exception as e:
        print(f"[{i}] [!] Download error: {e}")

driver.quit()
print("[+] All downloads completed.")
