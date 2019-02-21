const axiosLib = require('axios');
const fs = require('fs');
const https = require('https');
const to = require('await-to-js').to;

const configs = {
  prod: {
    mobileBankIdPolicy: '1.2.752.78.1.5',
    bankdIdUrl: 'https://appapi2.bankid.com/rp/v5',
    pfx: 'YOUR PRODUCTION CERT INFO GOES HERE',
    passphrase: 'YOUR PRODUCTION CERT INFO GOES HERE',
    ca: fs.readFileSync(`./cert/prod.ca`),
  },
  test: {
    mobileBankIdPolicy: '1.2.3.4.25',
    bankdIdUrl: 'https://appapi2.test.bankid.com/rp/v5',
    pfx: fs.readFileSync('./cert/FPTestcert2_20150818_102329.pfx'),
    passphrase: 'qwerty123',
    ca: fs.readFileSync(`./cert/test.ca`),
  }
};

const config = configs.test;

// Create an axios instance that's configured to use the appropriate
// certificates and always send the required headers
const axios = axiosLib.create({
  httpsAgent: new https.Agent({
    pfx: config.pfx,
    passphrase: config.passphrase,
    ca: config.ca,
  }),
  headers: {
    'Content-Type': 'application/json',
  },
});

// This is a wrapper that will be used for all calls to BankID
async function call (method, params) {
  const [error, result] = await to(
    axios.post(`${config.bankdIdUrl}/${method}`, params));

  if (error) {
    // You will want to implement your own error handling here
    console.error('Error in call');
    if (error.response && error.response.data && error.response.data.errorCode === 'alreadyInProgress') {
      console.error(error.response.data);
      console.error('You would have had to call cancel on this orderRef before retrying');
      console.error('The order should now have been automatically cancelled by this premature retry');
    }
    return {error};
  }

  return result.data;
}

// BankID method call auth
const auth = async (personalNumber, endUserIp, otherDevice) =>
  await call('auth', {
    endUserIp,
    personalNumber,
    requirement: {
      allowFingerprint: true,
      ...otherDevice ? {certificatePolicies: [
        mobileBankIdPolicy,
      ]} : {},
    },
  });

// BankID method call sign
const sign = async (personalNumber, text, endUserIp, otherDevice) =>
  await call('sign', {
    endUserIp,
    personalNumber,
    userVisibleData: Buffer.from(text).toString('base64'),
    requirement: {
      allowFingerprint: true,
      ...otherDevice ? {certificatePolicies: [
        '1.2.752.78.1.5'
      ]} : {},
    },
  });

// BankID method call collect
const collect = async orderRef => await call('collect', {orderRef});

// BankID method call cancel
const cancel = async orderRef => await call('cancel', {orderRef});

// Returns the appropriate urls to launch the native client on mobile devices
// Note that all non-iOS devices should use `url`, while iOS has its own url
const launchUrls = autoStartToken =>
  (launchParams => ({
      url: `bankid://${launchParams}`,
      iosUrl: `https://app.bankid.com${launchParams}`,
    })
  )(`/?autostarttoken=[${autoStartToken}]&redirect=null`);

const persistResult = bankIdResult => 
  // FIXME - YOU MUST STORE:
  //   bankIdResult.signature
  //   bankIdResult.user
  //   bankIdResult.ocspResponse
  true;

const authFlow = async (pnr, endUserIp, launchFn) =>
  new Promise(async (resolve, reject) => {
    const {autoStartToken, orderRef} = await auth(pnr, endUserIp);
    if (!autoStartToken || !orderRef) {
      reject(new Error('Auth request failed'));
      return;
    }

    launchFn && launchFn({...launchUrls(autoStartToken), orderRef});
  
    const interval = setInterval(async () => {
      const {status, hintCode, completionData} = await collect(orderRef);
      if (status === 'failed') {
        clearInterval(interval);
        resolve({ok: false, status: hintCode});
      } else if (status === 'complete') {
        clearInterval(interval);
        resolve({ok: true, status: completionData});
        persistResult(completionData);
      } else {
        console.log(hintCode);
      }
    }, 2000);
  });

const signFlow = async (pnr, endUserIp, text, launchFn) =>
  new Promise(async (resolve, reject) => {
    const {autoStartToken, orderRef} = await sign(pnr, endUserIp, text);
    if (!autoStartToken || !orderRef) {
      reject(new Error('Sign request failed'));
      return;
    }

    launchFn && launchFn({...launchUrls(autoStartToken), orderRef});
  
    const interval = setInterval(async () => {
      const {status, hintCode, completionData} = await collect(orderRef);
      if (status === 'failed') {
        clearInterval(interval);
        resolve({ok: false, status: hintCode});
      } else if (status === 'complete') {
        clearInterval(interval);
        resolve({ok: true, status: completionData});
        persistResult(completionData);
      } else {
        console.log(hintCode);
      }
    }, 2000);
  });

const runningAsScript = !module.parent;

if (runningAsScript) {
  function usage () {
    console.log('Usage: bankid [operation] [param]');
    console.log('       operation can be one of (auth, sign, cancel)');
    console.log('       for auth and sign, param must be a Swedish personnummer');
    console.log('       for cancel, param must be an orderRef previously started by auth or sign');
  }

  if (process.argv.length < 4) {
    usage();
    process.exit(1);
  }

  const operation = process.argv[2];
  const param = process.argv[3];

  function launchNativeApp ({url, iosUrl, orderRef}) {
    console.log(`Flow started with orderRef ${orderRef}`);
    console.log(`FIXME: launch native app on ${url} or ${iosUrl}`);
  }

  const dummyIp = '127.0.0.1';
  
  async function testAuth (pnr) {
    const result = await authFlow(pnr, dummyIp, launchNativeApp);
    console.log(result.ok, result.status.user);
  }
  
  async function testSign (pnr) {
    const result = await signFlow(pnr, dummyIp, 'Test text for signing', launchNativeApp);
    console.log(result.ok, result.status.user);
  }

  ({
    auth: testAuth,
    sign: testSign,
    cancel: cancel,
  }[operation] || (_ => console.log(`Unknown operation ${operation}`)))(param);
}

module.exports = {
  authFlow,
  signFlow,
  cancel,
};
