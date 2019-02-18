# BankID integration made easy
These are instructions for integrating Swedish BankID that aim to be as _succinct_ as possible. They should cover the needs of 99% of BankID integrations.

For a complete reference, refer to the official documentation available at [bankid.com](https://www.bankid.com/bankid-i-dina-tjanster/rp-info).

It's assumed that you are familiar with how BankID works from the users point of view. Armed with that knowledge, you should have all the important parts up and running within the hour. Let's go.

## Setting up your request agent
You have to configure your request agent to use the SSL certificate provided by BankID. The specifics of how to do that will depend on your environment.

BankID provides a PFX file for use with the test environment, available [here](https://www.bankid.com/assets/bankid/rp/FPTestcert2_20150818_102329.pfx). Switching to production later is a matter of using a different file (that your issuing bank will provide).

The certificate authority files for the environments are:

<details><summary>Test</summary><p>
<pre>
-----BEGIN CERTIFICATE-----
MIIF0DCCA7igAwIBAgIIIhYaxu4khgAwDQYJKoZIhvcNAQENBQAwbDEkMCIGA1UECgwbRmluYW5zaWVsbCBJRC1UZWtuaWsgQklEIEFCMRowGAYDVQQLDBFJbmZyYXN0cnVjdHVyZSBDQTEoMCYGA1UEAwwfVGVzdCBCYW5rSUQgU1NMIFJvb3QgQ0EgdjEgVGVzdDAeFw0xNDExMjExMjM5MzFaFw0zNDEyMzExMjM5MzFaMGwxJDAiBgNVBAoMG0ZpbmFuc2llbGwgSUQtVGVrbmlrIEJJRCBBQjEaMBgGA1UECwwRSW5mcmFzdHJ1Y3R1cmUgQ0ExKDAmBgNVBAMMH1Rlc3QgQmFua0lEIFNTTCBSb290IENBIHYxIFRlc3QwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCAKWsJc/kV/0434d+Sqn19mIr85RZ/PgRFaUplSrnhuzAmaXihPLCEsd3Mh/YErygcxhQ/MAzi5OZ/anfuWSCwceRlQINtvlRPdMoeZtu29FsntK1Z5r2SYNdFwbRFb8WN9FsU0KvC5zVnuDMgs5dUZwTmdzX5ZdLP7pdgB3zhTnra5ORtkiWiUxJVev9keRgAo00ZHIRJ+xTfiSPdJc314maigVRQZdGKSyQcQMTWi1YLwd2zwOacNxleYf8xqKgkZsmkrc4Dp2mR5PkrnnKB6A7sAOSNatua7M86EgcGi9AaEyaRMkYJImbBfzaNlaBPyMSvwmBZzp2xKc9OD3U06ogV6CJjJL7hSuVc5x/2H04d+2I+DKwep6YBoVL9L81gRYRycqg+w+cTZ1TF/s6NC5YRKSeOCrLw3ombhjyyuPl8T/h9cpXt6m3y2xIVLYVzeDhaql3hdi6IpRh6rwkMhJ/XmOpbDinXb1fWdFOyQwqsXQWOEwKBYIkM6cPnuid7qwaxfP22hDgAolGMLY7TPKUPRwV+a5Y3VPl7h0YSK7lDyckTJdtBqI6d4PWQLnHakUgRQy69nZhGRtUtPMSJ7I4Qtt3B6AwDq+SJTggwtJQHeid0jPki6pouenhPQ6dZT532x16XD+WIcD2f//XzzOueS29KB7lt/wH5K6EuxwIDAQABo3YwdDAdBgNVHQ4EFgQUDY6XJ/FIRFX3dB4Wep3RVM84RXowDwYDVR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBQNjpcn8UhEVfd0HhZ6ndFUzzhFejARBgNVHSAECjAIMAYGBCoDBAUwDgYDVR0PAQH/BAQDAgEGMA0GCSqGSIb3DQEBDQUAA4ICAQA5s59/Olio4svHXiKu7sPQRvrf4GfGB7hUjBGkYW2YOHTYnHavSqlBASHc8gGGwuc7v7+H+vmOfSLZfGDqxnBqeJx1H5E0YqEXtNqWG1JusIFa9xWypcONjg9v7IMnxxQzLYws4YwgPychpMzWY6B5hZsjUyKgB+1igxnfuaBueLPw3ZaJhcCL8gz6SdCKmQpX4VaAadS0vdMrBOmd826H+aDGZek1vMjuH11FfJoXY2jyDnlol7Z4BfHc011toWNMxojI7w+U4KKCbSxpWFVYITZ8WlYHcj+b2A1+dFQZFzQN+Y1Wx3VIUqSks6P7F5aF/l4RBngy08zkP7iLA/C7rm61xWxTmpj3p6SGfUBsrsBvBgfJQHD/Mx8U3iQCa0Vj1XPogE/PXQQq2vyWiAP662hD6og1/om3l1PJTBUyYXxqJO75ux8IWblUwAjsmTlF/Pcj8QbcMPXLMTgNQAgarV6guchjivYqb6Zrhq+Nh3JrF0HYQuMgExQ6VX8T56saOEtmlp6LSQi4HvKatCNfWUJGoYeT5SrcJ6snBy7XLMhQUCOXcBwKbNvX6aP79VA3yeJHZO7XParX7V9BB+jtf4tz/usmAT/+qXtHCCv9Xf4lv8jgdOnFfXbXuT8I4gz8uq8ElBlpbJntO6p/NY5a08E6C7FWVR+WJ5vZOP2HsA==
-----END CERTIFICATE-----
</pre></p></details>

<details><summary>Prod</summary><p><pre>
-----BEGIN CERTIFICATE-----
MIIFvjCCA6agAwIBAgIITyTh/u1bExowDQYJKoZIhvcNAQENBQAwYjEkMCIGA1UECgwbRmluYW5zaWVsbCBJRC1UZWtuaWsgQklEIEFCMRowGAYDVQQLDBFJbmZyYXN0cnVjdHVyZSBDQTEeMBwGA1UEAwwVQmFua0lEIFNTTCBSb290IENBIHYxMB4XDTExMTIwNzEyMzQwN1oXDTM0MTIzMTEyMzQwN1owYjEkMCIGA1UECgwbRmluYW5zaWVsbCBJRC1UZWtuaWsgQklEIEFCMRowGAYDVQQLDBFJbmZyYXN0cnVjdHVyZSBDQTEeMBwGA1UEAwwVQmFua0lEIFNTTCBSb290IENBIHYxMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwVA4snZiSFI3r64LvYu4mOsI42A9aLKEQGq4IZo257iqvPH82SMvgBJgE52kCx7gQMmZ7iSm39CEA19hlILh8JEJNTyJNxMxVDN6cfJP1jMHJeTES1TmVbWUqGyLpyT8LCJhC9Vq4W3t/O1svGJNOUQIQL4eAHSvWTVoalxzomJhOn97ENjXAt4BLb6sHfVBvmB5ReK0UfwpNACFM1RN8btEaDdWC4PfA72yzV3wK/cY5h2k1RM1s19PjoxnpJqrmn4qZmP4tN/nk2d7c4FErJAP0pnNsll1+JfkdMfiPD35+qcclpspzP2LpauQVyPbO21Nh+EPtr7+Iic2tkgz0g1kK0IL/foFrJ0Ievyr3Drm2uRnA0esZ45GOmZhE22mycEX9l7w9jrdsKtqs7N/T46hil4xBiGblXkqKNG6TvARk6XqOp3RtUvGGaKZnGllsgTvP38/nrSMlszNojrlbDnm16GGoRTQnwr8l+Yvbz/ev/e6wVFDjb52ZB0Z/KTfjXOl5cAJ7OCbODMWf8Na56OTlIkrk5NyU/uGzJFUQSvGdLHUipJ/sTZCbqNSZUwboI0oQNO/Ygez2J6zgWXGpDWiN4LGLDmBhB3T8CMQu9J/BcFvgjnUyhyim35kDpjVPC8nrSir5OkaYgGdYWdDuv1456lFNPNNQcdZdt5fcmMCAwEAAaN4MHYwHQYDVR0OBBYEFPgqsux5RtcrIhAVeuLBSgBuRDFVMA8GA1UdEwEB/wQFMAMBAf8wHwYDVR0jBBgwFoAU+Cqy7HlG1ysiEBV64sFKAG5EMVUwEwYDVR0gBAwwCjAIBgYqhXBOAQQwDgYDVR0PAQH/BAQDAgEGMA0GCSqGSIb3DQEBDQUAA4ICAQAJOjUOS2GJPNrrrqf539aN1/EbUj5ZVRjG4wzVtX5yVqPGcRZjUQlNTcfOpwPoczKBnNX2OMF+Qm94bb+xXc/08AERqJJ3FPKu8oDNeK+Rv1X4nh95J4RHZcvl4AGhECmGMyhyCea0qZBFBsBqQR7oC9afYOxsSovaPqX31QMLULWUYoBKWWHLVVIoHjAmGtAzMkLwe0/lrVyApr9iyXWhVr+qYGmFGw1+rwmvDmmSLWNWawYgH4NYxTf8z5hBiDOdAgilvyiAF8Yl0kCKUB2fAPhRNYlEcN+UP/KL24h/pB+hZ9mvR0tM6nW3HVZaDrvRz4VihZ8vRi3fYnOAkNE6kZdrrdO7LdBc9yYkfQdTcy0N+Aw7q4TkQ8npomrVmTKaPhtGhA7VICyRNBVcvyoxr+CY7aRQyHn/C7n/jRsQYxs7uc+msq6jRS4HPK8olnF9usWZX6KY+8mweJiTE4uN4ZUUBUtt8WcXXDiK/bxEG2amjPcZ/b4LXwGCJb+aNWP4+iY6kBKrMANs01pLvtVjUS9RtRrY3cNEOhmKhO0qJSDXhsTcVtpbDr37UTSqQVw83dReiARPwGdURmmkaheH6z4k6qEUSXuFch0w53UAc+1aBXR1bgyFqMdy7Yxib2AYu7wnrHioDWqP6DTkUSUeMB/zqWPM/qx6QNNOcaOcjA==
-----END CERTIFICATE-----
</pre></p></details>

### Examples
- [Node.js/Axios](https://todo.com/test.js)

After you've configured the http agent, you're ready to start making API
calls.
- All calls are made as HTTP POST
- Must include the header `Content-Type: application/json`
- All parameters should (unsurprisingly) be sent as JSON in the request body
- For all the methods covered below, calling them is simply a matter of making a POST request to `BASE_URL/METHOD_NAME`

The base URL for the test environment is `https://appapi2.test.bankid.com/rp/v5`, and production is located at `https://appapi2.bankid.com/rp/v5`. These may not be the most _current_ ones when you're reading this, but they should remain available indefinitely at the given locations.

## Authentication
To initiate authentication, call the `auth` endpoint (for example `https://appapi2.test.bankid.com/rp/v5/auth`) with the following parameters.

Name|Required|Example|Description
-|-|-|-
endUserIp|Yes|`"213.112.83.16"`
personalNumber|Yes*|`"198006211414"`|Required for the "other device" flow. For "same device" it's optional.
requirement|No|`{}`|Object containing various flags. For "same device" flow, pass `certificatePolicies: ['1.2.752.78.1.5']`. Another useful requirement is `allowFingerprint: true`. You probably won't ever need any of the other possible fields.

Making this call will trigger the authorization flow in the users BankID app.

## Signing
To initiate signing, use the `sign` endpoint.

Name|Required|Example|Description
-|-|-|-
endUserIp|Yes|`213.112.83.16`
userVisibleData|Yes|`"SmFnIGludHlnYXIgYXR0IGphZyB2aWxsIHNrcml2YSBww6UgZG9rdW1lbnRldC4="`|Base64 encoded string containing the text you want the user to sign.
personalNumber|Yes*|`198006211414`|See `auth`.
requirement|No|`{}`|See `auth`.

Making this call will trigger the signing flow in the users BankID app. 

## Polling for results
Both the `sign` and `auth` endpoints return objects that contain the fields `autoStartToken` and `orderRef`. You will need to poll the `collect` method to retrieve the status of an ongoing operation.

Documentation states that you should call `collect` every two seconds but specifically not more often than once per second.

The `collect` method takes a single parameter – `orderRef` – and returns two out of three values: `status`, `hintCode` and `completionData`.

If `status` is `pending`, keep polling.
If `status` is `complete` or `failed`, the flow has finished. For failed and pending orders, `hintCode` will provide more information on the reason/state. For completed orders, `completionData` will be an object containing information on the user.

## Cancelling an ongoing order
Call `cancel` with a single parameter – `orderRef`. Any ongoing orders must be cancelled before the user can start a new order.

## Wrapping up
Those four methods, `auth`, `sign`, `collect`, and `cancel` are all you need to get your integration working. Once you get this far though, you'll need to refer to the official docs to ensure you're in compliance with all of the specific requirements therein. For example, certain failstates require you to display specific error messages, and certain data must always be persisted to disk.