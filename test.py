import requests

city = "Thrissur"  # Replace with your desired city
response = requests.get(f"http://wttr.in/{city}?format=j1")
data = response.json()
print(data['current_condition'][0]['weatherDesc'][0]['value'])
print(data['current_condition'][0]['temp_C'], "°C")
