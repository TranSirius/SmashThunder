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
import axios from "axios";

export default {
  name: "News",
  components: {
    NewsCards
  },
  data() {
    return {
      news: [],
      friendsActivities: []
    };
  },
  methods: {
    getNews() {
      axios.post("/get/news", { target: "news" }).then(
        res => {
          if (res.data.status == "ok") this.news = res.data.posts;
        },
        () => {}
      );
    },
    getFriendsActivities() {
      axios.post("/get/news", { target: "friendsActivities" }).then(
        res => {
          if (res.data.status == "ok") this.friendsActivities = res.data.posts;
        },
        () => {}
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