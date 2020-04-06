// Det här är en kommentar
var ws = new WebSocket("ws://" + location.host + "/ws");
var update = function(event) {
    let data = JSON.parse(event.data);
    let p = document.getElementById("active");
    p.innerHTML = data['lights'];

    p = document.getElementById("players");
    p.innerHTML = data['players'];

    p = document.getElementById("stage");
    p.innerHTML = data['stage'];

    p = document.getElementById("heart_beat");
    p.innerHTML = data['heartBeat'];

    p = document.getElementById("running");
    p.innerHTML = data['running'];
    console.log(data);
};
ws.addEventListener('message', update, false)
//ws.addEventListener('open', update, false)
/*ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    let p = document.getElementById("active");
    p.innerHTML = data['lights'];
    console.log(data);
};*/
function sendDrinkEvent(event) {
    var json = {};
    json.action = "drink_event";
    ws.send(JSON.stringify(json));
    event.preventDefault();
}
function startGame(event) {
    const fetchValue = id => document.getElementById( id ).value;
    var json = {};
    var player_array = [];
    player_array.push(fetchValue('p1')); 
    player_array.push(fetchValue('p2')); 
    player_array.push(fetchValue('p3')); 
    player_array.push(fetchValue('p4'));
    json.players = player_array; 
    json.action = "start_game";
    ws.send(JSON.stringify(json));
    console.log(JSON.stringify(json));
    event.preventDefault();
}
