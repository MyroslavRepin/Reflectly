<script setup>
import {ref, onMounted, computed, onUnmounted, watch} from "vue";
import axios from "axios";

let isError = ref(false)
let errorMessage = ref("")
let isTimerRunning = ref(false)

const startedAtTimerSeconds = ref(0)
const dateNow = ref(new Date())
const elapsedSeconds = ref(0)
let intervalId = null

function startTick() {
  if (intervalId) return

  intervalId = setInterval(() => {
    elapsedSeconds.value += 1
  }, 1000)
}
function stopTick() {
  clearInterval(intervalId)
  intervalId = null
}

const hours = computed(() => Math.floor(elapsedSeconds.value / 3600))
const minutes = computed(() => Math.floor(elapsedSeconds.value / 60) % 60)
const seconds = computed(() => elapsedSeconds.value % 60)

async function initTimerFromApi() {
  try {
    const response = await axios.get(
      'http://localhost:8080/api/v1/timer/current',
      { withCredentials: true }
    )

    if (response.status === 204) {
      isTimerRunning.value = false
      elapsedSeconds.value = 0
      return
    }

    const startedAt = Math.floor(
      new Date(response.data.started_at).getTime() / 1000
    )

    const now = Math.floor(Date.now() / 1000)

    elapsedSeconds.value = now - startedAt
    isTimerRunning.value = true
    startTick()

  } catch (e) {
    console.error('Timer init failed', e)
  }
}

const startTimerRequest = async () => {
  try {
    const response = await axios('http://localhost:8080/api/v1/timer/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true,
    })
    console.log("Timer started:", response.data);
    isTimerRunning.value = true;
  }
  catch (error) {
    isError.value = true
    errorMessage.value = error.message
    console.error("Error starting timer:", error);
  }
}
const stopTimerRequest = async () => {
  try {
    const response = await axios('http://localhost:8080/api/v1/timer/stop', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true,
    })
    isTimerRunning.value = false
    elapsedSeconds.value = 0
  }
  catch (error) {
    isError.value = true
    errorMessage.value = error.message
    console.error("Error stopping timer:", error);
  }
}

onMounted( () => {
  initTimerFromApi()
})

watch(isTimerRunning, (running) => {
  if (running) startTick()
  else stopTick()
})
const timerDisplay = computed(() => {
  return `${hours.value}h ${minutes.value}m ${seconds.value}s`
})
</script>

<template>
<!--  <div class="timer-card">-->
<!--    <div class="timer-header">-->
<!--      <p class="current-session">Current session</p>-->
<!--      <p class="session-time">{{ timerDisplay }}</p>-->
<!--      <div class="timer-controls">-->
<!--        <button v-on:click="startTimerRequest" v-if="!isTimerRunning">Start Timer</button>-->
<!--        <button v-on:click="stopTimerRequest" v-if="isTimerRunning">Stop Timer</button>-->
<!--      </div>-->
<!--      <p v-show="isError">{{errorMessage}}</p>-->
<!--    </div>-->
  <div class="tracking-card">
      <div class="tracking-header">
        <div class="left-side-card">
          <div class="current-session">Current Session</div>
          <div class="session-time" id="sessionTime">0h 00m</div>
          <div class="session-project">React Dashboard Project</div>
          <div class="status-indicator">
            <div class="status-dot"></div>
            <div class="status-text">Tracking active</div>
          </div>
        </div>
        <div class="tracking-controls">
          <button class="btn btn-start" id="startBtn" onclick="startTracking()" style="display: inline-block;">Start</button>
          <button class="btn btn-pause" id="pauseBtn" onclick="pauseTracking()" style="display: none;">Pause</button>
          <button class="btn btn-stop" id="stopBtn" onclick="stopTracking()" style="display: none;">Stop</button>
        </div>
      </div>
  </div>
</template>

<style scoped>
.tracking-card {
    background: #0a0a0a;
    border-radius: 24px;
    padding: 40px;
    margin-bottom: 30px;
    color: #fff;
  width: 700px;
}
.tracking-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 30px;
}
.current-session {
    font-size: 15px;
    color: #999;
    margin-bottom: 8px;
}
.session-time {
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -2px;
}
.session-project {
    font-size: 18px;
    color: #999;
    margin-top: 8px;
}
.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 20px;
}
.tracking-controls {
    display: flex;
    gap: 12px;
}
</style>