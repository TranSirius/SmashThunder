<template>
  <div>
    <div v-for="folder in folders" :key="folder.title">
      <!-- Folder title and action buttons -->
      <h2>
        {{ folder.title }}
        <b-dropdown split text="Rename" class="mb-1 ml-3" variant="secondary" v-if="editable">
          <b-dropdown-item variant="danger">Delete</b-dropdown-item>
        </b-dropdown>
        <b-button
          class="mb-1 ml-3"
          variant="outline-info"
          :pressed.sync="folder.show"
        >{{ folder.show ? 'Hide' : 'Show' }}</b-button>
      </h2>
      <!-- Posts table -->
      <b-table
        :items="folder.posts"
        :fields="table.fields"
        hover
        striped
        sticky-header
        sort-icon-left
        :tbodyTrClass="rowStyle"
      >
        <template v-slot:cell(title)="data">
          <b-link :to="'/'+$route.params.username+'/posts/'+data.item.title">{{ data.item.title }}</b-link>
        </template>
        <template v-slot:cell(format)="data">{{ data.item.format=='md'?'Markdown':'Latex' }}</template>
        <template v-slot:cell(createTime)="data">{{ data.item.createTime | peekDate }}</template>
        <template v-slot:cell(published)="data">{{ data.item.published ? 'Yes' : 'No' }}</template>
        <template v-slot:cell(actions)="data">
          <b-button size="sm" variant="primary">{{ data.item.published ? 'Withdraw' : 'Publish'}}</b-button>
          <b-button size="sm" class="ml-2" variant="outline-danger">Delete</b-button>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import errHandler from "../mixin/errHandler";
import timeFilter from "../mixin/timeFilter";
import axios from "axios";

export default {
  name: "Posts",
  mixins: [errHandler, timeFilter],
  data() {
    return {
      table: {
        fields: [
          { key: "title", sortable: true },
          { key: "createTime", label: "Created At", sortable: true },
          { key: "format", sortable: true },
          { key: "published", sortable: true },
          { key: "stars", sortable: true },
          { key: "comments", sortable: true },
          "actions"
        ]
      },
      folders: []
    };
  },
  methods: {
    rowStyle(item) {
      if (item.published) {
        return "table-success";
      }
    },
    enter() {
      axios
        .post("/get/post/foldersDetail")
        .then(res => {
          if (res.data.status == "ok") {
            this.folders = res.data.folders;
          } else this.toastErr("Get posts error", res.data.status);
        })
        .catch(() => {
          this.toastErr("Get posts error");
        });
    }
  },
  computed: {
    editable() {
      return (
        this.$root.$data.user.loggedIn &&
        this.$root.$data.user.username == this.$route.params.username
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