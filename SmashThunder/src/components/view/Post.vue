<template>
  <div>
    <!-- Content -->
    <div>
      <PostDisplay v-if="post.content" :raw="post.content" :format="post.format"></PostDisplay>
    </div>
    <!-- New comment card -->
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
    <!-- Comments -->
    <b-card v-for="comment in post.comments" :key="comment.time" class="mb-2">
      <b-card-title>
        <b-link :to="'/'+comment.username">{{ comment.username }}</b-link>
        <b-button
          variant="outline-danger"
          v-b-tooltip.hover
          title="report"
          @click="triggerReport(comment.username)"
          size="sm"
          class="ml-3 mb-2"
        >❗</b-button>
        <b-button
          v-if="editable"
          variant="outline-secondary"
          v-b-tooltip.hover
          title="remove this comment"
          size="sm"
          class="mb-2 ml-2"
          @click="deleteComment(comment.ID)"
        >❌</b-button>
      </b-card-title>
      <b-card-sub-title class="mb-2">Comment at {{ comment.time | timeOffset }} ago.</b-card-sub-title>
      <b-card-text>{{ comment.comment }}</b-card-text>
    </b-card>
    <!-- btns -->
    <div id="btnGroup">
      <b-button-group vertical>
        <!-- homepage only buttons -->
        <b-button
          v-if="$route.name=='toMainPage'"
          variant="outline-info"
          v-b-tooltip.hover.left
          title="See his/her followers"
          @click="$router.push('/'+$route.params.username+'/follow')"
        >➕</b-button>
        <b-button
          v-if="$route.name=='toMainPage'"
          variant="outline-info"
          v-b-tooltip.hover.left
          title="See his/her stars"
          @click="$router.push('/'+$route.params.username+'/star')"
          class="mb-3"
        >⭐</b-button>
        <!-- Action buttons -->
        <b-button
          :variant="post.followed?'success':'outline-success'"
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
        <b-button
          variant="outline-danger"
          v-b-tooltip.hover.left
          title="report"
          @click="triggerReport()"
        >❗</b-button>
      </b-button-group>
    </div>
    <ReportModal
      :target="report.target"
      :reporter="$root.$data.user.username"
      :reason="report.reason"
      ref="reportModal"
    ></ReportModal>
  </div>
</template>

<script>
import PostDisplay from "../utils/PostDisplay";
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import downloadUtils from "../mixin/downloadUtils";
import ReportModal from "../utils/ReportModal";

export default {
  name: "Post",
  mixins: [netapi, timeFilter, downloadUtils],
  components: { PostDisplay, ReportModal },
  data() {
    return {
      post: {},
      text: "",
      report: {
        reason: "",
        target: ""
      }
    };
  },
  methods: {
    deleteComment(commentId) {
      this.apiPost(
        {
          route: "/admin/comment/delete/author",
          data: { id: commentId }
        },
        () =>
          (this.post.comments = this.post.comments.filter(
            c => c.ID !== commentId
          )),
        "Delete comment failed."
      );
    },
    triggerReport(commenter) {
      if (!this.$root.$data.user.loggedIn) {
        this.toastErr("Error", "Please login first.");
        return;
      }
      this.report.target = commenter || this.$route.params.username;
      this.report.reason = commenter
        ? "Target comment: " + this.report.target + " in "
        : "Target post: ";
      this.report.reason +=
        [
          this.$route.params.username,
          this.post.folder || this.$route.params.folder,
          this.post.title || this.$route.params.title
        ].join("/") + "\n";
      this.$refs.reportModal.show();
    },
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
          if (this.post.followed) this.post.followers++;
          else this.post.followers--;
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
            folder: this.post.folder || this.$route.params.folder,
            post: this.post.title || this.$route.params.title,
            star: !this.post.starred
          }
        },
        () => {
          this.post.starred = !this.post.starred;
          if (this.post.starred) this.post.stars++;
          else this.post.stars--;
        },
        "Star failed."
      );
    },
    downloadPost() {
      let username = this.$route.params.username;
      let folder = this.post.folder || this.$route.params.folder;
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
            username: this.$route.params.username,
            folder: this.post.folder || this.$route.params.folder,
            post: this.post.title || this.$route.params.title,
            comment: text
          }
        },
        () => {
          this.text = "";
          this.post.comments.unshift({
            username: this.$root.$data.user.username,
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
              folder: this.post.folder || this.$route.params.folder,
              postTitle: this.$route.params.title
            }
          },
          data => {
            this.post = data;
            this.post.comments.sort((a, b) => {
              return b.time - a.time;
            });
          },
          "",
          () => this.to404()
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
            } else {
              to404();
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
#btnGroup {
  position: fixed;
  right: 3%;
  bottom: 10%;
}
</style>
