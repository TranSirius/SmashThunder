<template>
  <div>
    <h1>404 Not Found</h1>
    <h2>Will jump to index page in {{ countDown }}s.</h2>
  </div>
</template>

<script>
export default {
  name: "Page404",
  data() {
    return {
      countDown: 3
    };
  },
  methods: {
    enter() {
      this.toIndex();
    },
    toIndex() {
      if (this.countDown) {
        this.countDown--;
        setTimeout(this.toIndex);
      } else {
        this.$router.push("/");
      }
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
  }
};
</script>