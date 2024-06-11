document.getElementById('request-permission-btn').addEventListener('click', function() {
    Notification.requestPermission().then(function(permission) {
        if (permission === 'granted') {
            document.getElementById('show-notification-btn').style.display = 'block';
        }
    });
});

document.getElementById('show-notification-btn').addEventListener('click', function() {
    if (Notification.permission === 'granted') {
        new Notification('Hello!', {
            body: 'This is a test notification.',
            icon: '../static/img/campana.png' // Puedes agregar un ícono aquí
        });
    }
});
