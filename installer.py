import typing as t

import subprocess
from os import path, chdir
from pathlib import Path
from dataclasses import dataclass

from log import logger


@dataclass
class DriverInstallError(Exception):
    error_msg: str


class DriverInstaller:

    def __init__(self, directory: str, name: str) -> None:
        self.directory = Path(path.abspath(directory))
        self.name = name

    @staticmethod
    def _driver_files(directory: Path, suffix: str = 'inf') -> t.Iterator[Path]:
        for inf_file in directory.rglob(f'*.{suffix}'):
            yield inf_file

    @staticmethod
    def _install_inf_driver(driver: Path) -> None:
        # Enetering driver path
        dirpath = path.dirname(path.abspath(driver))
        chdir(dirpath)

        logger.debug(f'installing driver: {driver}')

        # Run installer
        result = subprocess.run(
            ['pnputil', '/add-driver', str(driver), '/install'],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            logger.debug(f'installed driver: {result.stdout.strip()}')
            return

        logger.error(
            f'installing driver failed: {result.stderr.strip()}, {result.stdout.strip()}')
        raise DriverInstallError(error_msg=result.stderr.strip())

    @staticmethod
    def _add_printer_driver(driver: Path, name: str) -> None:
        # Get abspath of driver
        driver_path = path.abspath(driver)

        # Run printer driver adding process
        logger.debug('trying to add printer driver: {driver_path}, {name}')
        subprocess.run(
            ['printui.exe', '/ia', '/m', name, '/f', driver_path, '/q'],
            text=True,
            shell=True
        )

        # Process above sometimes fails, beacuase we dont know which inf file indicates
        # the main driver package, so the result should be ignored.

    def install(self) -> None:
        for inf_file in self._driver_files(self.directory):
            try:
                self._install_inf_driver(inf_file)
                self._add_printer_driver(inf_file, self.name)
            except DriverInstallError as e:
                logger.error(msg=str(e))
                raise
