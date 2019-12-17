<template>
  <div>
    <PostOverview
      v-for="folder in folders"
      :key="folder.title"
      :title="folder.title"
      :data="folder.posts"
    ></PostOverview>
    <h3 v-if="folders.length == 0">No folders here.</h3>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import PostOverview from "../utils/PostOverview";

export default {
  name: "Posts",
  mixins: [netapi],
  components: { PostOverview },
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
        data => {
          this.folders = data.folders;
          this.folders.map(folder => {
            folder.posts.map(post => (post.folder = folder.title));
          });
        }
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