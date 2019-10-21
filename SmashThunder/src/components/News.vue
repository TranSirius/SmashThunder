<template>
  <div>
    <!-- Friends Activities -->
    <div v-if="$root.$data.user.loggedIn">
      <h2>Friends Activities</h2>
      <hr />
    </div>
    <!-- New posts -->
    <h2>News</h2>
    <hr />
    <b-card-group columns v-if="news.length">
      <b-card v-for="newPost in news" :key="newPost.time" :img-src="newPost.img" img-top>
        <b-card-title>{{ newPost.title }}</b-card-title>
        <b-card-sub-title class="mb-2">{{ newPost.author }}</b-card-sub-title>
        <b-card-text>{{ newPost.description }}</b-card-text>
        <b-card-text class="small text-muted">
          Posted {{ newPost.time | timeOffset }}
          ago
        </b-card-text>
      </b-card>
    </b-card-group>
    <div v-else>
      <h3>Nothing new.</h3>
    </div>
  </div>
</template>

<script>
export default {
  name: "News",
  data() {
    return { news: [], friendsActivities: [] };
  },
  filters: {
    timeOffset: function(s) {
      var now = new Date(Date.now());
      var t = new Date(parseInt(s));
      var offset = new Date(now - t);
      // different year
      if (offset.getFullYear() - 1970 == 1) return "1 year";
      else if (offset.getFullYear() - 1970 > 0)
        return offset.getFullYear() - 1970 + " years";
      // different month
      else if (offset.getMonth() == 1) return "1 month";
      else if (offset.getMonth() > 0) return offset.getMonth() + " months";
      // different day
      else if (offset.getDate() == 2) return "1 day";
      else if (offset.getDate() > 1) return offset.getDay() - 1 + " days";
      // different hour
      else if (offset.getHours() == 9) return "1 hour";
      else if (offset.getHours() > 8) return offset.getHours() - 8 + "hours";
      // different minutes
      else if (offset.getMinutes() == 1) return "1 minute";
      else if (offset.getMinutes() > 0) return offset.getMinutes() + " minutes";
      // just now
      else return "less than 1 minute";
    }
  }
};
</script>