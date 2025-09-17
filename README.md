# google-classroom-document-download-tool

Because sometimes you just want all the files — without right-click → download → repeat 1000 times.  
This tool sneaks into Google Classroom (with your cookies), grabs every `.ipynb`, `.pdf`, `.png`, etc., and saves them with the correct names.  

No API, no pain. Just download and chill.  

<img width="1915" height="867" alt="Screenshot" src="https://github.com/user-attachments/assets/4ed449d0-a4ec-4193-a4a2-092d1cbaaff5" />

---

## Features
- Auto-login Google Classroom using Selenium  
- Extracts Google Drive file links automatically  
- Supports `.ipynb`, `.pdf`, `.png`, `.jpg`, and other formats  
- Saves files with original filenames and extensions  

---

## Installation
Clone this repository:
```bash
git clone https://github.com/yourusername/google-classroom-document-download-tool.git
cd google-classroom-document-download-tool
Install the dependencies:

bash
Sao chép mã
pip install -r requirements.txt
requirements.txt should contain:

nginx
Sao chép mã
selenium
requests
beautifulsoup4
You also need Google Chrome and ChromeDriver installed.

Usage
Open the script file assignment_download.py.

Replace the placeholders with your Google Classroom credentials and course URL:

python
Sao chép mã
EMAIL = "your_email"
PASSWORD = "your_password"
COURSE_URL = "your_classroom_course_url"
Run the script:

bash
Sao chép mã
python assignment_download.py
Files will be downloaded into the downloads/ folder.

Notes
This tool uses Selenium to log in, so you will see a browser window pop up.

Make sure you have access to the Classroom course before running.

This project is for educational purposes only. Please respect Google’s terms of service.

css
Sao chép mã
