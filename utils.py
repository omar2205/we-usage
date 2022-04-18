from base64 import b64encode
from binascii import unhexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_pw(password: str) -> str:
  if password == 'NO_PW':
    return 'NO_PW'

  # from https://my.te.eg/assets/config/config.json
  iv = '000102030405060708090a0b0c0d0e0f'
  k = '0f0e0d0c0b0a09080706050403020100'

  # prepare the encryption components
  iv = unhexlify(iv)
  k = unhexlify(k)
  pw = pad(password.encode(), AES.block_size)
  
  cipher = AES.new(k, AES.MODE_CBC, iv)

  encrypted_password = cipher.encrypt(pw)

  return b64encode(encrypted_password).decode('utf-8')
