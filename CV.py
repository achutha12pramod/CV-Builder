import streamlit as st
from fpdf import FPDF
import base64
from PIL import Image
import io
import pandas as pd
import tempfile

def create_pdf(name, phone, mail, address, summary, skills, achievements, projects, certifications, image_path=None, academic_data=None, linkedin=None):
    pdf = FPDF()
    pdf.add_page()

    # Add Image if provided
    if image_path:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            image_path.save(tmp_file, format="PNG")
            tmp_file.seek(0)
            pdf.image(tmp_file.name, x=10, y=8, w=30)  # Adjusted image size
        pdf.set_y(40)  # Adjust vertical position after image
    
    # Add Name
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"{name}", ln=True)

    # Add Contact Information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Phone : {phone}", ln=True)
    pdf.set_text_color(0, 0, 255)  # Blue color for clickable links
    pdf.cell(200, 10, "Email : "+f"{mail}", ln=True, link=mail)
    if linkedin:
        pdf.cell(200, 10, "LinkedIn : " + f"{linkedin}", ln=True, link=linkedin)
    pdf.set_text_color(0, 0, 0)  # Reset color to black
    pdf.cell(200, 10, f"Address : {address}", ln=True)
    pdf.ln(10)  # Add some space after contact info
    
    # Add Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf.ln(5)  # Add some space after the summary
    
    # Add Academic Qualifications as a Table
    if academic_data is not None:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Academic Qualifications", ln=True)
        pdf.set_font("Arial", size=12)
        
        # Table Header
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(45, 10, "Course", 1, 0, "C", fill=True)
        pdf.cell(70, 10, "Institution", 1, 0, "C", fill=True)
        pdf.cell(40, 10, "Year", 1, 0, "C", fill=True)
        pdf.cell(35, 10, "Aggregate", 1, 1, "C", fill=True)  # Adjusted cell width

        # Table Rows
        for course, institution, year, mark in zip(academic_data['Course'], academic_data['Institute'], academic_data['Year of Completion'], academic_data['Aggregate']):
            pdf.cell(45, 10, course, 1, 0, "C")
            pdf.cell(70, 10, institution, 1, 0, "C")
            pdf.cell(40, 10, year, 1, 0, "C")
            pdf.cell(35, 10, mark, 1, 1, "C")

    # Add Achievements
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Achievements", ln=True)
    pdf.set_font("Arial", size=12)
    for achievement in achievements:
        pdf.multi_cell(0, 10, f"  - {achievement}")
    
    # Add Projects
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Projects", ln=True)
    pdf.set_font("Arial", size=12)
    for project in projects:
        pdf.multi_cell(0, 10, f"  - {project}")
    
    # Add Skills
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Skills", ln=True)
    pdf.set_font("Arial", size=12)
    for skill in skills:
        pdf.cell(200, 10, f"  - {skill}", ln=True)
    
    # Add Certifications
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Certifications", ln=True)
    pdf.set_font("Arial", size=12)
    for certification in certifications:
        pdf.cell(200, 10, f"  - {certification}", ln=True)
    
    return pdf


def main():
    st.title("Resume Builder")

    with st.sidebar:
        st.subheader("Personal Info")
        name = st.text_input("Name")
        phone = st.text_input("Phone number")
        email = st.text_input("Email")
        address = st.text_area("Address")
        linkedin = st.text_input("LinkedIn URL")
        upload_image = st.file_uploader("Photo", type=["png", "jpg", "jpeg"])

        st.subheader("Profile Summary:")
        summary = st.text_area("About:")

        st.subheader("Academic Qualification")
        courses, institutions, periods, marks = [], [], [], []
        num_education = st.number_input("Number of Education Institutes", min_value=1, max_value=5, step=1)
        for i in range(num_education):
            course = st.text_input(f"Course {i+1}:", key=f"course_{i}")
            institution = st.text_input(f"Institution {i+1}:", key=f"institution_{i}")
            period = st.text_input(f"Year of Completion {i+1}:", key=f"period_{i}")
            mark = st.text_input(f"CGPA/Mark/Percent {i+1}:", key=f"mark_{i}")
            courses.append(course)
            institutions.append(institution)
            periods.append(period)
            marks.append(mark)

        st.subheader("Core Competencies")
        skills = st.text_area("Core Competencies (Enter each on a new line)")

        st.subheader("Achievements")
        achievements = st.text_area("Achievements")

        st.subheader("Projects")
        projects = st.text_area("Projects")

        st.subheader("Certifications")
        certifications = st.text_area("Certifications")

    # Displaying the content on the page
    if upload_image is not None:
        image = Image.open(upload_image)
        resized_img = image.resize((150, 150))
        st.image(resized_img)
    else:
        resized_img = None

    st.write(f"**{name}**")
    st.write(f"**Phone** : {phone}")
    st.write(f"**Email** : {email}")
    st.write(f"**Address** : {address}")
    st.write(f"**LinkedIn** : {linkedin}")

    st.subheader("Profile Summary")
    st.write(summary)

    if courses:
        academic_data = {
            "Course": courses,
            "Institute": institutions,
            "Year of Completion": periods,
            "Aggregate": marks
        }
        st.subheader("Academic Qualifications")
        st.table(pd.DataFrame(academic_data))

    st.subheader("Core Competencies")
    skills_list = skills.split("\n")
    for skill in skills_list:
        st.write(f"- {skill}")

    st.subheader("Achievements")
    achieve_list = achievements.split("\n")
    for achievement in achieve_list:
        st.write(f"- {achievement}")

    st.subheader("Projects")
    projects_list = projects.split("\n")
    for project in projects_list:
        st.write(f"- {project}")

    st.subheader("Certifications")
    certificate_list = certifications.split("\n")
    for certificate in certificate_list:
        st.write(f"- {certificate}")

    submitted = st.button("Generate PDF")

    if submitted:
        academic_data = {
            "Course": courses,
            "Institute": institutions,
            "Year of Completion": periods,
            "Aggregate": marks
        }
        pdf = create_pdf(name, phone, email, address, summary, skills_list, achieve_list, projects_list, certificate_list, image_path=resized_img, academic_data=academic_data, linkedin=linkedin)
        pdf_output = f"{name}_Resume.pdf"
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        b64_pdf = base64.b64encode(pdf_bytes).decode('latin1')
        download_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_output}">Download PDF</a>'
        st.markdown(download_link, unsafe_allow_html=True)
        st.success("PDF generated and ready to download!")

if __name__ == '__main__':
    main()
