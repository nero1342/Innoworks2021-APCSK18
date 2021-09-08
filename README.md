# Innoworks2021-APCSK18

# Requirements
 - flask
 - WISE_PaaS_DataHub_Edge_Python_SDK
 - pytorch==1.9.0
 - pyyaml==5.1
 - detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.9/index.html

# Download model
Transportation model
```
gdown --id 1-j9pC9BwjqCIN3IpCdhGsEwtbxk6apds -O Models/Transportation/model_final.pth
```

# Run
Run two below scipts in parallel.
```
python cameraMonitor.py
python app.py
```

- cameraMonitor: Build Model + Send data to datahub
- app: Stream frame to port 5000

# Publish by ngrok
Find file config of ngrok, default is ``` ~/.ngrok/ngrok.yml``` after authtoken. 
Change that file:
```
authtoken: <your_token>
tunnels:
  first:
    addr: 5000
    proto: http
  second:
    addr: 8080
    proto: http
```
Run ngrok 
```
ngrok start --all
```

In total, we need three tabs in parallel to run cameraMonitor, app, ngrok
