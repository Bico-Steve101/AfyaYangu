document.addEventListener('DOMContentLoaded', function() {
    var socket = new WebSocket('ws://' + window.location.host + '/chat/{{ chat.id }}/');

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        document.querySelector('#messages').innerHTML += '<div><strong>You</strong>: ' + message + '</div>';
    };

    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#messageForm').onsubmit = function(e) {
        e.preventDefault();
        var messageInput = document.querySelector('#id_content');
        var message = messageInput.value;
        socket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    };
});