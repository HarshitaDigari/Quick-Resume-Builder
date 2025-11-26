import streamlit as st   #venv\Scripts\activate.bat    
from reportlab.lib.pagesizes import A4 #streamlit run codee.py
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
import io

# PDF generator function
def generate_pdf(name, email, phone, linkedin, github, location, objective, education, projects, internships, certifications, skills, activities, languages):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Title style
    title_style = ParagraphStyle(name="TitleStyle", fontSize=24, textColor=colors.HexColor("#1E90FF"), alignment=1, leading=28, spaceAfter=6, fontName="Helvetica-Bold")

    # Section header style
    section_style = ParagraphStyle(name="SectionStyle", fontSize=16, textColor=colors.HexColor("#1E90FF"), leading=20, spaceAfter=4, fontName="Helvetica-Bold")

    # Normal text style
    normal_style = ParagraphStyle(name="NormalStyle", fontSize=11, leading=14, fontName="Helvetica")

    # Small text style (for date & CGPA)
    small_style = ParagraphStyle(name="SmallStyle", fontSize=10, textColor=colors.black, leading=12)

    # Resume Header
    story.append(Paragraph(f"<b>{name}</b>", title_style))
    story.append(Paragraph(f"{email} | {phone} | {linkedin} | {github} | {location}", normal_style))
    story.append(Spacer(1, 12))

    # Helper function to add section with underline
    def add_section(title):
        story.append(Paragraph(title, section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor("#1E90FF")))
        story.append(Spacer(1, 6))

    # Objective
    add_section("Objective")
    story.append(Paragraph(objective, normal_style))
    story.append(Spacer(1, 12))

    # Education
    add_section("Education")
    for edu in education:
        story.append(Paragraph(f"<b>{edu['institute']}</b>", normal_style))
        story.append(Paragraph(f"{edu['course']}", normal_style))
        story.append(Paragraph(f"{edu['date']} | CGPA: {edu['cgpa']}", small_style))
        story.append(Spacer(1, 8))

    # Projects
    add_section("Projects")
    for proj in projects:
        story.append(Paragraph(f"<b>{proj['title']}</b>", normal_style))
        story.append(Paragraph(f"{proj['description']}", normal_style))
        story.append(Paragraph(f"Tech Stack: {proj['techstack']}", small_style))
        story.append(Spacer(1, 8))

    # Internships (Optional)
    if internships:
        add_section("Internships & Training")
        for intern in internships:
            story.append(Paragraph(f"<b>{intern['topic']}</b>", normal_style))
            story.append(Paragraph(f"{intern['date']}", small_style))
            story.append(Paragraph(f"{intern['description']}", normal_style))
            story.append(Spacer(1, 8))

    # Certifications
    if certifications:
        add_section("Certifications")
        for cert in certifications:
            story.append(Paragraph(f"- {cert}", normal_style))
        story.append(Spacer(1, 12))

    # Skills
    add_section("Skills")
    story.append(Paragraph(", ".join(skills), normal_style))
    story.append(Spacer(1, 12))

    # Activities
    if activities:
        add_section("Extra Activities")
        story.append(Paragraph(", ".join(activities), normal_style))
        story.append(Spacer(1, 12))

    # Languages
    add_section("Languages")
    story.append(Paragraph(", ".join(languages), normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

#'Streamlit App'
st.title("Resume Builder")

# Personal Information
st.header("Personal Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
linkedin = st.text_input("LinkedIn")
github = st.text_input("GitHub")
location = st.text_input("Location")

# Objective
objective = st.text_area("Objective")

# Education
st.header("Education")
education = []
edu_count = st.number_input("Number of Education Entries", min_value=1, value=1)
for i in range(int(edu_count)):
    institute = st.text_input(f"Institute Name {i+1}", key=f"institute_{i}")
    course = st.text_input(f"Course {i+1}", key=f"course_{i}")
    date = st.text_input(f"Date {i+1}", key=f"date_{i}")
    cgpa = st.text_input(f"CGPA {i+1}", key=f"cgpa_{i}")
    education.append({"institute": institute, "course": course, "date": date, "cgpa": cgpa})

# Projects
st.header("Projects")
projects = []
proj_count = st.number_input("Number of Projects", min_value=1, value=1)
for i in range(int(proj_count)):
    title = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
    description = st.text_area(f"Project Description {i+1}", key=f"proj_desc_{i}")
    techstack = st.text_input(f"Tech Stack {i+1}", key=f"proj_tech_{i}")
    projects.append({"title": title, "description": description, "techstack": techstack})

# Internships (Optional)
st.header("Internships & Training (Optional)")
internships = []
intern_count = st.number_input("Number of Internships", min_value=0, value=0)
for i in range(int(intern_count)):
    topic = st.text_input(f"Internship/Training Topic {i+1}", key=f"intern_topic_{i}")
    intern_date = st.text_input(f"Date {i+1}", key=f"intern_date_{i}")
    intern_desc = st.text_area(f"Description {i+1}", key=f"intern_desc_{i}")
    internships.append({"topic": topic, "date": intern_date, "description": intern_desc})

# Certifications
st.header("Certifications (Optional)")
certifications = []
cert_count = st.number_input("Number of Certifications", min_value=0, value=0)
for i in range(int(cert_count)):
    cert = st.text_input(f"Certification {i+1}", key=f"cert_{i}")
    certifications.append(cert)

# Skills
st.header("Skills")
skills = st.text_area("Enter skills separated by commas").split(",")

# Extra Activities
st.header("Extra Activities (Optional)")
activities = st.text_area("Enter extra activities separated by commas").split(",")

# Languages
st.header("Languages")
languages = st.text_area("Enter languages separated by commas").split(",")

# Generate Resume
if st.button("Generate Resume"):
    pdf = generate_pdf(name, email, phone, linkedin, github, location, objective, education, projects, internships, certifications, skills, activities, languages)
    st.download_button("Download Resume", data=pdf, file_name="resume.pdf", mime="application/pdf")