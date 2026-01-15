let startTimerBtn = document.getElementById("startBtn");
let stopTimerBtn = document.getElementById("stopBtn");
let sessionTime = document.getElementById("sessionTime");
let timerActive = false
const serverUrl = `http://localhost:8080/api/v1/timer/`

async function fetchCurrentEntry() {
    const response = await fetch(serverUrl+"current", {
        method: 'GET',
        credentials: "include"
    })
    if (!response.ok) {
        if (response.status === 204) {
            // No current entry found
            timerActive = false
            startTimerBtn.style.display = "block"
            stopTimerBtn.style.display = "none";
            return null;
        }
        else {
            throw new Error(`Unexpected error: ${response.status} ${response.statusText}`);
        }
    }
    // Active timer found
    timerActive = true
    startTimerBtn.style.display = "none"
    stopTimerBtn.style.display = "block"
    if (response.ok) {
        if (response.status === 204) {
            // No active timer found
            timerActive = false
            stopTimerBtn.style.display = "none";
            startTimerBtn.style.display = "block"
            console.log("No current running timer")
        }
        else {
            const response_json = await response.json();
            return new Date(response_json.started_at);
        }
    }
    else {
        console.error(response.statusText);
    }
}

function controlTimer() {

    async function startTimerRequest() {
            const response = await fetch(serverUrl + "start", {
            method: "POST",
            credentials: "include",
        });

        if (!response.ok) {
            if (response.status === 409) {
                const err = await response.json();
                console.log(err.detail);
                startTimerBtn.disabled = false;
                timerActive = false
                return;
            } else {
                throw new Error(`Unexpected error: ${response.status} ${response.statusText}`);
            }
        }
        // Active timer is found
        timerActive = true
        startTimerBtn.style.display = "none"
        stopTimerBtn.style.display = "block"
    }

    async function stopTimerRequest() {
        const response = await fetch(serverUrl + "stop", {
            method: "POST",
            credentials: "include",
        });

        if (!response.ok) {
            if (response.status === 204) {
                const err = await response.json();
                console.log(err.detail);
                startTimerBtn.disabled = true;
                timerActive = true
                return;
            }
            else {
                throw new Error(`Unexpected error: ${response.status} ${response.statusText}`);
            }
        }
        // Timer stopped
        timerActive = false
        startTimerBtn.style.display = "block"
        stopTimerBtn.style.display = "none";
        sessionTime.textContent = "0h 0m"
    }

    document.getElementById("startBtn").addEventListener("click", async () => {
        try {
            await startTimerRequest();
        } catch (error) {
            console.error("Network or unexpected error:", error);
        }
    });
    document.getElementById("stopBtn").addEventListener("click", async () => {
        try {
            await stopTimerRequest();
        }
        catch (error) {
            console.error("Network or unexpected error:", error);
        }
    })
}
// Start functions after DOM is loaded
document.addEventListener("DOMContentLoaded", async () => {
    controlTimer()
    const startTime = await fetchCurrentEntry();

    if (!startTime) {
        return;
    }

    // Updating elapsed time
    function updateElapsedTime() {
        const elapsedMs = new Date() - startTime;
        const totalSeconds = Math.floor(elapsedMs / 1000);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        sessionTime.textContent = `${hours}h ${minutes}m ${seconds}s`;
    }

    updateElapsedTime();
    setInterval(updateElapsedTime, 1000);
})
