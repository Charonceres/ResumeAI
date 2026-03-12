# 📄 Resume AI Analyst

An intelligent web application that analyzes PDF resumes against specific industry job roles to identify skill gaps, calculate match percentages, and generate comprehensive, downloadable PDF reports. 

Featuring a sleek, modern UI with dark/light mode and animated SVG progress trackers.

## ✨ Features

* **Dynamic Job Selection:** Choose from multiple industries (Tech, Healthcare, Arts, etc.) and dynamically load specific job roles.
* **Skill Gap Analysis:** Compares the uploaded resume against a database of required skills for the target role.
* **Visual Dashboards:** Beautiful, animated radial progress bars and color-coded chips for "Matched" and "Missing" skills.
* **PDF Report Generation:** Automatically compiles the analysis into a professional, downloadable PDF report.
* **Modern UI/UX:** Drag-and-drop file uploading, responsive design, and a seamless Dark/Light theme toggle.

## 🛠️ Tech Stack

**Frontend:**
* HTML5, CSS3 (Custom styling, CSS Variables for theming)
* Vanilla JavaScript (ES6+ for async fetch API and DOM manipulation)

**Backend:**
* Python 3
* Flask (Web framework and API routing)
* ReportLab (For generating the downloadable PDF reports)

## 📁 Project Structure

```text
resume-ai-project/
│
├── app.py                 # Main Flask application and API endpoints
├── career_data.py         # Database dictionary containing industries, roles, and skills
├── requirements.txt       # Python dependencies (Flask, reportlab)
│
└── templates/             
    └── index.html         # Main frontend UI (HTML/CSS/JS)
