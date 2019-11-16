<template>
  <div>
    <!-- Friends Activities -->
    <div v-if="$root.$data.user.loggedIn">
      <NewsCards title="Friends Activities" :data="friendsActivities"></NewsCards>
    </div>
    <!-- New posts -->
    <NewsCards title="News" :data="news"></NewsCards>
  </div>
</template>

<script>
import NewsCards from "../utils/NewsCards.vue";
import netapi from "../mixin/netapi";

export default {
  name: "News",
  mixins: [netapi],
  components: {
    NewsCards
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