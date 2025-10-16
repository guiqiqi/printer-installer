import sys
import logging

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

BasePath = sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.'  # type: ignore