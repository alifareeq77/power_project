function toggle() {
    let button = document.getElementById("switch");
    let status = document.getElementById("status");

    if (button.innerHTML === "TURN ON") {
        button.innerHTML = "TURN OFF";
        button.style.backgroundColor = "#f44336";
        status.innerHTML = "ON";
    } else {
        button.innerHTML = "TURN ON";
        button.style.backgroundColor = "#4CAF50";
        status.innerHTML = "OFF";
    }
}

function check() {
    let button = document.getElementById("switch");
    let status = document.getElementById("status");
    console.log(status.dataset.status)
    if (status.dataset.status.toLowerCase() === "false".toLowerCase()) {
        console.log(button.innerHTML)
        button.innerHTML = "TURN ON";
        button.style.backgroundColor = "#4CAF50";
        status.innerHTML = "OFF";
    }
    if (status.dataset.status.toLowerCase() === "true".toLowerCase()) {
        button.innerHTML = "TURN OFF";
        button.style.backgroundColor = "#f44336";
        status.innerHTML = "ON";
    }
}

function sendData(id) {
    // Define the data to be sent in the request body
    document.getElementById("switch").disabled = true;
    // Make the POST request using fetch()
    fetch(`change_statue/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: ''
    })
        .then(response => {
            if (response.ok) {
                // Enable button
                console.log('ok')
                document.getElementById("switch").disabled = false;
                toggle()
            } else {
                console.log('Server did not respond successfully')
                document.getElementById("switch").disabled = false;
            }
        })
        .catch(error => {
            console.error('Error sending data:', error);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    check();
})
//check current status