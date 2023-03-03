import os

import pdfkit
from flask import Flask, send_file, request
from jinja2 import Environment, FileSystemLoader

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello from Flask & Docker</h2>'

def get_headers():
    content ={
        "company": request.headers.get('company'),
        "address_line1": request.headers.get('address_line1'),
        "address_line2": request.headers.get('address_line2'),
        "address_line3": request.headers.get('address_line3'),
        "id_number": request.headers.get('id_number'),
        "account_number": request.headers.get('account_number'),
        "payment_date": request.headers.get('payment_date'),
        "due_date": request.headers.get('due_date'),
        "payment_method": request.headers.get("payment_method"),
        "subtotal": request.headers.get('subtotal'),
        "tax_rate": request.headers.get('tax_rate'),
        "tax": request.headers.get('tax'),
        "shipping": request.headers.get('shipping'),
        "total": request.headers.get('total'),
        "paid": request.headers.get('paid'),
        "description": request.headers.get('description'),
        "quantity": request.headers.get('quantity'),
        "unit_price": request.headers.get('unit_price'),
        "item_total": request.headers.get('item_total'),
    }
    
    # Organize the list of items sent:
    items = []
    # Assuming if description has content, they all do:
    if content["description"]:
        try:
            description = content["description"].split('","')
            quantity = content["quantity"].split('","')
            unit_price = content["unit_price"].split('","')
            item_total = content["item_total"].split('","')
            for i, _ in enumerate(description):
                items.append(
                    {
                        "description": description[i],
                        "quantity": quantity[i],
                        "unit_price": unit_price[i],
                        "item_total": item_total[i],
                    }
                )
        except:
            print("description, quantity, unit_price, and item_total missmatch")
    content["items"] = items
    
    return content


def cleanup_old_files():
    #TODO
    return None


@app.route('/test_headers')
def test_headers():
    # Get headers that are sent:
    content = get_headers()
    
    return content, 200


@app.route('/receipt')
def send_receipt():
    # Get headers that are sent:
    content = get_headers()

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("receipt.html")
    rendered_html = template.render(
        content,
    )
    
    filename = f"receipt_{content['id_number']}.html"
    filename_pdf = f"receipt_{content['id_number']}.pdf"
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered_html)
    
    pdfkit.from_file(filename, filename_pdf, options={"enable-local-file-access": ""})
    entry = os.path.join(os.getcwd(), filename_pdf)

    # Cleanup function that looks for files with id_numbers
    # less than 100 the current value:
    ##cleanup_old_files()
    
    return send_file(entry), 200


@app.route('/invoice')
def send_invoice():
    # Get headers that are sent:
    content = get_headers()

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("invoice.html")
    rendered_html = template.render(
        content,
    )
    
    filename = f"invoice_{content['id_number']}.html"
    filename_pdf = f"invoice_{content['id_number']}.pdf"
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered_html)
    
    pdfkit.from_file(filename, filename_pdf, options={"enable-local-file-access": ""})
    entry = os.path.join(os.getcwd(), filename_pdf)

    # Cleanup function that looks for files with id_numbers
    # less than 100 the current value:
    ##cleanup_old_files()
    
    return send_file(entry), 200


@app.route('/refund')
def send_refund():
    # Get headers that are sent:
    content = get_headers()

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("refund.html")
    rendered_html = template.render(
        content,
    )
    
    filename = f"refund_{content['id_number']}.html"
    filename_pdf = f"refund_{content['id_number']}.pdf"
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered_html)
    
    pdfkit.from_file(filename, filename_pdf, options={"enable-local-file-access": ""})
    entry = os.path.join(os.getcwd(), filename_pdf)

    # Cleanup function that looks for files with id_numbers
    # less than 100 the current value:
    ##cleanup_old_files()
    
    return send_file(entry), 200


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
