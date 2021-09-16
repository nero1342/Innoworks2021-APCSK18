import requests

username = 'nero18@apcs.vn'
password = 'Nguyenero123!'

s = requests.Session()

base_url = 'http://portal-notification-cxnam-ews.education.wise-paas.com/api/'

# Login
data = {"username": username, "password": password}
auth_url = base_url + 'v1.5/Auth'
response = s.post(auth_url, data=data)
print(response)
print(response.text)

# List all groups
# group_url = base_url + 'v1.5/Groups'
# response = s.get(group_url)
# print(response)
# print(response.text)
# groupId = RT6Sa27Tvfua

# Send messages
data = {"groupId": "RT6Sa27Tvfua", 
        "subject": "Testing email",
        "useTemplate": True,
        "variables": {"something": "John"}}
send_noti_url = base_url + 'v1.5/Groups/send'
response = s.post(send_noti_url, data=data)
print(response, response.text)

