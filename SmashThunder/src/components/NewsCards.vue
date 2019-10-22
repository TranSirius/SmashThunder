<template>
  <div>
    <h2>{{ title }}</h2>
    <hr />
    <b-card-group columns v-if="data.length">
      <b-card v-for="post in data" :key="post.time" :img-src="post.img" img-top>
        <b-card-title>{{ post.title }}</b-card-title>
        <b-card-sub-title class="mb-2">{{ post.author }}</b-card-sub-title>
        <b-card-text>{{ post.description }}</b-card-text>
        <b-card-text class="small text-muted">
          Posted {{ post.time | timeOffset }}
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
  name: "NewsCards",
  props: {
    title: String,
    data: Array
  },
  filters: {
    timeOffset: function(s) {
      var now = new Date(Date.now());
      var t = new Date(s);
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