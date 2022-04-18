import time
import requests

TE_API_URL = 'https://api-my.te.eg/api/'
API_GEN_TOKEN = f'{TE_API_URL}user/generatetoken?channelId=WEB_APP'
API_LOGIN = f'{TE_API_URL}user/login?channelId=WEB_APP'
API_LINE_USAGE = f'{TE_API_URL}line/freeunitusage'

class User:
  def __init__(self, pw, msisdn):
    self.pw = pw
    self.msisdn = msisdn
    self.s = requests.session()
    self.header = {
      'customerId': None,
      'msisdn': msisdn,
      'locale': 'en',
      'timestamp': None,
    }
    self.body = {}
    self.jwt = None

  def generate_jwt(self):
    '''
      Generate default JWT token for login
    '''
    r = self.s.get(API_GEN_TOKEN)
    body = r.json()['body']
    if 'jwt' in body:
      return body['jwt']

  def login(self):
    timestamp = int(time.time())
    jwt = self.generate_jwt()
    # preflight
    self.s.options(API_LOGIN)
    # send request
    req = {
      'header': self.header,
      'body': {
        'password': self.pw
      }
    }
    req['header']['timestamp'] = timestamp
    res = self.s.post(API_LOGIN, json=req, headers={'Jwt': jwt})
    res_json = res.json()
    # we are OK and no session error
    if res_json['header']['responseCode'] == '0':
      res_json = res.json()
      self.jwt = res_json['body']['jwt']
      self.header['customerId'] = res_json['header']['customerId']
      return 'OK'
    else:
      print('ERR')
      return res

  def get_usage(self):
    res = self.s.post(API_LINE_USAGE, json={'header': self.header}, headers={'Jwt': self.jwt})
    res_json = res.json()
    detailed_usage = res_json['body']['detailedLineUsageList']
    return detailed_usage

  def print_report(self):
    if not self.jwt:
      self.login()
    usage = self.get_usage()
    for i in range(len(usage)):
      print(f'''{usage[i]['usedAmount']}/{usage[i]['initialTotalAmount']}{usage[i]['measureUnitEnName']}\t{usage[i]['itemCode']}''')

  def get_full_usage(self):
    '''
    get full usage (calcaulate all available packages)
    return total_amount, total_used
    '''
    if not self.jwt:
      self.login()
    usage = self.get_usage()
    total_amount = 0
    total_used = 0
    for i in range(len(usage)):
      total_amount = total_amount + usage[i]['initialTotalAmount']
      total_used = total_used + usage[i]['usedAmount']
    return total_amount, total_used
