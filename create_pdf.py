try:
    from reportlab.pdfgen import canvas
except ImportError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.pdfgen import canvas

c = canvas.Canvas("java_resume.pdf")
c.drawString(100, 750, "I am a Java Developer")
c.save()
print("PDF created successfully")
