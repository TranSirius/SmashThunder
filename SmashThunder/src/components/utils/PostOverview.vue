<template>
  <div>
    <h2>{{ title }}</h2>
    <hr />
    <b-card-group columns v-if="data.length">
      <b-card
        v-for="post in data"
        :key="post.time"
        no-body
        class="hoverCard"
        @click="$router.push('/'+post.author+'/posts/'+post.folder+'/'+post.title)"
      >
        <b-card-img
          v-if="post.coverImage"
          :src="'/data/'+post.author+'/img/'+post.coverAlbum+'/'+post.coverImage"
          top
        ></b-card-img>
        <b-card-body>
          <b-card-title>
            <b-link :to="'/'+post.author+'/posts/'+post.folder+'/'+post.title">{{ post.title }}</b-link>
          </b-card-title>
          <b-card-sub-title class="mb-2">
            <b-link :to="'/'+post.author">{{ post.author }}</b-link>
          </b-card-sub-title>
          <b-card-text>{{ post.description }}</b-card-text>
          <b-card-text class="small text-muted">
            Posted {{ post.time | timeOffset }}
            ago
          </b-card-text>
        </b-card-body>
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
.hoverCard:hover {
  cursor: pointer;
  border-color: #bdbdbd;
  transition: all 0.2s;
}
</style>