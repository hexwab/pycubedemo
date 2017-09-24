var player = prompt("player? (0-3)");
var ws;
function gebi(id) { return document.getElementById(id); }
var el = gebi("log");

function log(l) {
    el.innerHTML="<br>"+l;
    //window.scrollTo(0,document.body.scrollHeight);
}
function send(o) {
    ws.send(JSON.stringify(o));
}
function connected() {
    send({player:player});
    log("connected as player "+player);
}
function reconnect() {
    log("reconnecting");
    window.setTimeout(wsstart,300);
}
function onmsg(e) {
    m=JSON.parse(e.data);
    console.log(m);
    if (m.colname) {
	log("you are "+"<span style='color:"+m.col+"'>"+m.colname+"</sp"+"an>");
    } else if (m.gameover!==undefined) {
	log("you scored "+m.gameover);
    }
}
function wsstart() {
    ws = new WebSocket("ws://"+window.location.hostname+":27681/");
    ws.onopen = connected;
    ws.onclose = reconnect;
    ws.onmessage = onmsg;
}

for (var i=0;i<6;i++) {
    gebi(i).onclick=((i)=>(()=>sendkey(i)))(i);
}

wsstart();
keys = { a:0, d:1, w:2, s:3, q:4, e:5 };

function sendkey(k) {
    //log("sent "+k);
    send({key:k});
}
window.onkeydown = function(e) {
    var k=keys[e.key];
    if (k!==undefined)
        sendkey(k);
}
