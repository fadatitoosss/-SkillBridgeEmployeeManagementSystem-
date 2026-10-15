console.log("EMS loaded");

$(document).ready(function () {
    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(scheme + '://' + window.location.host + '/ws/employees/');

    socket.onopen = function () { console.log('WebSocket connected'); };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const toast = $('<div class="alert alert-info shadow position-fixed top-0 end-0 m-3"></div>')
            .text(data.message)
            .css('z-index', 2000);
        $('body').append(toast);
        setTimeout(function () { toast.fadeOut('slow', function () { $(this).remove(); }); }, 5000);
    };

    socket.onclose = function () { console.log('WebSocket closed'); };
    socket.onerror = function (e) { console.log('WebSocket error', e); };
});