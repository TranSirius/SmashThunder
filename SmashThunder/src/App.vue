<template>
  <div id="app">
    <Header></Header>
    <!-- Main content -->
    <b-container>
      <router-view></router-view>
    </b-container>
  </div>
</template>

<script>
import Header from "./components/Header.vue";

export default {
  name: "app",
  components: {
    Header,
  }
};
</script>