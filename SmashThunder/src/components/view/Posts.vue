<template>
  <div>
    <NewsCards
      v-for="folder in folders"
      :key="folder.title"
      :title="folder.title"
      :data="folder.posts"
    ></NewsCards>
    <h3 v-if="folders.length == 0">No folders here.</h3>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import NewsCards from "../utils/NewsCards";

export default {
  name: "Posts",
  mixins: [netapi],
  components: { NewsCards },
  data() {
    return { folders: [] };
  },
  methods: {
    enter() {
      this.apiPost(
        {
          route: "/get/posts",
          data: { username: this.$route.params.username }
        },
        data => (this.folders = data.folders)
      );
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
  },
  beforeRouteUpdate(to, from, next) {
    next();
    this.enter();
  }
};
</script>