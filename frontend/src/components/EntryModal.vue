<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({ entry: Object })
const emit = defineEmits(['close'])

function closeModal() {
  emit('close')
}
</script>
<template>
  <div class="modal-backdrop" @click="closeModal">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>Entry Details</h3>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="modal-field">
          <label>ID:</label>
          <span>{{ entry.id }}</span>
        </div>
        
        <div class="modal-field">
          <label>Started:</label>
          <span>{{ new Date(entry.started_at).toLocaleString() }}</span>
        </div>
        
        <div class="modal-field">
          <label>Ended:</label>
          <span>{{ entry.ended_at ? new Date(entry.ended_at).toLocaleString() : 'Running' }}</span>
        </div>
        
        <div class="modal-field">
          <label>Duration:</label>
          <span v-if="entry.elapsed">
            {{ entry.elapsed.hours }}h {{ entry.elapsed.minutes }}m {{ entry.elapsed.seconds }}s
          </span>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-primary" @click="closeModal">Close</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #3f403f;
  border-radius: 24px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  color: #fff;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 40px 20px;
  border-bottom: 1px solid #222;
}

.modal-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 32px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  line-height: 32px;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #fff;
}

.modal-body {
  padding: 30px 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-field {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-field label {
  font-size: 15px;
  color: #999;
  font-weight: 500;
}

.modal-field span {
  font-size: 16px;
  color: #fff;
}

.modal-footer {
  padding: 20px 40px 30px;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn-primary {
  background: #ffffff;
  color: #000000;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.btn-primary:hover {
  box-shadow: #9e9e9d 0px 0px 7px;
}
</style>