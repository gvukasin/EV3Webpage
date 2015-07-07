//deal with communication with the server
function xml_http_post(url, data, callback) {
    var req = false;
    try {
        // Firefox, Opera 8.0+, Safari
        req = new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status==200) {
            callback(req);
        }
    }
    req.send(data);
}
//called when click the button,post data to the server and show feedback from the server
function call_LED() {
    var data1=document.led.range_value1.value;
    var data2=document.led.range_value2.value;
    var data3=document.led.range_value3.value;
    var data4=document.led.range_value4.value;
    var data ={device:'led',led1:data1,led2:data2,led3:data3,led4:data4};
    data=JSON.stringify(data);
    //console.log(data);
    //console.log(typeof data);
    xml_http_post("index.html", data, test_handle); 
    $("#test_result").fadeOut(200).fadeIn(200);
    
}
//show led range value 
function test_range1(data){
document.getElementById("rangevalue1").innerHTML=data;}
function test_range2(data){
document.getElementById("rangevalue2").innerHTML=data;}
function test_range3(data){
document.getElementById("rangevalue3").innerHTML=data;}
function test_range4(data){
document.getElementById("rangevalue4").innerHTML=data;}


function get_motorspeed(){
    var data1=document.motor.Speed0.value;
    var data2=document.motor.Speed1.value;
    var data3=document.motor.Speed2.value;
    var data4=document.motor.Speed3.value;
    var data={device:'motor',motor0:data1,motor1:data2,motor2:data3,motor3:data4};
    return data;}


function run_MOTOR() {
    var data=get_motorspeed();
    data.cmd='run';
    data=JSON.stringify(data);
    //console.log(data);
    //console.log(typeof data);
    xml_http_post("index.html", data, test_handle); 
    $("#test_result").fadeOut(200).fadeIn(200);}

function stop_MOTOR() {
    var data=get_motorspeed();
    data.cmd='stop';
    data=JSON.stringify(data);
    xml_http_post("index.html", data, test_handle); 
    $("#test_result").fadeOut(200).fadeIn(200);}

//show motor range value
function psp1(val){
document.getElementById("sp1").innerHTML=val;}
function psp2(val){
document.getElementById("sp2").innerHTML=val;}
function psp3(val){
document.getElementById("sp3").innerHTML=val;}
function psp4(val){
document.getElementById("sp4").innerHTML=val;}

// show sensor value
function show1(val){document.getElementById("s1").innerHTML=val;}
function show2(val){document.getElementById("s2").innerHTML=val;}
function show3(val){document.getElementById("s3").innerHTML=val;}
function show4(val){document.getElementById("s4").innerHTML=val;}

// sent post to server requesting sensor values
function getSensor() {
    var data = {device:'sensor'};
    data=JSON.stringify(data);
    xml_http_post("index.html", data, test_handle); 
    $("#test_result").fadeOut(200).fadeIn(200);}

//get response from server (callback)
function test_handle(req) {
    var elem1 = document.getElementById('test_result');
    // var elem2 = document.getElementById('s1');
    // var elem3 = document.getElementById('s2');
    // var elem4 = document.getElementById('s3');
    // var elem5 = document.getElementById('s4');
    elem1.innerHTML =  req.responseText;
    // elem2.innerHTML =  req.responseText; 
    // elem3.innerHTML =  req.responseText;
    // elem4.innerHTML =  req.responseText;
    // elem5.innerHTML =  req.responseText;


}
