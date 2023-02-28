import pdfkit

pdfkit.from_file('index.html', 'out.pdf', options={"enable-local-file-access": ""})
