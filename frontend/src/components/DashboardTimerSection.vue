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

const formData = ref({
  title: '',
  description: '',
});

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
const pauseTimerRequest = async () => {
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
  <div class="tracking-card">
      <div class="tracking-header">
        <div class="left-side-card">
          <div class="current-session">Current Session</div>
          <div class="session-time" id="sessionTime">{{ timerDisplay }}</div>
          <div class="session-project" v-if="isTimerRunning">Current task</div>
        </div>
        <div class="tracking-controls">
          <button class="btn btn-start" v-if="!isTimerRunning" @click="startTimerRequest">Start</button>
          <button class="btn btn-pause" v-if="isTimerRunning" @click="pauseTimerRequest">Pause</button>
          <button class="btn btn-stop" v-if="isTimerRunning" @click="stopTimerRequest">Stop</button>
        </div>
      </div>
      <div class="bottom-section">
        <div class="timerForm" v-if="!isTimerRunning">
          <form>
            <input id="titleFrom" type="text" placeholder="How do you want call your session?" class="titleForm" v-model="formData.title"/>
            <textarea id="descriptionForm" placeholder="Tell what you want to do..." class="descriptionForm" v-model="formData.description"/>
          </form>
        </div>
      </div>
  </div>
</template>

<style scoped>
.tracking-card {
  margin-top: 15px;
  background: #0a0a0a;
  border-radius: 24px;
  padding: 40px;
  margin-bottom: 30px;
  color: #fff;
  max-width: 700px;
  width: 100%;
  min-height: 200px;  /* Change height to min-height */
}
.tracking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
}
.left-side-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
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
.tracking-controls {
  display: flex;
  gap: 16px;
}
.btn-start {
  background: #ffffff;
  color: #000000;
}
.btn-start:hover {
  box-shadow: #9e9e9d 0px 0px 7px;
  border-color: transparent;
}
.btn {
  color: #000000;
}
.btn:hover {
  transition: all 0.3s ease-in-out;
}
.btn-stop:hover {
  background-color: #be2222;
}
.btn-pause {
  border-color: #222222;
  border-width: 1.5px;
  background: #1a1a1a;
  color: #FFFFFF;
}
.btn-pause:hover {
  background-color: #222222;
}
.btn-stop {
  background: #dc2626;
  color: #FFFFFF;
}
/* Form styles */
.bottom-section{
  display: flex;
  flex-direction: column;
}
.titleForm, .descriptionForm{
  border: none;
  width: 70%;
  height: 30px;
  border-radius: 8px;
  background-color: rgba(43, 43, 47, 0.23);
  padding-left: 10px;
  color: #FFFFFF;
}
.titleForm::placeholder, .descriptionForm::placeholder{
  color: #b6b6b6;
}
.descriptionForm{
  padding-top: 10px;
  margin-top: 10px;
  width: 100%;
  height: 100px;
  max-width: 100%;
  min-width: 100%;
  max-height: 100px;
  min-height: 100px;
}
</style>