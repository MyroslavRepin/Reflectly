<script setup>
</script>

<template>
  <div class="landing-page">
    <h1>Landing Page</h1>
    <ul>
      <li>
        <RouterLink to="/login">Log In</RouterLink>
      </li>
      <li>
        <RouterLink to="/signup">Sign Up</RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.landing-page {
  display: block;
  padding: 0;
  margin: 0;
}
</style>