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
  background: var(--color-off-white);
  padding: 0;
  overflow-x: hidden;
}

.container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 !important;
  width: 100%;
  min-height: 100vh;
}

.dashboard-wrapper {
  display: flex;
  flex-direction: row;
  gap: 24px;
  width: 100%;
  min-height: 100vh;
  padding: 15px;
  //padding-left: 102px;
  box-sizing: border-box;
}

.sidebar {
  flex-shrink: 0;
  width: 72px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: calc(100% - 96px);
  overflow-x: hidden;
}
</style>