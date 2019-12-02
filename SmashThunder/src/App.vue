<template>
  <div id="app">
    <Header></Header>
    <!-- Main content, the top margin is to leave space for nav bar -->
    <b-container style="margin-top:80px">
      <router-view></router-view>
    </b-container>
    <br />
    <b-navbar>
      <b-nav-text class="text-center w-100" id="footer">京ICP备19053534</b-nav-text>
    </b-navbar>
  </div>
</template>

<script>
import Header from "./components/Header.vue";

export default {
  name: "app",
  components: {
    Header
  }
};
</script>

<style scoped>
#footer {
  background-color: #fff;
  position: fixed;
  bottom: 0;
}
</style>