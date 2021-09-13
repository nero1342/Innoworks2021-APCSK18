# Innoworks2021-APCSK18

# Requirements
## Install Pedestron model
```
pip install virtualenv

virtualenv pytorch14
source pytorch14/bin/activate
pip install -r requirements_14.txt

cd models
git clone https://github.com/hasanirtiza/Pedestron.git
cd Pedestron
pip install -v -e .
```
## Install Transportation model
```
virtualenv pytorch19
source pytorch19/bin/activate
pip install -r requirements_19.txt
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.9/index.html
```
# Download model
```
mkdir weights
gdown --id 1-j9pC9BwjqCIN3IpCdhGsEwtbxk6apds -O weights/transportation.pth
gdown --id 12mWjmWBv-4wra8hCNF71Wq0U2va0Ai8e -O weights/CascadeRCNNCP_model.pth.stu
```

# Run
There are 2 ways:
## Run each service each tap in parallel
```
source activate pytorch19
python services/app.py 
```

```
source activate pytorch19
python services/app_transportation.py
```

```
source activate pytorch14
python services/app_pedestron.py
```

```
python cameraMonitor.py
```
## All in one bash (run services in background, need to kill process manually)
```
sh app.sh 
```

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


# Activate cameras in dashboard
- Assume the current ngrok domain is http://8a20-14-238-32-110.ngrok.io 

Follow these steps to activate the camera:
- Go to the dashboard. [Link here](https://dashboard-cxnam-ews.education.wise-paas.com/?orgId=5)
- Chose the ```Main``` dashboard.
- Edit panel "Camera 1"
- Choose Visualization
- Edit the ```Picture URL``` by ```http://8a20-14-238-32-110.ngrok.io/static/last_0.jpeg``` (The format is ```{DOMAIN}/static/last_{X - 1}.jpeg```)
- Save dashboard. 

Do the same with other cameras (i.e Camera 2 - last_1.jpeg, Camera 3 - last_2.jpeg)