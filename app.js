var express = require('express');
var io = require('socket.io');
var app = express();

app.get("/", function(req, res){
    res.send("Hello world!");
    res.send("seongwoo let's go!");
});


app.get("/gps", function(req, res){
    var lat = req.query.lat;
    var lng = req.query.lng;
    var device_id = req.query.device_id;

    var obj = new Object();
    obj.lat = lat;
    obj.lng = lng;
    obj.device = device_id;

    //WebSocket Client
    res.send(JSON.stringify(obj));
});



var port = process.env.PORT || 8081;
var server = app.listen(port, function(){
    console.log("Express server has started on port " + port)
})
server.timeout = 1000;

const socketServer = io(server);

socketServer.on("connection", socket=>{
    console.log("connect client by socket.io - id: " + socket.id);
    socket.on("sendGPS", req=>{
        console.log(req);
        socket.broadcast.emit("sendGPS", {data: req});
    })

    socket.on("disconnection", socket=>{
        console.log("disconnect client manually - id: " + socket.id);
    })
})