<script setup>
import DashboardTimerSection from "./DashboardTimerSection.vue";
import SideMenuDashboard from "./DashboardSideMenu.vue";
import DashboardUserGreeting from "./DashboardUserGreeting.vue";
import DashboardEntries from "./DashboardEntries.vue";
</script>

<template>
  <div class="dashboard-page">
    <div class="container">
      <div class="dashboard-wrapper">
        <aside class="sidebar">
          <SideMenuDashboard />
        </aside>
        <main class="main-content">
<!--          <DashboardUserGreeting />-->
          <DashboardTimerSection />
          <DashboardEntries />
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
  /* align-items: center; */
}

.dashboard-wrapper {
  display: flex;
  flex-direction: row;
  gap: 100px;
  width: 100%;
  min-height: 600px;
  padding-left: 10px;
}

.sidebar {
  flex-shrink: 0;
  display: flex;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>