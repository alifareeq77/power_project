import requests

# Login endpoint URL
url = 'http://127.0.0.1:8000/login'

# Login credentials
data = {
    'username': 'rogue',
    'password': '1q'
}

# Send login POST request
response = requests.post(url, data=data)

# Retrieve the session cookies from the response
cookies = response.cookies.get_dict()
f = open("cookies.txt", "w+")
f.write(str(response))
f.close()
# Use the cookies for subsequent requests to maintain the authentication
