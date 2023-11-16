from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image


def generate_invoice(invoice_data, name):
    # Create a new PDF canvas
    c = canvas.Canvas(f"Pdf/{name}.pdf", pagesize=letter)

    # Set the header
    company_name = "Zydus Lifesciences Ltd."
    address = "123 Main Street, New York"

    c.saveState()

    # Draw company name
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, letter[1] - inch, company_name)

    c.setFont('Helvetica-Bold', 11)
    c.drawString(400, letter[1] - inch-15, "GSTIN : ")

    # draw a line for the partition
    c.line(30, 690, 600, 690)

    # Draw address
    c.setFont("Helvetica", 11)
    c.drawString(50, letter[1] - inch - 15, address)
    c.drawString(450, letter[1]-inch-15, "27AABCA1906H1Z2")

    # Write customer information
    c.drawString(50, 650, "Buyer Name: {}".format(invoice_data["Buyer Name"]))
    c.drawString(50, 630, f'Payment Type: {invoice_data["Payment Type"]}')
    c.drawString(50, 610, f'GST %: {invoice_data["GST"]}')

    # Write invoice details
    c.drawString(400, 650, "Invoice : {}".format(invoice_data["_id"]))
    c.drawString(400, 630, "Invoice Date: {}".format(invoice_data["Selling date"].split(' ')[0]))

    # Write item details in a formatted table
    item_data = []
    for item in invoice_data["Medicine Data"]:
        item_data.append([item["Name"],
                          item["Quantity"],
                          "{}".format(item["Price"]),
                          item['Lot Number'],
                          item['Expiry Date'].split(" ")[0]
                          ])

    # gst_amount = (int(invoice_data['GST']) / 100) * int(invoice_data['Total Price'])

    # Add row count to the table data
    item_data.insert(0, ["Name", "Quantity", "Price (Rs)", "Lot Number", "Expiry Date"])
    item_data.append(["", "", "", "",  f"Total(Rs): {invoice_data['Total Price']}"
                                       f" (Inc gst{invoice_data['GST']}%)"])

    # Define the column widths and table style
    col_widths = [200, 75, 75, 100, 100]
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), 'grey'),
        ('TEXTCOLOR', (0, -1), (-1, -1), 'white'),
        ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ])

    # # Create the table and apply the table style
    invoice_table = Table(item_data, colWidths=col_widths)
    invoice_table.setStyle(table_style)

    # # Draw the table on the canvas
    table_y = 490  # Adjust this value based on table placement
    invoice_table.wrapOn(c, 200, 400)
    invoice_table.drawOn(c, 30, table_y)

    c.setFont("Helvetica", 9)
    # add the signature image in the invoice
    img_path = "/Users/yashmitawa/Documents/Alogbeacon Technology/PyQt_learn/eMediInvoice/Images/signature.jpg"
    c.drawImage(img_path, 400, 320, width=100, height=50)
    c.drawString(430, 310, 'Signature')

    # draw a line for the partition
    c.line(30, 300, 600, 300)

    c.drawString(40, 290, "Thanks for your purchasing")

    # Save the PDF
    c.save()


# if __name__ == "__main__":
#     # Sample invoice data (replace this with your actual invoice data)
#     invoice_data = {
#         "_id": "",
#         "Buyer Name": "satesh",
#         "Selling date": "2023-08-14 00:00:00",
#         "GST": 18,
#         "Payment Type": "Cash",
#         "Medicine Data": [
#             {
#                 "Name": "combifilame ",
#                 "Quantity": 2,
#                 "Price": 4000,
#                 "Lot Number": "yhnbghjkdc",
#                 "Expiry Date": "2024-01-24 00:00:00"
#             },
#             {
#                 "Name": "tablelet1",
#                 "Quantity": 3,
#                 "Price": 1675,
#                 "Lot Number": "ytfghj",
#                 "Expiry Date": "2024-01-26 00:00:00"
#             }
#         ],
#         "Total Price": 13025
#     }
#
#     generate_invoice(invoice_data, "Hello")
