<template>
  <div>
    <!-- Content -->
    <div>
      <PostDisplay :raw="post.content" :format="post.format"></PostDisplay>
    </div>
    <!-- Comments -->
    <b-card title="Leave a comment" class="mb-2">
      <b-form @submit.prevent="comment">
        <b-form-group :label="$root.$data.user.username+':'" label-for="yourComment">
          <b-form-textarea
            id="yourComment"
            v-model="text"
            placeholder="Enter something..."
            rows="3"
            max-rows="6"
          ></b-form-textarea>
        </b-form-group>
        <b-button variant="primary" type="submit">Comment</b-button>
      </b-form>
    </b-card>
    <b-card v-for="comment in post.comments" :key="comment.time" class="mb-2">
      <b-card-title>
        <b-link :to="'/'+comment.username">{{ comment.username }}</b-link>
      </b-card-title>
      <b-card-sub-title class="mb-2">Comment at {{ comment.time }}</b-card-sub-title>
      <b-card-text>{{ comment.content }}</b-card-text>
    </b-card>
    <!-- Action buttons -->
    <b-button-group vertical id="actionBtns">
      <b-button>Follow</b-button>
      <b-button>Download</b-button>
      <b-button>Edit</b-button>
      <b-button>Star</b-button>
      <b-button>Report</b-button>
    </b-button-group>
  </div>
</template>

<script>
import PostDisplay from "../utils/PostDisplay";
import netapi from "../mixin/netapi";

export default {
  name: "Post",
  mixins: [netapi],
  components: { PostDisplay },
  data() {
    return {
      post: {},
      text: ""
    };
  },
  methods: {
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
          this.post.comments.push({
            username: this.$route.params.username,
            content: text,
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