#type: ignore

from __future__ import annotations

import win32com.client
import win32print
import pywintypes

import re
import typing as t
from dataclasses import dataclass

from log import logger


PRINTER_NAME = 'pPrinterName'
PRINTER_PORT_NAME = 'pPortName'
PRINTER_COMMENT_NAME = 'pComment'
PRINTER_DRIVER_NAME = 'pDriverName'
PRINTER_SERVER_NAME = 'pServerName'
PRINTER_SHARE_NAME = 'pShareName'
PRINTER_LOCATION_NAME = 'pLocation'
PRINTER_PROCESSOR_NAME = 'pPrintProcessor'
PRINTER_DATATYPE_NAME = 'pDatatype'
PRINTER_DEVMODE_NAME = 'pDevMode'
PRINTER_SECURITY_NAME = 'pSecurityDescriptor'
PRINTER_SEPFILE_NAME = 'pSepFile'
PRINTER_PARAS_NAME = 'pParameters'
PRINTER_ATTRE_NAME = 'Attributes'
PRINTER_PRIORITY_NAME = 'Priority'
PRINTER_PRIORITY_DEFAULT_NAME = 'DefaultPriority'
PRINTER_START_TIME_NAME = 'StartTime'
PRINTER_END_TIME_NAME = 'UntilTime'
PRINTER_STATUS_NAME = 'Status'
PRINTER_JOBS_NAME = 'cJobs'
PRINTER_PPM_NAME = 'AveragePPM'

PRINTER_DEFAULT_DATATYPE = 'RAW'
PRINTER_DEFAULT_PROCESSOR = 'winprint'

IPV4_REGEX_PATTERN = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'


@dataclass
class PortCreationError(Exception):
    error_msg: str


@dataclass
class PrinterAlreadyExist(Exception):
    ...


@dataclass
class Printer:
    ip: str
    name: str
    description: str
    driver: str

    @classmethod
    def list_current_installed(cls) -> t.Iterator[Printer]:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        for _flags, description, name, _comment in printers:
            info = win32print.GetPrinter(win32print.OpenPrinter(name), 2)
            logger.debug(f'printer info: {info}')
            ips = re.findall(IPV4_REGEX_PATTERN, info[PRINTER_PORT_NAME] + info[PRINTER_LOCATION_NAME])
            yield cls(
                ip=ips[0] if ips else '', 
                name=name, 
                description=description,
                driver=info[PRINTER_DRIVER_NAME]
            )

    @staticmethod
    def _create_port(name: str, address: str, protocol: t.Literal[1, 2] = 1) -> None:
        wmi = win32com.client.GetObject('winmgmts:')
        port = wmi.Get('Win32_TCPIPPrinterPort').SpawnInstance_()
        port.Name = name
        port.Protocol = protocol
        port.HostAddress = address
        port.SNMPEnabled = False
        port.Put_()
        logger.debug(f'created port: name={name}, addr={address}, protocol={protocol}')

        ports = wmi.ExecQuery(f"SELECT * FROM Win32_TCPIPPrinterPort WHERE Name = '{name}'")
        if len(list(ports)) > 0:
            return
        
        logger.warning(f'created but not found port: name={name}, addr={address}, protocol={protocol}')
        raise PortCreationError(error_msg=f'port {name} creation failed')

    def install(self) -> None:
        # Check if printer already exists
        try:
            hprinter = win32print.OpenPrinter(self.name)
            win32print.ClosePrinter(hprinter)
        except pywintypes.error:
            ...
        else:
            logger.warning(f'target printer already installed: {self.name}')
            raise PrinterAlreadyExist()

        # Add port
        self._create_port(self.ip, self.ip)

        # Add printer
        logger.debug(f'starting create printer: {self.name}, port={self.ip}, driver={self.driver}')
        win32print.AddPrinter(None, 2, {
            PRINTER_SERVER_NAME: None,
            PRINTER_NAME: self.name,
            PRINTER_SHARE_NAME: '',
            PRINTER_PORT_NAME: self.ip,
            PRINTER_DRIVER_NAME: self.driver,
            PRINTER_COMMENT_NAME: self.description,
            PRINTER_LOCATION_NAME: '',
            PRINTER_DEVMODE_NAME: pywintypes.DEVMODEType(),
            PRINTER_SEPFILE_NAME: '',
            PRINTER_PROCESSOR_NAME: PRINTER_DEFAULT_PROCESSOR,
            PRINTER_DATATYPE_NAME: PRINTER_DEFAULT_DATATYPE,
            PRINTER_PARAS_NAME: '',
            PRINTER_SECURITY_NAME: None,
            PRINTER_ATTRE_NAME: 0,
            PRINTER_PRIORITY_NAME: 1,
            PRINTER_PRIORITY_DEFAULT_NAME: 0,
            PRINTER_START_TIME_NAME: 0,
            PRINTER_END_TIME_NAME: 0,
            PRINTER_STATUS_NAME: 0,
            PRINTER_JOBS_NAME: 0,
            PRINTER_PPM_NAME: 0
        })


if __name__ == '__main__':
    for printer in Printer.list_current_installed():
        print(printer)
