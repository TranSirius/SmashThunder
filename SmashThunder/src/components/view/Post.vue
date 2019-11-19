<template>
  <div>
    <!-- Content -->
    <div>
      <PostDisplay :raw="post.content" :format="post.format"></PostDisplay>
    </div>
    <!-- Comments -->
    <b-card title="Leave a comment" :sub-title="$root.$data.user.username+':'" class="mb-2">
      <b-form @submit.prevent="comment">
        <b-form-group>
          <b-form-textarea v-model="text" placeholder="Enter something..." rows="3" max-rows="6"></b-form-textarea>
        </b-form-group>
        <b-button variant="primary" type="submit">Comment</b-button>
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
      <b-button>Follow</b-button>
      <b-button @click="downloadPost">Download</b-button>
      <b-button>Edit</b-button>
      <b-button>Star</b-button>
      <b-button>Report</b-button>
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
            folder: this.$route.params.folder,
            post: this.$route.params.title,
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
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
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