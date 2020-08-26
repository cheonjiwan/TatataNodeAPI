# Web Server for Socket I/O
---
### Purpose      
For our webOS project, this web server helps socket communication among web cam, smart ring and webos webapp.  
### Socket Server([SocketIO](https://socket.io/))    
Event 1: sendGPS     
=> get GPS data and device id from Raspi, broadcast data to webOS and CCTV.   
Event 2: turnCCTV      
=> get turn request from webOS dashboard, send turnning direction to CCTV.

### API    
* /getinfo      
method: GET
dataType: json     
request body: {id: id}
response body: {user_id, age, sex, phone_num, photo_url, user_address, etc}     
        
### User registration     
* /

