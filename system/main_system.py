from pyfiglet import Figlet
from Data_Show_sys import *
from clawler_sys import *
from DataAnalysis_sys import *


def sys_init():
    Logo=Figlet()
    Logo_text=Logo.renderText('BJTUAtt')
    print(Logo_text,end='')
    print("初始化...",end='\n')

def menu():
    pass

def main_sys():
    pass

def main():
    sys_init()
    clawler_menu()

if __name__=='__main__':
    main()