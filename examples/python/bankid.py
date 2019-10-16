import sys
import time, threading
import base64
import tempfile
import requests
import OpenSSL.crypto
import contextlib
import urllib3
import json

urllib3.disable_warnings()

CONFIGS = {
    'prod': {
        'mobileBankIdPolicy': '1.2.752.78.1.5',
        'bankIdUrl': 'https://appapi2.bankid.com/rp/v5',
        'pfx': 'YOUR PRODUCTION CERT INFO GOES HERE',
        'passphrase': 'YOUR PRODUCTION CERT INFO GOES HERE',
        'ca': './cert/test.ca'
    },
    'test': {
        'mobileBankIdPolicy': '1.2.3.4.25',
        'bankIdUrl': 'https://appapi2.test.bankid.com/rp/v5',
        'pfx': './cert/FPTestcert2_20150818_102329.pfx',
        'passphrase': 'qwerty123',
        'ca': './cert/test.ca'
    }
}

config = CONFIGS['test']

@contextlib.contextmanager
def pfx_to_pem(pfx_path, pfx_password):
    ''' Decrypts the .pfx file to be used with requests. '''
    with tempfile.NamedTemporaryFile(suffix='.pem') as t_pem:
        f_pem = open(t_pem.name, 'wb')
        pfx = open(pfx_path, 'rb').read()
        p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
        f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
        f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
        ca = p12.get_ca_certificates()
        if ca is not None:
            for cert in ca:
                f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        f_pem.close()
        yield t_pem.name

class SetInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target = self.__set_interval)
        thread.start()

    def __set_interval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()) :
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def call(method, params):
    with pfx_to_pem(config['pfx'], config['passphrase']) as cert:
        r = requests.post(config['bankIdUrl'] + '/' + method, cert=cert, json=params, verify=config['ca'])

    return r.json()

def auth(pnr, end_user_ip, other_device = False) :
    requirement = {
        'allowFingerprint': True,
    }
    if other_device:
        requirement['certificatePolicies'] = [config['mobileBankIdPolicy']]

    return call('auth', {
        'endUserIp': end_user_ip,
        'personalNumber': pnr,
        'requirement': requirement
    })

def sign(pnr, end_user_ip, text, other_device = False):
    requirement = {
        'allowFingerprint': True,
    }
    if other_device:
        requirement['certificatePolicies'] = [config['mobileBankIdPolicy']]

    return call('sign', {
        'endUserIp': end_user_ip,
        'personalNumber': pnr,
        'userVisibleData': base64.b64encode(text.encode()).decode(),
        'requirement': requirement
    })

def collect(order_ref):
    return call('collect', {
        'orderRef': order_ref
    })

def cancel(order_ref):
    return call('cancel', {
        'orderRef': order_ref
    })

def launch_urls(auto_start_token):
    launch_params = '/?autostarttoken=[' + auto_start_token + ']&redirect=null'
    return {
      'url': 'bankid://' + launch_params,
      'iosUrl': 'https://app.bankid.com' + launch_params,
    }

def persist_result(bank_id_result):
    # FIXME - YOU MUST STORE:
    #   bank_id_result.signature
    #   bank_id_result.user
    #   bank_id_result.ocspResponse
    pass

def auth_flow(pnr, end_user_ip, launch_fn):
    r = auth(pnr, end_user_ip)
    if not 'autoStartToken' in r or not 'orderRef' in r:
        print(r)
        raise ValueError('Auth request failed')

    auto_start_token = r['autoStartToken']
    order_ref = r['orderRef']

    if launch_fn:
        urls = launch_urls(auto_start_token)
        launch_fn({
            'url': urls['url'],
            'iosUrl': urls['iosUrl'],
            'orderRef': order_ref
        })

    def poll():
        r = collect(order_ref)
        if r['status'] == 'failed':
            interval.cancel()
            print('Authorization failed')
            print(r['hintCode'])
        elif r['status'] == 'complete':
            interval.cancel()
            persist_result(r)
            print('Authorization successful')
            print(r['completionData']['user'])
            print(r['completionData']['device'])
        else:
            print(r['hintCode'])

    interval = SetInterval(2, poll)

def sign_flow(pnr, end_user_ip, text, launch_fn):
    r = sign(pnr, end_user_ip, text)
    if not 'autoStartToken' in r or not 'orderRef' in r:
        print(r)
        raise ValueError('Sign request failed')

    auto_start_token = r['autoStartToken']
    order_ref = r['orderRef']

    if launch_fn:
        urls = launch_urls(auto_start_token)
        launch_fn({
            'url': urls['url'],
            'iosUrl': urls['iosUrl'],
            'orderRef': order_ref
        })

    def poll():
        r = collect(order_ref)
        if r['status'] == 'failed':
            interval.cancel()
            print('Signing failed')
            print(r['hintCode'])
        elif r['status'] == 'complete':
            interval.cancel()
            persist_result(r)
            print('Signing successful')
            print(r['completionData']['user'])
            print(r['completionData']['device'])
        else:
            print(r['hintCode'])

    interval = SetInterval(2, poll)

def usage():
    print('Usage: %s [operation] [param]' % sys.argv[0])
    print('       operation can be one of (auth, sign, cancel)')
    print('       for auth and sign, param must be a Swedish personnummer')
    print('       for cancel, param must be an orderRef previously started by auth or sign')
    sys.exit()

if len(sys.argv) < 3:
    usage()

operation = sys.argv[1]
if operation not in ['auth', 'sign', 'cancel']:
    usage()

pnr_or_order_ref = sys.argv[2]

launch_native_app = lambda launch_info: print('TODO: Launch native app ' + json.dumps(launch_info))

try:
    if operation == 'auth':
        auth_flow(pnr_or_order_ref, '123.123.123.123', launch_native_app)
    elif operation == 'sign':
        sign_flow(pnr_or_order_ref, '123.123.123.123', 'Test text for signing', launch_native_app)
    elif operation == 'cancel':
        cancel(pnr_or_order_ref)
except ValueError as e:
    print(e)
