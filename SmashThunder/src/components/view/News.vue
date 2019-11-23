<template>
  <div>
    <!-- Friends Activities -->
    <div v-if="$root.$data.user.loggedIn">
      <PostOverview
        title="Friends Activities"
        :data="friendsActivities"
        emptyHint="No friends activities."
      ></PostOverview>
    </div>
    <!-- New posts -->
    <PostOverview title="News" :data="news" emptyHint="No news."></PostOverview>
  </div>
</template>

<script>
import PostOverview from "../utils/PostOverview.vue";
import netapi from "../mixin/netapi";

export default {
  name: "News",
  mixins: [netapi],
  components: {
    PostOverview
  },
  data() {
    return {
      news: [],
      friendsActivities: []
    };
  },
  watch: {
    "$root.$data.user.loggedIn": function(val) {
      if (val) {
        this.getFriendsActivities();
      }
    }
  },
  methods: {
    getNews() {
      this.apiPost(
        { route: "/get/news", data: { target: "news" } },
        data => (this.news = data.posts),
        "Can't load news!"
      );
    },
    getFriendsActivities() {
      this.apiPost(
        { route: "/get/news", data: { target: "friendsActivities" } },
        data => (this.friendsActivities = data.posts),
        "Can't load friends activities!"
      );
    }
  },
  beforeRouteEnter: (from, to, next) => {
    next(v => {
      v.getNews();
      if (v.$root.$data.user.loggedIn) v.getFriendsActivities();
    });
  }
};
</script>