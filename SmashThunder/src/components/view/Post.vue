<template>
  <div>
    <!-- Content -->
    <div>
      <h1>Waiting for WYX to finish latex module.</h1>
      {{ post.content }}
    </div>
    <!-- Comments -->
    <b-card title="Leave a comment" class="mb-2">
      <b-form>
        <b-form-group
          :label="$root.$data.user.username+':'"
          label-for="yourComment"
        >
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
    <b-card v-for="comment in comments" :key="comment.time" class="mb-2">
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
export default {
  name: "Post",
  data() {
    return {
      post: {
        content: "大佬真垃圾".repeat(1000)
      },
      comments: [
        {
          username: "someUser",
          content: "大佬真垃圾".repeat(10),
          time: 123123
        }
      ]
    };
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