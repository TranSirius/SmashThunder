<template>
  <div>
    <div v-if="stars.length">
      <h2>{{$route.params.username}}</h2>
      <h6>Edit your star posts here.</h6>
      <b-table
        :items="stars"
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
            :to="'/'+data.item.username+'/posts/'+data.item.folder+'/'+data.item.post"
          >{{ data.item.post }}</b-link>
        </template>
        <template v-slot:cell(author)="data">{{ data.item.username }}</template>
        <template v-slot:cell(folder)="data">{{ data.item.folder }}</template>
        <template v-slot:cell(actions)="data">
          <b-button
            class="mb-1"
            variant="danger"
            @click="deleteStar(data.item.username, data.item.folder, data.item.post)"
          >Delete</b-button>
        </template>
      </b-table>
    </div>
    <h2 v-else>No stars here.</h2>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
// import ModalInput from "../utils/ModalInput";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "Star",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  data() {
    return {
      table: {
        fields: [
          { key: "title", sortable: true },
          { key: "author", sortable: true },
          { key: "folder", sortable: true },
          "actions"
        ]
      },
      stars: []
    };
  },
  methods: {
    enter() {
      this.apiPost(
        {
          route: "/get/star",
          data: {
            username: this.$route.params.username
          }
        },
        data => {
          this.stars = data.stars;
        },
        "",
        () => this.to404()
      );
    },
    deleteStar(author, folder, post) {
      this.apiPost(
        {
          route: "/submit/star",
          data: {
            username: author,
            folder: folder,
            post: post,
            star: false
          }
        },
        () => {
          for (let i = 0; i < this.stars.length; ++i) {
            if (
              this.stars[i].post == post &&
              this.stars[i].folder == folder &&
              this.stars[i].username == author
            ) {
              this.stars = this.stars.filter(s => {
                return (
                  s.folder != folder && s.post != post && s.username != author
                );
              });
              return;
            }
          }
        }
        //"unstar error"
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