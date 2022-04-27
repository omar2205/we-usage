#!/usr/bin/python3
from dotenv import load_dotenv
load_dotenv() # load from .env file
import os
import sys
from utils import encrypt_pw
from user import User

PW = encrypt_pw(os.environ.get('WE_PW', 'NO_PW'))
MSISDN = os.environ.get('WE_MSISDN')

if PW == 'NO_PW':
  print('Make sure that your password is correct')
  exit(1)

def main():
  u = User(PW, MSISDN)
  try:
    if sys.argv[1] == 'report':
      u.print_report()
      return
  except:
    pass
#  u.print_report()
  amount, used = u.get_full_usage()
  print(f'{used}/{amount}')

if __name__ == '__main__':
  main()

