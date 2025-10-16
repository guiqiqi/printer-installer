import tkinter as tk
from tkinter import ttk
from os import path

from log import BasePath


# Create the main window
root = tk.Tk()
root.title("Printer Setup")
root.geometry("400x260")
root.resizable(False, False)
root.iconbitmap(path.join(BasePath, 'favicon.ico'))

# Label for driver installation question
driver_label = tk.Label(root, text='Not sure if you installed driver?')
driver_label.pack(pady=10)

# Button for installing driver
install_button = tk.Button(root, text='Install driver')
install_button.pack(pady=5)

# Label for selecting printer
printer_select_label = tk.Label(root, text='Select which printer you want to use')
printer_select_label.pack(pady=10)

# Dropdown menu for printer names
printer_var = tk.StringVar()
printer_dropdown = ttk.Combobox(root, textvariable=printer_var, state='readonly')
printer_dropdown.pack(pady=5)
printer_dropdown.set("Printer Name")  # Default text

# Label for printer introduction
intro_label = tk.Label(root, wraplength=350)
intro_label.pack(pady=10)

# Install printer button
add_printer_button = tk.Button(root, text='Add printer')
add_printer_button.pack(pady=5)

Root = root
PrinterDropdown = printer_dropdown
DriverInstallButton = install_button
IntroLabel = intro_label
SelectedPrinter = printer_var
AddPrinterButton = add_printer_button
