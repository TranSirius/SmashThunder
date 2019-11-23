<template>
  <div>
    <!-- Content -->
    <div>
      <PostDisplay v-if="post.content" :raw="post.content" :format="post.format"></PostDisplay>
    </div>
    <!-- Comments -->
    <b-card
      title="Leave a comment"
      :sub-title="$root.$data.user.loggedIn?$root.$data.user.username+':':''"
      class="mb-2"
    >
      <b-form @submit.prevent="comment">
        <b-form-group>
          <b-form-textarea
            v-model="text"
            :placeholder="$root.$data.user.loggedIn?'Enter something...':'Please sign in/up first'"
            :disabled="!$root.$data.user.loggedIn"
            rows="3"
            max-rows="6"
            required
          ></b-form-textarea>
        </b-form-group>
        <b-button :disabled="!$root.$data.user.loggedIn" variant="primary" type="submit">Comment</b-button>
      </b-form>
    </b-card>
    <b-card v-for="comment in post.comments" :key="comment.time" class="mb-2">
      <b-card-title>
        <b-link :to="'/'+comment.username">{{ comment.username }}</b-link>
      </b-card-title>
      <b-card-sub-title class="mb-2">Comment at {{ comment.time | timeOffset }} ago.</b-card-sub-title>
      <b-card-text>{{ comment.comment }}</b-card-text>
    </b-card>
    <!-- Action buttons -->
    <b-button-group vertical id="actionBtns">
      <b-button
        :variant="post.followed?'primary':'outline-primary'"
        v-b-tooltip.hover.left
        :title="post.followed?'unfollow':'follow'"
        @click="follow"
      >➕ {{ post.followers }}</b-button>
      <b-button
        @click="downloadPost"
        v-b-tooltip.hover.left
        title="download"
        variant="outline-secondary"
      >⇓</b-button>
      <b-button
        v-if="editable"
        @click="$router.push('/'+$root.$data.user.username+'/edit?folder='+$route.params.folder+'&post='+$route.params.title)"
        variant="outline-info"
        v-b-tooltip.hover.left
        title="edit"
      >✍</b-button>
      <b-button
        :variant="post.starred?'warning':'outline-warning'"
        v-b-tooltip.hover.left
        :title="post.starred?'unstar':'star'"
        @click="star"
      >⭐ {{ post.stars }}</b-button>
      <b-button variant="outline-danger" v-b-tooltip.hover.left title="report">❗</b-button>
    </b-button-group>
  </div>
</template>

<script>
import PostDisplay from "../utils/PostDisplay";
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "Post",
  mixins: [netapi, timeFilter, downloadUtils],
  components: { PostDisplay },
  data() {
    return {
      post: {},
      text: ""
    };
  },
  methods: {
    follow() {
      if (!this.$root.$data.user.loggedIn) {
        this.toastErr("Error", "Please login first.");
        return;
      }
      if (this.$root.$data.user.username == this.$route.params.username) {
        this.toastErr("Error", "You can not follow yourself.");
        return;
      }
      this.apiPost(
        {
          route: "/submit/follow",
          data: {
            target: this.$route.params.username,
            follow: !this.post.followed
          }
        },
        () => {
          this.post.followed = !this.post.followed;
          this.post.followers++;
        },
        "Follow failed."
      );
    },
    star() {
      if (!this.$root.$data.user.loggedIn) {
        this.toastErr("Error", "Please login first.");
        return;
      }
      this.apiPost(
        {
          route: "/submit/star",
          data: {
            username: this.$route.params.username,
            folder: this.post.folder,
            post: this.post.title,
            star: !this.post.starred
          }
        },
        () => {
          this.post.starred = !this.post.starred;
          this.post.stars++;
        },
        "Star failed."
      );
    },
    downloadPost() {
      let username = this.$route.params.username;
      let folder = this.$route.params.folder;
      let post = this.$route.params.title;
      this.apiPost(
        {
          route: "/render",
          data: {
            username,
            folder,
            post,
            format: "pdf"
          }
        },
        data => {
          this.download(
            "/render/" + data.filename,
            `${username}_${folder}_${post}`
          );
        }
      );
    },
    comment() {
      var text = this.text;
      this.apiPost(
        {
          route: "/submit/comment",
          data: {
            folder: this.post.folder,
            post: this.post.title,
            comment: text
          }
        },
        () => {
          this.text = "";
          this.post.comments.push({
            username: this.$route.params.username,
            comment: text,
            time: Date.now()
          });
        }
      );
    },
    enter() {
      if (this.$route.name == "toPost") {
        this.apiPost(
          {
            route: "/get/post",
            data: {
              username: this.$route.params.username,
              folder: this.$route.params.folder,
              postTitle: this.$route.params.title
            }
          },
          data => {
            this.post = data;
          }
        );
      } else {
        this.apiPost(
          {
            route: "/get/mainpage",
            data: {
              username: this.$route.params.username
            }
          },
          data => {
            if (data.exist) {
              this.post = data.post;
            }
          }
        );
      }
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
  },
  computed: {
    editable() {
      return (
        this.$root.$data.user.loggedIn &&
        this.$route.params.username == this.$root.$data.user.username
      );
    }
  }
};
</script>

<style scoped>
#actionBtns {
  position: fixed;
  bottom: 200px;
  right: 100px;
}
</style>