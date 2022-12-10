import customtkinter
from tkinter import *
from tkinter import filedialog
import random
import os
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("700x550")
root.title("Random Number Generator")

def seeFiles():
	filedialog.askopenfilename(initialdir = os.getcwd())

def generateNumber():

	numList = []; min = 0; max = 1000000000000000000
	try:
		file = open("numberlog.txt", "r+")
		for line in file:
			line = line[line.index(">") + 2:].rstrip()
			numList.append(line)
		file.close()
	except Exception as e:
		file = open("numberlog.txt", "a+")
		file.close()

	for item in numList:
		print(item)
	num = random.randrange(min, max)
	checkNum = str(num)

	if len(numList) >= max:
		quit()
	if checkNum in numList:
		textbox.delete(0.0, 100.0)
		textbox.insert(index = 0.0, text = "Duplicate number created, try again.", tags = None)
		return

	file = open("numberlog.txt", "a+")
	file.write(str(time.ctime(time.time())) + " -> " + str(num) + "\n")

	textbox.delete(0.0, 100.0)
	textbox.insert(index = 0.0, text = str(num), tags = None)

frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 12, padx = 10, fill = "both", expand = True)

fileExplorer = customtkinter.CTkLabel(master = frame, text = "Number Generator", font = ("Arial", 48))
fileExplorer.pack(pady = 2, padx = 10)

label = customtkinter.CTkLabel(master = frame, text = "Made By Adam Johnes\n ©AlfaPet Inc.")
label.pack(pady = 2, padx = 10)

button = customtkinter.CTkButton(master = frame, text = "Generate Number!", command = generateNumber)
button.pack(pady = 12, padx = 10)

textbox = customtkinter.CTkTextbox(master = frame, width = 230, height = 100)
textbox.pack(pady = 5, padx = 5)

label = customtkinter.CTkLabel(master = frame, text = "See file containing all generated numbers below")
label.pack(pady = 2, padx = 2)

button = customtkinter.CTkButton(master = frame, text = "See numberlog.txt", command = seeFiles)
button.pack(pady = 2, padx = 2)

label = customtkinter.CTkLabel(master = frame, text = "(you may have to right-click on numberlog.txt and select 'open')")
label.pack(pady = 20, padx = 2)

root.mainloop()