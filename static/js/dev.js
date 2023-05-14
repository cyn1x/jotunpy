// const socket = new WebSocket('ws://google.com:80')

// socket.onmessage = ({ data }) => {
//     console.log('Message from server ', data)
// }

// const socket = io('wss://localhost:5000')

// socket.on('message', text => {
//     console.log(text)
// })


// socket.emit("hodwy")

var net = require('net');

var client = new net.Socket();
client.connect(5000, '127.0.0.1', function() {
    console.log('Connected');
    client.write('Hello, server! Love, Client.');
});

client.on('data', function(data) {
    console.log('Received: ' + data);
    client.destroy(); // kill client after server's response
});