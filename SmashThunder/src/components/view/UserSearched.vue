<template>
  <div>
    <div v-if="users.length">
      <h6>Find users below.</h6>
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
            :to="'/'+data.item"
          >{{ data.item }}</b-link>
        </template>
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
  name: "UserSearched",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  data() {
    return {
      table: {
        fields: [{ key: "username", sortable: true }]
      },
      users: []
    };
  },
  methods: {
    enter() {
      this.apiPost(
        {
          route: "/search/user",
          data: {
            keyword: this.$route.params.keyword
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