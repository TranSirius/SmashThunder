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
  }
};
</script>