import requests
import base64
def encode_image(img_path):
    with open(img_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode("utf-8")

url = 'http://127.0.0.1:5567//predict'
response = requests.post(url, json = {'image': encode_image('static/main.png')})
print(response.text)

# url = 'http://127.0.0.1:5556//predict'
# response = requests.post(url, json = {'image': encode_image('/home/nero/Innoworks2021-APCSK18/services/last_1.jpeg')})
# print(response.text)