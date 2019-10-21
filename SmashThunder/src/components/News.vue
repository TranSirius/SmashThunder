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
import NewsCards from "./NewsCards.vue";

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
  }
};
</script>