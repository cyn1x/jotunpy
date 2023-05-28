const evtSource = new EventSource("http://localhost:8000/events");

evtSource.onmessage = (event) => {
    console.log('Received event:', event);
    
    if (event.data == 'refresh')
        refreshPage()
};

evtSource.onerror = (err) => {
    console.error('EventSource failed:', err);
};

function refreshPage() {
    evtSource.close();

    location.reload();
}
