<script setup>
import { ref } from 'vue'
let count = ref(0)
const serverUrl = "https://api.api-ninjas.com/v2/quotes"

async function fetchQuote() {
  const response = await fetch(serverUrl, {
    method: "GET",
  })
  const data = await response.json()
  return data
}
let quote = ref(await fetchQuote())
</script>

<template>
  <button @click="count++">{{quote}}</button>
  <h1>{{}}</h1>
</template>

<style scoped>

</style>