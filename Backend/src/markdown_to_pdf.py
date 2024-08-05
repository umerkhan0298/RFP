import pdfkit
import markdown
from io import BytesIO

# Sample Markdown text
md_text = """
**4. Communication and Reporting:**

* **Communication Protocols:** Establish clear communication protocols for regular updates, status reports, and issue resolution.
* **Reporting Procedures:** Define reporting procedures for project progress, milestones, and any challenges encountered.
"""

# Convert Markdown to HTML
html = markdown.markdown(md_text)

# Convert HTML to PDF
pdf = pdfkit.from_string(html, False)

# Save PDF to a file
with open("output.pdf", "wb") as file:
    file.write(pdf)
