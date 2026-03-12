from flask import Flask, render_template, request, jsonify, send_file
import json
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import datetime

app = Flask(__name__)

from career_data import career_db


@app.route("/")
def index():
    categories = list(career_db.keys())
    return render_template("index.html", categories=categories)


@app.route("/api/roles/<category>")
def get_roles(category):
    roles = list(career_db.get(category, {}).keys())
    return jsonify(roles)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    category = request.form.get("category")
    role = request.form.get("role")
    resume_file = request.files.get("resume")

    if not category or not role:
        return jsonify({"error": "Please select category and role."}), 400

    if not resume_file or resume_file.filename == "":
        return jsonify({"error": "Please upload a PDF resume."}), 400

    if not resume_file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed."}), 400

    skills = career_db.get(category, {}).get(role, [])
    if not skills:
        return jsonify({"error": "Invalid category or role."}), 400

    # Demo split: first half matched, second half missing
    mid = len(skills) // 2
    matched = skills[:mid]
    missing = skills[mid:]
    percent = int((len(matched) / len(skills)) * 100)

    return jsonify({
        "role": role,
        "percent": percent,
        "matched": matched,
        "missing": missing
    })


@app.route("/api/download_report", methods=["POST"])
def download_report():
    data = request.get_json()
    name = data.get("name", "Candidate")
    role = data.get("role", "")
    percent = data.get("percent", 0)
    matched = data.get("matched", [])
    missing = data.get("missing", [])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", fontSize=22, fontName="Helvetica-Bold",
                                 textColor=colors.HexColor("#1e1e2f"), spaceAfter=4)
    sub_style = ParagraphStyle("sub", fontSize=11, fontName="Helvetica",
                               textColor=colors.HexColor("#718096"), spaceAfter=16)
    section_style = ParagraphStyle("section", fontSize=13, fontName="Helvetica-Bold",
                                   textColor=colors.HexColor("#1e1e2f"), spaceBefore=12, spaceAfter=6)
    normal_style = ParagraphStyle("normal", fontSize=11, fontName="Helvetica",
                                  textColor=colors.HexColor("#2d3748"), spaceAfter=4)

    elements = []

    elements.append(Paragraph("Resume AI — Skill Gap Report", title_style))
    elements.append(Paragraph(f"Generated on {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    elements.append(Spacer(1, 8*mm))

    info_data = [
        ["Candidate Name", name],
        ["Target Role", role],
        ["Match Score", f"{percent}%"],
    ]
    info_table = Table(info_data, colWidths=[50*mm, 120*mm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#718096")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#2d3748")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 6*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))

    elements.append(Paragraph("✅ Matched Skills", section_style))
    for skill in matched:
        elements.append(Paragraph(f"• {skill}", normal_style))

    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph("❌ Missing Skills (Skill Gaps)", section_style))
    for skill in missing:
        elements.append(Paragraph(f"• {skill}", normal_style))

    elements.append(Spacer(1, 8*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph("Resume AI — Skill Gap Finder", ParagraphStyle(
        "footer", fontSize=9, fontName="Helvetica", textColor=colors.HexColor("#adb5bd"), alignment=TA_CENTER
    )))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="Resume_AI_Report.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
