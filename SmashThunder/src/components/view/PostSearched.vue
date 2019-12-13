<template>
  <div>
    <!-- <h6>Find users below.</h6> -->
    <div v-if="users.length">
      <h6>Find posts below.</h6>
      <b-table
        :items="users"
        :fields="table.fields"
        hover
        striped
        sticky-header
        sort-icon-left
        :tbodyTrClass="rowStyle"
        style="min-height:250px"
      >
        <template v-slot:cell(title)="data">
          <b-link
            :to="'/'+data.item.author+'/posts/'+data.item.folder+'/'+data.item.title"
          >{{ data.item.title }}</b-link>
        </template>
        <template v-slot:cell(author)="data">{{ data.item.author }}</template>
        <template v-slot:cell(folder)="data">{{ data.item.folder }}</template>
      </b-table>
    </div>
    <h2 v-else>No users here.</h2>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "PostSearched",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  data() {
    return {
      table: {
        fields: [
          { key: "title", sortable: true },
          { key: "author", sortable: true },
          { key: "folder", sortable: true },
          ]
      },
      posts: []
    };
  },
  methods: {
    enter() {
      this.apiPost(
        {
          route: "/search/post",
          data: {
            keyword: this.$route.query.keyword,
            scroll_id:""
          }
        },
        data => {
          this.posts = [];
          for (let i = 0; i < data.posts.length; ++i) {
            this.posts.push(data.posts[i]);
          }
        },
        "Get posts error"
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