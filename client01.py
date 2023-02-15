import json
import requests
import websocket

# Login endpoint URL
url = 'http://127.0.0.1:8000/api/login'

# Login credentials
data = {
    'username': 'rogue',
    'password': '1q'
}
session = requests.Session()
# Send login POST request
response = session.post(url, data=data)

# Retrieve the session cookies from the response
cookies = response.cookies.get_dict()

# Use the cookies for subsequent requests to maintain the authentication

f = open("cookies.txt", "w+")
f.write(str(cookies))
f.close()
# Use the cookies for subsequent requests to maintain the authentication
response = session.get('http://127.0.0.1:8000/api/esp_token')
if response.status_code == 200:
    data = response.json()
    token = data['token']
    print(token)
else:
    print('Error:', response.status_code)


def on_message(ws, message):
    message = json.loads(message)
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, *args, **kwargs):
    print(kwargs)
    print("### closed ###")


def on_open(ws):
    print("### open ###")

    data = {
        'type': 'websocket_handshake',
        'path': f'/ws/esp/{token}/',
    }

    ws.send(json.dumps(data))


websocket.enableTrace(True)
ws = websocket.socket.connect(f"ws://localhost:8000/ws/esp/{token}/")
