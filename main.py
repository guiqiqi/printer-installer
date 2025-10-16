from installer import DriverInstaller
from printer import Printer, PrinterAlreadyExist
from ui import (
    Root, 
    SelectedPrinter,
    DriverInstallButton, 
    AddPrinterButton,
    PrinterDropdown, 
    IntroLabel
)
from log import logger, BasePath

import os
import sys
import ctypes
from tkinter import messagebox

# NOTE: all printers add to one printer group should have same printer driver name !!!
Printers = [
    Printer('10.56.92.134', 'Color Printer Sales', 'Color printer in Sales Zone', 'EPSON WF-C579R Series'),
    Printer('10.56.92.135', 'B&W Printer AIoT', 'Black and White printer in Zone Reception', 'EPSON WF-C579R Series'),
    Printer('10.56.92.136', 'B&W Printer Management', 'Black and White printer in Zone Management', 'EPSON WF-C579R Series')
]


class Main:
    
    DriverFolder = os.path.join(BasePath, 'driver')
    logger.debug(f'base path of program: {BasePath}')

    def __init__(self) -> None:
        PrinterDropdown['values'] = [p.name for p in Printers]
        PrinterDropdown.bind('<<ComboboxSelected>>', self._select_printer)
        SelectedPrinter.set(Printers[0].name)
        IntroLabel.config(text=Printers[0].description)

        self._process_busy = False
        self._printer_maps = {
            p.name: p for p in Printers
        }

        DriverInstallButton.bind('<Button-1>', self._install_driver)
        AddPrinterButton.bind('<Button-1>', self._add_printer)

        self._driver_name = Printers[0].driver
        assert all(printer.driver == self._driver_name for printer in Printers)

    def _select_printer(self, _e) -> None:
        selected_printer = SelectedPrinter.get()
        IntroLabel.config(text=self._printer_maps[selected_printer].description)

    def _install_driver(self, _e) -> None:
        DriverInstallButton.config(state='disabled')
        try:
            messagebox.showinfo('Driver Installation', 'Start driver installation, it may need a while, UI may not responding during this time')
            installer = DriverInstaller(self.DriverFolder, self._driver_name)
            installer.install()
        except Exception:
            messagebox.showerror('Driver Installation', 'Driver install failed. Please contact admin')
        else:
            messagebox.showinfo('Driver Installation', 'Driver installed successfully')
        DriverInstallButton.config(state='normal')

    def _add_printer(self, _e) -> None:
        if self._process_busy:
            return
        self._process_busy = True

        selected_printer = SelectedPrinter.get()
        printer = self._printer_maps[selected_printer]
        AddPrinterButton.config(state='disabled')
        try:
            printer.install()
        except PrinterAlreadyExist:
            messagebox.showwarning('Notice', f'Selected printer {printer.name} has already in your system')
        except Exception as e:
            logger.error(f'insatll printer {printer} failed: {e}')
            messagebox.showerror('Failed', f'Printer {printer.name} installed failed. Please contact admin')
        else:
            messagebox.showinfo('Success', f'Printer {printer.name} installed successfully')
        AddPrinterButton.config(state='normal')
        self._process_busy = False

    def run(self) -> None:
        Root.mainloop()


if __name__ == '__main__':
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            raise RuntimeError
    except:
        messagebox.showerror('Error', 'Please run program with Administrator')
        sys.exit(1)
    if 'nt' not in os.name:
        messagebox.showerror('Error', 'Installer can only been run in Windows platform')
    Main().run()