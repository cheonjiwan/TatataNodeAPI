var express = require('express');
var io = require('socket.io');
var path = require('path');
var app = express();

app.use(express.static(path.join(__dirname, 'html')));
app.get("/", function(req, res){
    res.sendFile(path.join(__dirname, 'html', 'main.html'));
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

app.get("/about", function (req, res) {
    res.sendFile(path.join(__dirname, 'html', 'about.html'));
    
    var mysql = require("mysql"); // mysql 모듈을 불러옵니다.

    // 커넥션을 정의합니다.
    // RDS Console 에서 본인이 설정한 값을 입력해주세요.
    var connection = mysql.createConnection({
    host: "userinfo-db.cfndrgetutvs.ap-northeast-2.rds.amazonaws.com",
    user: "jiwan",
    password: "wan2good",
    database: "UserInfo"
    });

    var device_id = req.query.id;
    var user_name = req.query.name;
    var age = req.query.age;
    var sex = req.query.gender;
    var phone_num = req.query.phonenumber;
    var photo_url = req.query.photo;
    var user_address = req.query.address;
    var etc = req.query.etc;

    var sql = "insert into user_info values ("+device_id+","+user_name+","+age+","+sex+","+phone_num+","+photo_url+","+user_address+","+etc+")"
    var selectsql = "select * from user_info"
    // RDS에 접속합니다.
    connection.connect(function(err) {
        if (err) {
            throw err; // 접속에 실패하면 에러를 throw 합니다.
        } else {
            // 접속시 쿼리를 보냅니다.
            connection.query(selectsql, function(err, rows, fields) {
                console.log(rows); // 결과를 출력합니다!
            });
        }
    });
    
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