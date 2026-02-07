<script setup>
import SideMenuDashboard from "../Dashboard/DashboardSideMenu.vue";
import SettingsProfile from "@/components/Settings/SettingsProfile.vue";
import SettingsProjects from "@/components/Settings/SettingsProjects.vue";
import SettingsSecurity from "@/components/Settings/SettingsSecurity.vue";

import axios from "axios";
import { API_BASE_URL } from "@/config/api.js";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isVerified = ref(false);

const userDataForm = ref({
  email: '',
  username: '',
  password: '',
})
const isUserVerified = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/verify`, {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true,
    });

    if (response.data?.ok) {
      isVerified.value = true;
      return true;
    }
    return false;
  } catch (error) {
    console.error("Error verifying user:", error);
    isVerified.value = false;
    return false;
  }
};

const activeSettingTab = ref('general')

const settingsMap = {
  general: SettingsProfile,
  projects: SettingsProjects,
  security: SettingsSecurity,
}

const activeComponent = computed(() => {
  return settingsMap[activeSettingTab.value]
})

onMounted(async () => {
  const verified = await isUserVerified();
  if (!verified) {
    router.push('/login');
  }
});
</script>

<template>
  <div v-if="isVerified" class="settings-page">
    <div class="container">
      <div class="settings-wrapper">
        <aside class="sidebar">
          <SideMenuDashboard />
        </aside>
        <main class="main-content">
          <h1>Settings</h1>
          <header class="top-menu-section">
            <button @click="activeComponent = 'profile'">Profile</button>
            <button @click="activeComponent = 'projects'">Projects</button>
            <button @click="activeComponent = 'security'">Security</button>
          </header>
        </main>
      </div>
    </div>
  </div>
</template>
<style scoped>
h1{
  margin: 0;
  color: #000000;
  font-family: Montserrat;
}
h*, p* {
  margin: 0;
}
.settings-page {
  min-height: 100vh;
  background: var(--color-off-white);
  padding: 0;
  /* overflow-x: hidden; */
}

.container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 !important;
  width: 100%;
  min-height: 100vh;
}

.settings-wrapper {
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
  //overflow-x: hidden;
}

/* TOP MENU SECTION */
.top-menu-section {
  width: 100%;
  height: 50px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #a8a8a8;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
</style>