var mysql = require('mysql');


var con = mysql.createConnection({
    host: "rm-gs5c889f8g6s7c80vso.mysql.singapore.rds.aliyuncs.com",
    user: "1802028WRH",
    password: "_Pass1234"
  });
  
  con.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
  });

