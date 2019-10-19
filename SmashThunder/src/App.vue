<template>
  <div id="app">
    <Header :user="userData"></Header>
    <!-- Main content -->
    <b-container>
      <Content></Content>
    </b-container>
  </div>
</template>

<script>
import Content from "./components/Content.vue";
import Header from "./components/Header.vue";

export default {
  name: "app",
  components: {
    Header,
    Content
  },
  data() {
    return {
      userData: {
        username: "",
        password: "",
        loggedIn: false
      }
    };
  }
};
</script>