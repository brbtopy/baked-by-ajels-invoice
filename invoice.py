from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from decimal import Decimal
from datetime import date, timedelta
import requests, json
from stat import S_IREAD, S_IRGRP, S_IROTH
from stat import S_IWUSR
from PIL import Image, ImageEnhance
import fitz  # PyMuPDF
import io


def read_counter(directory):
    called = True
    if called:
        count_file = open(directory, "r")
        count = count_file.read()
        count_file.close()
    return count

def increase_counter(directory):
    called = True
    if called:
        count_file = open(directory, "r")
        count = count_file.read()
        count_file.close()

        count_file = open(directory, "w")
        count = int(count) + 1
        count_file.write(str(count))
        count_file.close()
    return count

def drawMyRuler(pdf):
    pdf.drawString(100,750, 'x100')
    pdf.drawString(200,750, 'x200')
    pdf.drawString(300,750, 'x300')
    pdf.drawString(400,750, 'x400')
    pdf.drawString(500,750, 'x500')
    pdf.drawString(600,750, 'x600')
    pdf.drawString(700,750, 'x700')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')

pdf = canvas.Canvas("C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\test.pdf", pagesize=letter)
pdf.setLineWidth(0)
# drawMyRuler(pdf)

invoice_no_file = "C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\counter\\counter.txt"
os.chmod(invoice_no_file, S_IWUSR|S_IREAD)

today = date.today()

print("\n[+] Welcome to AJELS Invoice Generator")
print("[+] Please provide the following details to generate an invoice\n")
print("[+] Note: To end the purchase list, type 'end' when asked for the product name\n")

username = str(input("Who's invoice is being created? "))
username = username.title()
user_phone = str(input(f"What is the contact address for {username}? "))

invoice_no = "#0" + str(read_counter(invoice_no_file))

logo = os.path.join(os.getcwd(), "C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\pictures\\logo.jpg")
pdf.drawImage(logo, 60, 680, width=70, height=73)

pdf.setFont("Courier-Bold", 12)
pdf.drawString(60, 630, "ISSUED TO:")
pdf.setFont("Courier", 12)
pdf.drawString(60, 610, username.title())
pdf.drawString(60, 590, user_phone)

pdf.setFont("Courier-Bold", 12)
pdf.drawString(480, 630, "INVOICE NO:")
if int(read_counter(invoice_no_file)) < 10:
    pdf.drawString(534, 610, invoice_no)
if int(read_counter(invoice_no_file)) >= 10 and int(read_counter(invoice_no_file)) < 100:
    pdf.drawString(527, 610, invoice_no)
if int(read_counter(invoice_no_file)) >= 100 and int(read_counter(invoice_no_file)) < 1000:
    pdf.drawString(520, 610, invoice_no)
if int(read_counter(invoice_no_file)) >= 1000 and int(read_counter(invoice_no_file)) < 10000:
    pdf.drawString(513, 610, invoice_no)
if int(read_counter(invoice_no_file)) >= 10000:
    pdf.drawString(506, 610, invoice_no)
pdf.setFont("Courier", 11)
date_format = today.strftime("%d.%b.%Y")
pdf.drawString(483, 590, date_format)

pdf.line(60, 565, 557, 565)
pdf.line(60, 525, 557, 525)

pdf.setFont("Courier-Bold", 13)
pdf.drawString(63, 541, "DESCRIPTION")
pdf.drawString(240, 541, "UNIT PRICE")
pdf.drawString(390, 541, "QTY")
pdf.drawString(510, 541, "TOTAL")

#append purchase list to little invoice table
product = input(f"What is {username} buying? ")
product = product.title()
unit_price = Decimal(input(f"What is the unit price of {product} that {username} is buying? "))
quantity = int(input(f"What is the quantity of {product} that {username} is buying? "))

x_axis = 67
y_axis = 500
make_up_y = 70

count = 0
total = 0
while product.lower() != "end":
    unit_price_dsp = ("%.2f" % unit_price)
    pdf.setFont("Courier", 11)
    pdf.drawString(x_axis, y_axis, product.title())
    pdf.drawString(x_axis+185, y_axis, str(unit_price_dsp))
    pdf.drawString(x_axis+329, y_axis, str(quantity))
    unit_total = unit_price * quantity
    unit_total_dsp = ("%.2f" % unit_total)
    pdf.drawString(x_axis+437, y_axis, str(unit_total_dsp))
    y_axis = y_axis - 25

    product = input(f"What next is {username} buying? ")
    product = product.title()

    total = total + unit_total
    count += 1

    if product.lower() == "end":
        break
    unit_price = Decimal(input(f"What is the unit price of {product} that {username} is buying? "))
    quantity = int(input(f"What is the quantity of {product} that {username} is buying? "))

total_dsp = ("%.2f" % total)

# end_date = int(input(f"\n[+] How many days is {username} given to pay? "))

if count <= 3:
    pdf.setFont("Courier", 11)
    pdf.line(60, 300+make_up_y, 557, 300+make_up_y)
    pdf.line(60, 260+make_up_y, 557, 260+make_up_y)

    pdf.setFont("Courier-Bold", 13)
    pdf.drawString(63, 276+make_up_y, "TOTAL")
    if total < 100:
        pdf.drawString(484, 276+make_up_y, f"Ghc {total_dsp}")
    if total >= 100 and total < 1000 :
        pdf.drawString(477, 276+make_up_y, f"Ghc {total_dsp}")
    if total >= 1000 and total < 10000:
        pdf.drawString(470, 276+make_up_y, f"Ghc {total_dsp}")
    if total >= 10000:
        pdf.drawString(463, 276+make_up_y, f"Ghc {total_dsp}")

    pdf.setFont("Courier-Bold", 13)
    pdf.drawString(60, 130+make_up_y, "ACCOUNT DETAILS")
    pdf.setFont("Courier", 12)
    pdf.drawString(60, 105+make_up_y, "MTN MOBILE MONEY WALLET")
    pdf.drawString(60, 85+make_up_y, "Account Name: Stacey N Adjeley Adjei")
    pdf.drawString(60, 65+make_up_y, "Account Number: 0540563300")
    # pay_by = today + timedelta(days=end_date)
    # pdf.drawString(60, 45+make_up_y, f"Pay by: {pay_by.strftime("%d %B %Y")}")

    thanks = os.path.join(os.getcwd(), "C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\pictures\\thanks.png")
    pdf.drawImage(thanks, 440, 50+make_up_y, width=130, height=130)

if count > 3:
    pdf.setFont("Courier", 11)
    pdf.line(60, 300, 557, 300)
    pdf.line(60, 260, 557, 260)

    pdf.setFont("Courier-Bold", 13)
    pdf.drawString(63, 276, "TOTAL")
    if total < 100:
        pdf.drawString(484, 276, f"Ghc {total_dsp}")
    if total >= 100 and total < 1000 :
        pdf.drawString(477, 276, f"Ghc {total_dsp}")
    if total >= 1000 and total < 10000:
        pdf.drawString(470, 276, f"Ghc {total_dsp}")
    if total >= 10000:
        pdf.drawString(463, 276, f"Ghc {total_dsp}")

    pdf.setFont("Courier-Bold", 13)
    pdf.drawString(60, 130, "ACCOUNT DETAILS")
    pdf.setFont("Courier", 12)
    pdf.drawString(60, 105, "MTN MOBILE MONEY WALLET")
    pdf.drawString(60, 85, "Account Name: Stacey N Adjeley Adjei")
    pdf.drawString(60, 65, "Account Number: 0540563300")
    # pay_by = today + timedelta(days=end_date)
    # pdf.drawString(60, 45, f"Pay by: {pay_by.strftime("%d %B %Y")}")

    thanks = os.path.join(os.getcwd(), "C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\pictures\\thanks.png")
    pdf.drawImage(thanks, 440, 50, width=130, height=130)

pdf.save()

#################################################################################
#adding watermark to receipt
# Function to compress images
def compress_image(image, quality=50):
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer)

document_path = 'C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\test.pdf'
watermark_path = 'C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\pictures\\logo.jpg'
opacity = 0.08

# Open the original document
pdf_document = fitz.open(document_path)
page = pdf_document.load_page(0)  # Load the first page

# Load the watermark image
watermark = Image.open(watermark_path).convert("RGBA")

# Resize the watermark to a larger size
document_width, document_height = page.rect.width, page.rect.height
watermark_width = int(document_width * 0.75)  # Increase the width to 75% of the document width
watermark_height = int(watermark.size[1] * (watermark_width / watermark.size[0]))
watermark = watermark.resize((watermark_width, watermark_height), Image.LANCZOS)

# Adjust the opacity of the watermark
alpha = watermark.split()[3]
alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
watermark.putalpha(alpha)

# Convert the watermark to a pixmap
watermark_bytes = io.BytesIO()
watermark.save(watermark_bytes, format='PNG')
watermark_pix = fitz.Pixmap(watermark_bytes.getvalue())

# Calculate the position to center the watermark
x = (document_width - watermark_width) // 2
y = (document_height - watermark_height) // 2

# Apply the watermark to the page
page.insert_image(fitz.Rect(x, y, x + watermark_width, y + watermark_height), pixmap=watermark_pix, overlay=True)

# Save the result with compression
output_file = f"C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\invoice_docs\\{username}'s invoice_{invoice_no}.pdf"
pdf_document.save(output_file, garbage=4, deflate=True, clean=True)
pdf_document.close()

os.remove("C:\\Users\\SAMUEL\\Desktop\\proj\\ajels\\baked-by-ajels-invoice\\test.pdf")

increase_counter(invoice_no_file)
os.chmod(invoice_no_file, S_IREAD|S_IRGRP|S_IROTH)

print(f"\n[+] Invoice for {username} has been generated successfully!")
print(f"[+] Invoice saved as {username}'s invoice_{invoice_no}.pdf in the invoice_docs folder")
print("[+] Thank you for using AJELS Invoice Generator")