<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <div class="profile-content">
      <img
        :src="user.picture"
        alt="Profile Picture"
        class="profile-picture"
      />
      <div class="profile-details">
        <h2>{{ user.name }}</h2>
        <p><strong>Role:</strong> {{ user.role }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: Object, // Passed down from the backend
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.profile-content {
  display: flex;
  align-items: center;
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-details h2 {
  margin: 0;
  font-size: 24px;
}

.profile-details p {
  margin: 5px 0;
}
</style>
