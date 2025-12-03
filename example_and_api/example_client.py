import requests
import time
import json
import jwt

import random

SERVER_URL = "http://127.0.0.1:5000"

PASSWORD = "dummy_password"
# NOTE: this is used as both passphrase and salt
# in PBKDF2 with SHA1 in 1000 iteration to derive
# symmetric key in MAC generation

def run():
    # Send POST request
    response = requests.post(f'{SERVER_URL}/login', data={"password": PASSWORD})

    # Check login result
    print("Status:", response.status_code)
    print("Response:", response.text)

    if (response.status_code == 200):
        print('Login successful')
    else:
        print('Login failed!!!!!!!')
        return
    # Print stored cookies
    stored_cookies = response.cookies.get_dict()
    print("Received cookies:", stored_cookies)

    while (1):
        r = requests.get(f"{SERVER_URL}/car", cookies=stored_cookies)
        if r.status_code != 200:
            print("Failed to get car", r.status_code, r.text)
            continue

        car = json.loads(r.text)
        if car['state'] == 'STOP':
            r = requests.get(f"{SERVER_URL}/get_tokens", cookies=stored_cookies)
            if r.status_code != 200:
                print("Failed to get tokens", r.status_code, r.text)
                continue

            response_payload = json.loads(r.text)

            if "tokens" in response_payload:
                tokens = response_payload["tokens"]
                # But first token, decode without verification
                token_payload = jwt.decode(tokens[0], options={"verify_signature": False})
                print(token_payload)
                if 'frame' in token_payload:
                    frame = token_payload['frame']
                    received_MAC = frame.get("MAC", None)
                    coordinates = frame.get("coordinates", None)
                    print('MAC:', received_MAC)
                    print('Coordinates:', coordinates)
                    #
                    index = 0 #dummy data
                    print('index:',index)
                    request_payload = {"index": index}
                    print('payload:', request_payload)
                    r2 = requests.post(
                        f"{SERVER_URL}/set_index",
                        json=request_payload,   # sends as application/json
                        cookies=stored_cookies,
                    )
                    print("Server response:", r2.status_code, r2.text)
            else:
                print("Response payload: ", response_payload)
        else:
            print(car['state'])
            print(car['position'])
        time.sleep(0.5)

if __name__ == "__main__":
    run()
