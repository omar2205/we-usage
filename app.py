from dotenv import load_dotenv
load_dotenv() # load from .env file
import os
from utils import encrypt_pw
from user import User

PW = encrypt_pw(os.environ.get('WE_PW', 'NO_PW'))
MSISDN = os.environ.get('WE_MSISDN')

if PW == 'NO_PW':
  print('Make sure that your password is correct')
  exit(1)

u = User(PW, MSISDN)
