from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import date, timedelta
import requests, json
from stat import S_IREAD, S_IRGRP, S_IROTH
from stat import S_IWUSR

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

pdf = canvas.Canvas("test.pdf", pagesize=letter)
pdf.setLineWidth(0)
# drawMyRuler(pdf)

invoice_no_file = "counter\\counter.txt"
os.chmod(invoice_no_file, S_IWUSR|S_IREAD)

today = date.today()

username = str(input("Who's invoice is being created? "))
username = username.title()
user_phone = str(input(f"What is the contact address for {username}? "))

invoice_no = "#0" + str(read_counter(invoice_no_file))

logo = os.path.join(os.getcwd(), "pictures\\logo.jpg")
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
product_prices = {"Chicken Pieces":10, "Gizzard Khebab":7, "Chicken Khebab":10, "Meat Pie":7, "Rock Buns":5, "Mini Pizza":10,
                  "Quiche Slice":10, "Mini Quiche":8, "Fish Pie":10, "Yam Balls":2.5, "Spring Rolls":2, "Samosa":2.5,
                  "Plain Cake":200, "Baked Flour Chips":150, "Straw Flour Chips":180, "Atsomo":150, "Plantain Chips (Yellow)":100,
                  "Plantain Chips (Brown)":100,"Chips":75,
                  "Coated Nuts":150, "Piped Cookies":150, "Oat Cookies":180, "Ring Donut":180, "Drop Donut":180, "1/2 Riped Plantain Chips":70,
                  "1/2 Unriped Plantain Chips":70}

product = input(f"What is {username} buying? ")
if product.lower() == "chips":
    product_dsp = product_dict = "Chips"
if product.lower() == "half riped plantain chips":
    product_dsp = product_dict = "1/2 Riped Plantain Chips"
if product.lower() == "half unriped plantain chips":
    product_dsp = product_dict = "1/2 Unriped Plantain Chips"
if product.lower() == "baked flour chips":
    product_dsp = product_dict = "Baked Flour Chips"
if product.lower() == "straw flour chips":
    product_dsp = product_dict = "Straw Flour Chips"
if product.lower() == "atsomo":
    product_dsp = product_dict = "Atsomo"
if product.lower() == "chips yellow":
    product_dsp = product_dict = "Plantain Chips (Yellow)"
if product.lower() == "chips brown":
    product_dsp = product_dict = "Plantain Chips (Brown)"
if product.lower() == "coated nuts":
    product_dsp = product_dict = "Coated Nuts"
if product.lower() == "piped cookies":
    product_dsp = product_dict = "Piped Cookies"
if product.lower() == "oat cookies":
    product_dsp = product_dict = "Oat Cookies"
if product.lower() == "ring donut":
    product_dsp = product_dict = "Ring Donut"
if product.lower() == "drop donut":
    product_dsp = product_dict = "Drop Donut"
if product.lower() == "chicken pieces":
    product_dsp = product_dict = "Chicken Pieces"
if product.lower() == "gizzard khebab":
    product_dsp = product_dict = "Gizzard Khebab"
if product.lower() == "chicken khebab":
    product_dsp = product_dict = "Chicken Khebab"
if product.lower() == "meat pie":
    product_dsp = product_dict = "Meat Pie"
if product.lower() == "rock buns":
    product_dsp = product_dict = "Rock Buns"
if product.lower() == "mini pizza":
    product_dsp = product_dict = "Mini Pizza"
if product.lower() == "quiche slice":
    product_dsp = product_dict = "Quiche Slice"
if product.lower() == "mini quiche":
    product_dsp = product_dict = "Mini Quiche"
if product.lower() == "fish pie":
    product_dsp = product_dict = "Fish Pie"
if product.lower() == "yam balls":
    product_dsp = product_dict = "Yam Balls"
if product.lower() == "spring rolls":
    product_dsp = product_dict = "Spring Rolls"
if product.lower() == "samosa":
    product_dsp = product_dict = "Samosa"
if product.lower() == "plain cake":
    product_dsp = product_dict = "Plain Cake"

quantity = int(input(f"What is the quantity of {product_dict} that {username} is buying? "))

x_axis = 67
y_axis = 500
make_up_y = 70

count = 0
total = 0
while product.lower() != "end":
    unit_price = product_prices[product_dict]
    unit_price_dsp = ("%.2f" % unit_price)
    pdf.setFont("Courier", 11)
    pdf.drawString(x_axis, y_axis, product_dsp)
    pdf.drawString(x_axis+185, y_axis, str(unit_price_dsp))
    pdf.drawString(x_axis+329, y_axis, str(quantity))
    unit_total = unit_price * quantity
    unit_total_dsp = ("%.2f" % unit_total)
    pdf.drawString(x_axis+437, y_axis, str(unit_total_dsp))
    y_axis = y_axis - 30

    product = input(f"What next is {username} buying? ")
    if product.lower() == "chips":
        product_dsp = product_dict = "Chips"
    if product.lower() == "half riped plantain chips":
        product_dsp = product_dict = "1/2 Riped Plantain Chips"
    if product.lower() == "half unriped plantain chips":
        product_dsp = product_dict = "1/2 Unriped Plantain Chips"
    if product.lower() == "baked flour chips":
        product_dsp = product_dict = "Baked Flour Chips"
    if product.lower() == "straw flour chips":
        product_dsp = product_dict = "Straw Flour Chips"
    if product.lower() == "atsomo":
        product_dsp = product_dict = "Atsomo"
    if product.lower() == "chips yellow":
        product_dsp = product_dict = "Plantain Chips (Yellow)"
    if product.lower() == "chips brown":
        product_dsp = product_dict = "Plantain Chips (Brown)"
    if product.lower() == "coated nuts":
        product_dsp = product_dict = "Coated Nuts"
    if product.lower() == "piped cookies":
        product_dsp = product_dict = "Piped Cookies"
    if product.lower() == "oat cookies":
        product_dsp = product_dict = "Oat Cookies"
    if product.lower() == "ring donut":
        product_dsp = product_dict = "Ring Donut"
    if product.lower() == "drop donut":
        product_dsp = product_dict = "Drop Donut"
    if product.lower() == "chicken pieces":
        product_dsp = product_dict = "Chicken Pieces"
    if product.lower() == "gizzard khebab":
        product_dsp = product_dict = "Gizzard Khebab"
    if product.lower() == "chicken khebab":
        product_dsp = product_dict = "Chicken Khebab"
    if product.lower() == "meat pie":
        product_dsp = product_dict = "Meat Pie"
    if product.lower() == "rock buns":
        product_dsp = product_dict = "Rock Buns"
    if product.lower() == "mini pizza":
        product_dsp = product_dict = "Mini Pizza"
    if product.lower() == "quiche slice":
        product_dsp = product_dict = "Quiche Slice"
    if product.lower() == "mini quiche":
        product_dsp = product_dict = "Mini Quiche"
    if product.lower() == "fish pie":
        product_dsp = product_dict = "Fish Pie"
    if product.lower() == "yam balls":
        product_dsp = product_dict = "Yam Balls"
    if product.lower() == "spring rolls":
        product_dsp = product_dict = "Spring Rolls"
    if product.lower() == "samosa":
        product_dsp = product_dict = "Samosa"
    if product.lower() == "plain cake":
        product_dsp = product_dict = "Plain Cake"    

    total = total + unit_total
    count += 1

    if product.lower() == "end":
        break
    quantity = int(input(f"What is the quantity of {product_dict} that {username} is buying? "))

total_dsp = ("%.2f" % total)

end_date = int(input(f"\n[+] How many days is {username} given to pay? "))

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
    pay_by = today + timedelta(days=end_date)
    pdf.drawString(60, 45+make_up_y, f"Pay by: {pay_by.strftime("%d %B %Y")}")

    thanks = os.path.join(os.getcwd(), "pictures\\thanks.png")
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
    pay_by = today + timedelta(days=end_date)
    pdf.drawString(60, 45, f"Pay by: {pay_by.strftime("%d %B %Y")}")

    thanks = os.path.join(os.getcwd(), "pictures\\thanks.png")
    pdf.drawImage(thanks, 440, 50, width=130, height=130)

pdf.save()

#################################################################################
#adding watermark to receipt
instructions = {
  'parts': [
    {
      'file': 'document'
    }
  ],
  'actions': [
    {
      'type': 'watermark',
      'image': 'logo',
      'width': '75%',
      "opacity": 0.1
    }
  ]
}

output_file = f"invoice_docs\\{username}'s invoice_{invoice_no}.pdf"

response = requests.request(
  'POST',
  'https://api.pspdfkit.com/build',
  headers = {
    'Authorization': 'Bearer pdf_live_8vTpklf6KnF6ZiK5DqZrbfDJrIcDSTkSJpIlP0beDH7'
  },
  files = {
    'document': open('test.pdf', 'rb'),
    'logo': open('pictures\\logo3.jpg', 'rb')
  },
  data = {
    'instructions': json.dumps(instructions)
  },
  stream = True
)

if response.ok:
  with open(output_file, 'wb') as fd:
    for chunk in response.iter_content(chunk_size=8096):
      fd.write(chunk)
else:
  print(response.text)
  exit()

os.remove("test.pdf")

increase_counter(invoice_no_file)
os.chmod(invoice_no_file, S_IREAD|S_IRGRP|S_IROTH)