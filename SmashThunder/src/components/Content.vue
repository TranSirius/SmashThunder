<template>
  <div class="Content">
    <!-- Friends Activities -->
    <div v-if="user.loggedIn">
      <h2>Friends Activities</h2>
      <hr />
    </div>
    <!-- New posts -->
    <h2>News</h2>
    <hr />
    <b-card-group columns>
      <b-card
        v-for="num in 10"
        :key="num"
        img-src="https://discretetom.github.io/img/me.jpg"
        img-top
      >
        <b-card-title>Blog's Title</b-card-title>
        <b-card-sub-title class="mb-2">Author</b-card-sub-title>
        <b-card-text>{{ "Blog's subtitle and other description.".repeat((Math.floor(Math.random() * 10) + 1)) }}</b-card-text>
        <b-card-text class="small text-muted">
          Last updated {{ Math.floor(Math.random() * 10) + 1 }} mins
          ago
        </b-card-text>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
export default {
  name: "Content",
  props: {
    user: Object
  }
};
</script>