@echo off

uv run pyinstaller ^
    --onefile ^
    --noconsole ^
    --icon=favicon.ico ^
    --add-data "driver;driver" ^
    --add-data "favicon.ico;." ^
    --name "Printer Installer" ^
    main.py

uv run pyinstaller ^
    --onefile ^
    --icon=favicon.ico ^
    --add-data "driver;driver" ^
    --add-data "favicon.ico;." ^
    --name "Printer Installer (Debug)" ^
    main.py