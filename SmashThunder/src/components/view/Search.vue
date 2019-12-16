<template>
  <div>
    <div v-if="users.length">
      <font size='1' style="color:gray">We have found {{users.length}} users below.</font>
      <p></p>
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
        <template v-slot:cell(username)="data">
          <b-link
            :to="'/'+data.item.username"
          >{{ data.item.username }}</b-link>
        </template>
      </b-table>
    </div>
    <!-- <h2 v-else>No users here.</h2> -->
    <div v-if="posts.length">
      <font size='1' style="color:gray">We have found {{posts.length}} posts below.</font>
      <p></p>
      <div v-for="post in this.posts" :key="post">
        <h5><u><b-link
              :to="'/'+post.author+'/posts/'+post.folder+'/'+post.title"
            >{{ post.title }}</b-link></u></h5>
            <font size='2' style="color:green">{{post.author}}《{{post.folder}}》</font>
            <p>{{post.content}}</p>
      </div>
    </div>

    <div v-if="imgs.length">
    <font size='1' style="color:gray">We have found {{imgs.length}} photos below.</font>
      <p></p>
      <b-card-group columns>
        <b-card
              v-for="img in this.imgs"
              :key="img"
              :img-src="img.url"
              :img-alt="img.photoname"
           >
            <b-card-title>{{ img.photoname }}</b-card-title>
            <b-card-sub-title class="mb-2">{{img.album}}</b-card-sub-title>
        </b-card>
      </b-card-group>
      <!-- <b-table
        :items="imgs"
        :fields="imgTable.fields"
        hover
        striped
        sticky-header
        sort-icon-left
        :tbodyTrClass="rowStyle"
        style="min-height:250px"
      >
        <template v-slot:cell(photoname)="data">
          <b-link
            :to="'/'+data.item.photoname"
          >{{ data.item.photoname }}</b-link>
        </template>
        <template v-slot:cell(user)="data">{{ data.item.user }}</template>
        <template v-slot:cell(album)="data">{{ data.item.album }}</template>
      </b-table> -->
    </div>
    <!-- <h2 v-else>No photos here.</h2> -->
    <div v-if="users.length < 1 && posts.length < 1 && imgs.length < 1">
      <div v-if="isSearchBoxEmpty">
        <h2>Your search box is empty.</h2>
      </div>
      <div v-else>
        <h2>Nothing found.</h2>
      </div>
      </div>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "Search",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  data() {
    return {
      table: {
        fields: [{ key: "username", sortable: true }]
      },
      postTable: {
        fields: [
          { key: "title", sortable: true },
          { key: "author", sortable: true },
          { key: "folder", sortable: true },
          ]
      },
      imgTable: {
        fields: [
          { key: "photoname", sortable: true },
          { key: "user", sortable: true },
          { key: "album", sortable: true },
          ]
      },
      users: [],
      posts: [],
      imgs: [],
      isSearchBoxEmpty: false
    };
  },
  methods: {
    enter() {
      if(this.$route.query.keyword.length < 1){
        this.users = [];
        this.posts = [];
        this.imgs = [];
        this.isSearchBoxEmpty = true;
        return;
      }
      this.isSearchBoxEmpty = false;
      this.apiPost(
        {
          route: "/search/user",
          data: {
            keyword: this.$route.query.keyword,
            scroll_id:""
          }
        },
        data => {
          this.users = [];
          for (let i = 0; i < data.username.length; ++i) {
            this.users.push(data.username[i]);
          }
        },
        "Get users error"
      );
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
          // windows.console.log("hereposts");
        },
        "Get posts error"
      );
      this.apiPost(
        {
          route: "/search/img",
          data: {
            keyword: this.$route.query.keyword,
            scroll_id:""
          }
        },
        data => {
          this.imgs = [];
          for (let i = 0; i < data.photo.length; ++i) {
            this.imgs.push(data.photo[i]);
            this.imgs[i].url = '/data/' + this.imgs[i].user + '/img/'
            + this.imgs[i].album + '/' + this.imgs[i].photoname;
          }
          // windows.console.log("hereimgs");
        },
        "Get photos error"
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