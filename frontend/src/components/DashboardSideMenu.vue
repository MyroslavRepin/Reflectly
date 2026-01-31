<script setup>

</script>
<template>
  <div class="sidebar-menu">
    <div class="top-navigation">
      <div class="link-square"></div>
    </div>
    <div class="bottom-navigation">
      <div class="link-square"></div>
      <div class="link-square"></div>
    </div>
  </div>
</template>

<style scoped>
.sidebar-menu {
  position: fixed;
  top: 15px;
  left: 15px;
  bottom: 15px;
  width: 60px;
  background-color: #0a0a0a;
  color: #000000;
  display: flex;
  padding: 10px 0;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border-radius: 12px;
}

.top-navigation {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.link-square {
  box-sizing: border-box;
  width: 40px;
  height: 40px;
  background-color: #FFFFFF;
  border-radius: 7px;
}

.bottom-navigation {
  display: flex;
  gap: 10px;
  flex-direction: column;
  align-items: center;
}
</style>