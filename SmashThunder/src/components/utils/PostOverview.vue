<template>
  <div>
    <h2>{{ title }}</h2>
    <hr />
    <b-card-group columns v-if="data.length">
      <b-card
        v-for="post in data"
        :key="post.time"
        :img-src="'/data/'+post.author+'/img/'+post.coverAlbum+'/'+post.coverImage"
        img-top
      >
        <b-card-title>
          <b-link :to="'/'+post.author+'/posts/'+post.folder+'/'+post.title">{{ post.title }}</b-link>
        </b-card-title>
        <b-card-sub-title class="mb-2">
          <b-link :to="'/'+post.author">{{ post.author }}</b-link>
        </b-card-sub-title>
        <b-card-text>
          <b-link :to="'/'+post.author+'/posts/'+post.folder+'/'+post.title">{{ post.description }}</b-link>
        </b-card-text>
        <b-card-text class="small text-muted">
          Posted {{ post.time | timeOffset }}
          ago
        </b-card-text>
      </b-card>
    </b-card-group>
    <div v-else>
      <h3>{{emptyHint||'Nothing here.'}}</h3>
    </div>
  </div>
</template>

<script>
import timeFilter from "../mixin/timeFilter";

export default {
  name: "PostOverview",
  mixins: [timeFilter],
  props: {
    title: String,
    data: Array,
    emptyHint: String
  }
};
</script>

<style scoped>
a {
  color: inherit;
}
</style>