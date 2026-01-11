const serverUrl = "http://localhost:8080/api/v1/timer/";

async function startTimer() {
    try {
        const response = await fetch(serverUrl + "start", {
            method: "POST",
            credentials: "include",
        })
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Failed to stop timer:", errorData.detail || errorData);
            return;
        }

        const data = await response.json();
        console.log("Start clicked:", data);
    }
    catch (error) {
        console.error("Error occurred: ", error)
    }
}

async function stopTimer() {
    const response = await fetch(serverUrl + "stop", {
        method: "POST",
        credentials: "include",
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const data = await response.json();

    if (!response.ok) {
        console.error("Failed to stop timer: ", data.error)
    }
    console.log("Stop clicked:", data);
}

const startBtn = document.getElementById("StartTimerBtn");
const stopBtn = document.getElementById("StopTimerBtn");

startBtn.addEventListener("click", startTimer);
stopBtn.addEventListener("click", stopTimer);
