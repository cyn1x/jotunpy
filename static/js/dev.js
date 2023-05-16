const evtSource = new EventSource("http://localhost:8000/events");

evtSource.onmessage = (event) => {
    console.log('Received event:', event);
};

evtSource.onerror = (err) => {
    console.error('EventSource failed:', err);
};

function refreshPage() {
    evtSource.close();

    location.reload();
}
