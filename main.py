import customtkinter
from tkinter import *
from tkinter import filedialog
import random
import os
import sys
import time
from datetime import date
import code128
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

addrHelps = "7035: Alachua, FL\n\
7033: Apple Valley, CA\n\
7039: Beaver Dam, WI\n\
6094: Bentonville, AR\n\
6011: Brookhaven, MS\n\
6020: Brooksville, FL\n\
6031: Buckeye, AZ\n\
6043: Coldwater, MI\n\
6006: Cullman, AL\n\
6010: Douglas, GA\n\
7038: Ft Pierce, FL\n\
7026: Grantsville, UT\n\
6024: Grove City, OH\n\
6037: Hermiston, OR\n\
6040: Hope Mills, NC\n\
6066: Hopkinsville, KY\n\
6054: La Grange, GA\n\
6019: Loveland, CO\n\
6038: Marcy, NY\n\
6025: Menomonie, WI\n\
6039: Midway, TN\n\
7045: Mt Crawford, VA\n\
6009: Mount Pleasant, IA\n\
6016: New Braunfels, TX\n\
6048: Opelousas, LA\n\
6035: Ottawa, KS\n\
6036: Palestine, TX\n\
6012: Plainview, TX\n\
6021: Porterville, CA\n\
6030: Raymond, NH\n\
6026: Red Bluff, CA\n\
6068: Sanger, TX\n\
7036: Sealy, TX\n\
6018: Searcy, AZ\n\
6017: Seymour, IN\n\
6070: Shelby, NC\n\
7034: Smyrna, DE\n\
6092: Spring Valley, IL\n\
6069: St. James, MO\n\
6023: Sutherland, VA\n\
6080: Tobyhanna, PA\n\
6027: Woodland, PA"

destAddresses = {
		7035: "Alachua, FL",
		7033: "Apple Valley, CA",
		7039: "Beaver Dam, WI",
		6094: "Bentonville, AR",
		6011: "Brookhaven, MS",
		6020: "Brooksville, FL",
		6031: "Buckeye, AZ",
		6043: "Coldwater, MI",
		6006: "Cullman, AL",
		6010: "Douglas, GA",
		7038: "Ft Pierce, FL",
		7026: "Grantsville, UT",
		6024: "Grove City, OH",
		6037: "Hermiston, OR",
		6040: "Hope Mills, NC",
		6066: "Hopkinsville, KY",
		6054: "La Grange, GA",
		6019: "Loveland, CO",
		6038: "Marcy, NY",
		6025: "Menomonie, WI",
		6039: "Midway, TN",
		7045: "Mt Crawford, VA",
		6009: "Mount Pleasant, IA",
		6016: "New Braunfels, TX",
		6048: "Opelousas, LA",
		6035: "Ottawa, KS",
		6036: "Palestine, TX",
		6012: "Plainview, TX",
		6021: "Porterville, CA",
		6030: "Raymond, NH",
		6026: "Red Bluff, CA",
		6068: "Sanger, TX",
		7036: "Sealy, TX",
		6018: "Searcy, AZ",
		6017: "Seymour, IN",
		6070: "Shelby, NC",
		7034: "Smyrna, DE",
		6092: "Spring Valley, IL",
		6069: "St. James, MO",
		6023: "Sutherland, VA",
		6080: "Tobyhanna, PA",
		6027: "Woodland, PA"
				}

destAddress = str(); poNum = str();
step1 = False; step2 = False; single = True

root = customtkinter.CTk()
root.geometry("600x750")
root.title("Label Generator")

def seeFiles():
	filedialog.askopenfilename(initialdir = os.getcwd())

def getDestAddress():
	global step1, destAddress

	try:
		destText.delete(0.0, 100.0)
		dialog = customtkinter.CTkInputDialog(text = "Enter a 4-digit destination Address (i.e. 7033 for Apple Valley)", title = "Enter a 4-digit destination address")

		while not destAddress.isdigit() or len(destAddress) != 4 or destAddresses.get(int(destAddress), "Not Found") == "Not Found":
			try:	
				destAddress = dialog.get_input()
			except Exception as e:
				textbox.delete(0.0, 100.0)
				textbox.insert(index = 0.0, text = "Please write a known four-digit\nnumber!", tags = None)
				return
		textbox.delete(0.0, 100.0)
		destAddress = destAddresses.get(int(destAddress))
		destText.insert(index = 0.0, text = destAddress)
		step1 = True
	except Exception as e:
		quit()

def getPONum():
	global step2, poNum

	try:
		poText.delete(0.0, 100.0)
		dialog = customtkinter.CTkInputDialog(text = "Enter a valid PO number", title = "Enter a PO")
		while not poNum.isdigit():
			try:	
				poNum = dialog.get_input()
			except Exception as e:
				textbox.delete(0.0, 100.0)
				textbox.insert(index = 0.0, text = "Please write a valid PO\nnumber!", tags = None)
				return
		textbox.delete(0.0, 100.0)
		poText.insert(index = 0.0, text = poNum)
		step2 = True
	except Exception as e:
		quit()

def seeAddrs():
	dialog = customtkinter.CTkTextbox(master = frame, width = 200, height = 120)
	dialog.insert(index = 0.0, text = addrHelps)
	dialog.pack(pady = 5)

def mixedFunc():
	global single
	single = not single

def createBarcode(number : str):
	global step1, step2, destAddress, poNum, single

	singleOrMixed = "Single"

	if not step1:
		textbox.delete(0.0, 100.0)
		textbox.insert(index = 0.0, text = "Please generate a four-digit\nnumber first!", tags = None)
		return
	if not step2:
		textbox.delete(0.0, 100.0)
		textbox.insert(index = 0.0, text = "Please generate a PO\nnumber first!", tags = None)
		return

	if not single:
		singleOrMixed = "Mixed"

	fromAddr = "AlfaPet Inc.\n7319 Ingham Ln\nGodfrey, IL 62035"
	toAddr = destAddress

	barcode = code128.image(number, height = 100)
	top_bottom_margin = 70; left_right_margin = 10
	new_height = 400 + (2 * top_bottom_margin)
	new_width = barcode.width + (6 * left_right_margin)
	new_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))

	barcode_y = 100
	new_image.paste(barcode, (left_right_margin + 15, new_height - barcode_y - 40))

	draw = ImageDraw.Draw(new_image)

	h1_size = 26; h2_size = 26; h3_size = 26; footer_size = 26

	h1_font = ImageFont.truetype("arial.ttf", h1_size)
	h2_font = ImageFont.truetype("arial.ttf", h2_size)
	h3_font = ImageFont.truetype("arial.ttf", h3_size)
	footer_font = ImageFont.truetype("arial.ttf", footer_size)

	top_box = "From: " + fromAddr
	line = "_____________________________________________"
	mid_box = "To: " + toAddr + "\nAddress\nZIP Code"
	bot_box = "PO #: " + poNum + "\nDept: 00008\nType: 0033\n" + singleOrMixed
	center_bot_box = (barcode.width / 2) - len(bot_box) * 5
	center_barcode_value = (barcode.width / 2)

	draw.text((new_width / 4.5, 0), top_box, fill = (0, 0, 0), font = h1_font)
	draw.text((0, h1_size * 3), line, fill = (0, 0, 0), font = h2_font)
	draw.text((new_width / 4.5, (h1_size * 2.5 + h2_size + h3_size)), mid_box, fill = (0, 0, 0), font = h3_font)
	draw.text((0, h1_size * 7), line, fill = (0, 0, 0), font = h2_font)
	draw.text((new_width / 4.5, (h1_size  * 4 + h2_size + h3_size * 3 + 15)), bot_box, fill = (0, 0, 0), font = footer_font)
	draw.text((0, h1_size * 13), line, fill = (0, 0, 0), font = h2_font)
	draw.text((center_barcode_value / 1.5, (new_height - footer_size - 10)), number, fill = (0, 0, 0), font = h2_font)

	Path(".\\barcodes").mkdir(parents = True, exist_ok = True)
	new_image.save(".\\barcodes\\" + number + "_barcode.png", "PNG")
	step1 = False
	step2 = False
	poText.delete(0.0, 100.0)
	destText.delete(0.0, 100.0)

def generateNumber():

	numList = []; min = 1000000001; max = 9999999999
	try:
		file = open("numberlog.txt", "r+")
		for line in file:
			line = line[line.index(">") + 2:].rstrip()
			numList.append(line)
		file.close()
	except Exception as e:
		file = open("numberlog.txt", "a+")
		file.close()

	num = random.randrange(min, max)
	checkNum = "00070614" + str(num)

	if len(numList) >= max:
		quit()
	if checkNum in numList:
		textbox.delete(0.0, 100.0)
		textbox.insert(index = 0.0, text = "Duplicate number created, try again.", tags = None)
		return

	file = open("numberlog.txt", "a+")
	file.write(str(time.ctime(time.time())) + " -> " + checkNum + "\n")

	textbox.delete(0.0, 100.0)
	textbox.insert(index = 0.0, text = checkNum, tags = None)
	createBarcode(checkNum)

frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 12, padx = 10, fill = "both", expand = True)

fileExplorer = customtkinter.CTkLabel(master = frame, text = "Label Generator", font = ("Arial", 48))
fileExplorer.pack(pady = 2, padx = 10)

label = customtkinter.CTkLabel(master = frame, text = "©AlfaPet Inc.")
label.pack(pady = 2, padx = 10)

button = customtkinter.CTkButton(master = frame, text = "Enter 4-digit Address", command = getDestAddress)
button.pack(pady = 10, padx = 0.5)

destText = customtkinter.CTkTextbox(master = frame, width = 140, height = 25)
destText.pack()

button = customtkinter.CTkButton(master = frame, text = "Enter PO Number", command = getPONum)
button.pack(pady = 10, padx = 0.5)

poText = customtkinter.CTkTextbox(master = frame, width = 140, height = 25)
poText.pack()

checkbox = customtkinter.CTkCheckBox(master = frame, text = "Mixed? (only check if mixed)", command = mixedFunc,
                                     onvalue="on", offvalue="off")
checkbox.pack(padx=20, pady=10)

entry = customtkinter.CTkLabel(master = frame, text = "SSCC-18 Number:")
entry.pack()

textbox = customtkinter.CTkTextbox(master = frame, width = 200, height = 50)
textbox.pack(pady = 5, padx = 5)

button = customtkinter.CTkButton(master = frame, text = "Generate Label!", command = generateNumber)
button.pack(pady = 25, padx = 10)

label = customtkinter.CTkLabel(master = frame, text = "See folder containing all generated barcodes below")
label.pack(pady = 2, padx = 2)

button = customtkinter.CTkButton(master = frame, text = "See barcodes", command = seeFiles)
button.pack(pady = 2, padx = 2)

helper = customtkinter.CTkButton(master = frame, text = "See 4-digit addresses here", command = seeAddrs)
helper.pack(pady = 20, padx = 0)

root.mainloop()