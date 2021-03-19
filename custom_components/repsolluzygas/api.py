import json
import logging
import requests
import datetime

BASE_URL = 'https://tuoficinaonline.repsolluzygas.com/api'
DEFAULT_HEADERS = {
  'Market-Type': 'ML',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

class RepsolLYGAPI():
  def __init__(self, username, password, access_token=None, refresh_token=None, obtain_at=None, expires_in=None):
    self._username = username
    self._password = password

    self._access_token = access_token
    self._refresh_token = refresh_token
    self._obtain_at = obtain_at
    self._expires_in = expires_in
    self._expires_at = None

    if (not self._access_token) or self.tokenHasExpired():
      self.login()

  def login(self):
    login_url = '{BASE_URL}/auth/access'.format(BASE_URL=BASE_URL)
    login_data = {
      'username': self._username,
      'password': self._password
    }

    login_headers = {'content-type': 'application/json'}
    login_headers.update(DEFAULT_HEADERS)

    response = requests.post(login_url, json=login_data, headers=DEFAULT_HEADERS)
    response_json = response.json()

    self._access_token = response_json['data']['access_token']
    self._refresh_token = response_json['data']['refresh_token']
    self._obtain_at = response_json['data']['obtain_at']
    self._expires_in = response_json['data']['expires_in']
    self._expires_at = datetime.datetime.fromtimestamp((self._obtain_at + self._expires_in) / 1000)

  def retrieveContracts(self):
    if self.tokenHasExpired():
      self.login()

    request_url = '{BASE_URL}/contract'.format(BASE_URL=BASE_URL)
    request_headers = {'X-Smart-Token': self._access_token}
    request_headers.update(DEFAULT_HEADERS)

    response = requests.get(request_url, headers=request_headers)
    return response.json()['data']

  def retrieveConsumptionFromContract(self, contract_id):
    if self.tokenHasExpired():
      self.login()

    request_url = '{BASE_URL}/contract/{contract_id}/consumption/acummulated'.format(BASE_URL=BASE_URL, contract_id=contract_id)
    request_headers = {'X-Smart-Token': self._access_token}
    request_headers.update(DEFAULT_HEADERS)

    response = requests.get(request_url, headers=request_headers)

    if response.status_code is not 200:
      return

    return response.json()['data']

  def retrieveLastInvoiceFromContract(self, contract_id):
    if self.tokenHasExpired():
      self.login()

    request_url = '{BASE_URL}/contract/{contract_id}/invoice'.format(BASE_URL=BASE_URL, contract_id=contract_id)
    request_headers = {'X-Smart-Token': self._access_token}
    request_headers.update(DEFAULT_HEADERS)
    request_params = {'items': 1}

    response = requests.get(request_url, params=request_params, headers=request_headers)
    response_json = response.json()
    return response_json['data'][0]

  def retrieveInvoiceData(self, contract_id, invoice_id):
    if self.tokenHasExpired():
      self.login()

    request_url = '{BASE_URL}/contract/{contract_id}/invoice/{invoice_id}'.format(
      BASE_URL=BASE_URL,
      contract_id=contract_id,
      invoice_id=invoice_id
    )
    request_headers = {'X-Smart-Token': self._access_token}
    request_headers.update(DEFAULT_HEADERS)

    response = requests.get(request_url, headers=request_headers)
    response_json = response.json()
    return response_json['data']

  def tokenHasExpired(self):
    return datetime.datetime.now() > self._expires_at
