# Smart Emergency Monitoring System    
     
smart emergency monitoring system and smart wristband for a quick emergency call     

### Components     
- Web Server for Socket I/O (Node.js) -> see our root directory     
- RaspberryPi 4 for smart CCTV (Python)    
- [RaspberryPi 4 for smart wristband](https://github.com/kjsu0209/TatataNodeAPI/tree/master/band(client)) (Python)  
- [Web App for Emergency Dashboard](https://github.com/kjsu0209/TatataNodeAPI/tree/master/myApp) (HTML, JavaScript)      

----

## Web Server for Socket I/O
       
### Purpose      
For our webOS project, this web server helps socket communication among web cam, smart ring and webos webapp.  
### Socket Server([SocketIO](https://socket.io/))    
Event 1: sendGPS     
=> get GPS data and device id from Raspi, broadcast data to webOS and CCTV.   
- data      
data:{data:{lat, lng}}   
lat=latitude, lng=longitude       
     
Event 2: turnCCTV      
=> get turn request from webOS dashboard, send turnning direction to CCTV.       
- data      
data:{data:direction}       
left=0, right=1     
      
### API    
* /getinfo      
method: GET       
dataType: json     
request body: {id: id}       
response body: {user_id, age, sex, phone_num, photo_url, user_address, etc}     
        
### User registration     
* /

-------------------

## Web App for Emergency Dashboard
       
### Purpose      
This is an web app for showing emergency dashboard, works on webOS platform. The dashboard will show registered information of user who pushed the button of wristband and current CCTV screen. We added one more feature; buttons as a CCTV controller! These buttons will request to CCTV turn to each angle. Below is more detailed description of our dashboard.        
#### 1. Map    
Using Google Map API, dashboard will receive location info from server and display on screen.    
#### 2. User Information       
Dashboard will request /getinfo API to get user's information. AJAX is used for this feature.       
#### 3. Socket I/O Client      
This Dashboard can get/show data whenever user call.      
#### 4. CCTV monitoring/control      
Stream the nearest CCTV screen and control the CCTV.

-------------------

## RaspberryPi 4 for smart wristband

### Purpose
For our webOS project, this Pi sends location information and user data to the web server.

### Component
1 RaspberryPi4, 1 Buzzer sensor, 1 Button sensor, 1 GPS sensor.

### Process

* Raspi always checks if the emergency button is pressed.
* When the button is pressed for 3 seconds, raspi gets user location data from GPS sensor.
* Raspi sends the location data, user information and unique device number to the server.
* Also, make sound through a buzzer sensor.

-------------------

## Demo     

![image](https://user-images.githubusercontent.com/35682236/94402345-e306ba80-01a6-11eb-89ff-8a32efde745f.png)
![image2](https://user-images.githubusercontent.com/35682236/94449561-2d0f9080-01e7-11eb-9de3-fe8f74a01541.png)
