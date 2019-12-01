<template>
  <div>
    <div v-if="followers.length">
      <h2>{{$route.params.username}}'s followers</h2>
      <b-button
        class="mb-1 ml-3"
        variant="outline-info"
        :pressed.sync="followerShow"
      >{{ followerShow ? 'Hide' : 'Show' }}</b-button>
      <h6>You can find your followers here.</h6>
      <b-collapse v-model="followerShow">
        <b-table
          :items="followers"
          :fields="table1.fields"
          hover
          striped
          sticky-header
          sort-icon-left
          :tbodyTrClass="rowStyle"
          style="min-height:250px"
        >
          <template v-slot:cell(follower)="data">
            <b-link :to="'/'+$route.params.username">{{ data.item }}</b-link>
          </template>
          <template v-slot:cell(actions)="data">
            <b-button class="mb-1" variant="danger" @click="unfollow(data.item)">Delete</b-button>
          </template>
        </b-table>
      </b-collapse>
    </div>
    <h2 v-else>No followers.</h2>

    <div v-if="followings.length">
      <h2>{{$route.params.username}}'s followings</h2>
      <b-button
        class="mb-1 ml-3"
        variant="outline-info"
        :pressed.sync="followings.show"
      >{{ followings.show ? 'Hide' : 'Show' }}</b-button>
      <h6>You can find your followings here.</h6>
      <b-collapse v-model="followingShow">
        <b-table
          :items="followings"
          :fields="table2.fields"
          hover
          striped
          sticky-header
          sort-icon-left
          :tbodyTrClass="rowStyle"
          style="min-height:250px"
        >
          <template v-slot:cell(following)="data">
            <b-link :to="'/'+$route.params.username">{{ data.item }}</b-link>
          </template>
        </b-table>
      </b-collapse>
    </div>
    <h2 v-else>No followings.</h2>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
import ModalInput from "../utils/ModalInput";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "Star",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  data() {
    return {
      table1: {
        fields: [{ key: "follower", sortable: true }, "actions"]
      },
      table2: {
        fields: [{ key: "following", sortable: true }]
      },
      followers: [],
      followings: [],
      followerShow: true,
      followingShow: true
    };
  },
  methods: {
    enter() {
      this.apiPost(
        {
          route: "/get/follow",
          data: {
            username: this.$route.params.username
          }
        },
        data => {
          this.followers = data.followers;
          this.followings = data.followings;
        },
        "Get stars error"
      );
    },
    unfollow(unfollowName) {
      this.apiPost(
        {
          route: "/follow",
          data: {
            target: unfollowName,
            star: false
          }
        },
        () => {
          for (let i = 0; i < this.followers.length; ++i) {
            if (this.followers[i] == unfollowName) {
              this.followers = this.followers.filter(s => {
                return s != unfollowName;
              });
              return;
            }
          }
        },
        "Get stars error"
      );
    }
  }
};
</script>