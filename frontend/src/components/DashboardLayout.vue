<script setup>
import TimerSection from "./TimerSection.vue";
import SideMenuDashboard from "./DashboardSideMenu.vue";
</script>

<template>
  <div class="dashboard-page">
    <div class="container">
      <div class="dashboard-wrapper">
        <aside class="sidebar">
          <SideMenuDashboard />
        </aside>
        <main class="main-content">
          <TimerSection />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

.container {
  min-height: 100vh;
  display: flex;
  //align-items: center;
}

.dashboard-wrapper {
  display: flex;
  flex-direction: row;
  gap: 40px;
  width: 100%;
  min-height: 600px;
}

.sidebar {
  flex-shrink: 0;
  display: flex;
}

.main-content {
  flex: 1;
  display: flex;
  //align-items: center;
  justify-content: center;
}
</style>