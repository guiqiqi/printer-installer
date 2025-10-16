## Printer Setup Helper

Don't want to manually install drivers and add printers anymore? Is the process too tedious and time-consuming? Then try this tool!

It automatically installs the necessary drivers and adds printers.

Only Windows platform supported.

### Usage

To use: Right-click and open the app with administrator privileges. Install the driver and select the printer you want to add.

### For Developer

If you want to make your distibution of this helper, check following list:

- If your printer support TCP/IP in raw mode?
- If you know your printer IP address?
- If you know which `.inf` drivers are required to install?

If so, replace `driver` folder with your driver files, and change printer info in `main.py`, run `build.bat`, then you got your printer setup helper!

Have a nice day!