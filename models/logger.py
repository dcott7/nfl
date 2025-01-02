import sys
from colorama import Fore, Style
import datetime

class Logger:
    @staticmethod
    def _timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def info(message: str):
        print(f"{Fore.BLUE}[INFO] {Logger._timestamp()}{Style.RESET_ALL} {message}")
    
    @staticmethod
    def warning(message: str):
        print(f"{Fore.YELLOW}[WARNING] {Logger._timestamp()}{Style.RESET_ALL} {message}")
    
    @staticmethod
    def error(message: str):
        print(f"{Fore.RED}[ERROR] {Logger._timestamp()}{Style.RESET_ALL} {message}", file=sys.stderr)
