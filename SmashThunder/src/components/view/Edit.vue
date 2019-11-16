<template>
  <div>
    <!-- edit post form -->
    <b-form @submit.prevent="submit(true)" style="height:500px">
      <b-form-row>
        <b-col cols="6">
          <b-form-group label="Post title" label-for="postTitle">
            <b-form-input
              id="postTitle"
              v-model="form.title"
              placeholder="Please input the post title"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="3">
          <b-form-group label="File format" label-for="fileFormat">
            <b-form-select id="fileFormat" v-model="form.format" required>
              <option value="md">Markdown(md)</option>
              <option value="tex">LaTeX(tex)</option>
            </b-form-select>
          </b-form-group>
        </b-col>
        <b-col cols="3">
          <b-form-group label="Folder" label-for="postFolder">
            <NewableSelect
              id="postFolder"
              v-model="form.folder"
              :options="folderOptions"
              :hint="form.newFolderHint"
              modalTitle="Please enter the new folder's name"
              modalPlaceholder="New folder name"
            ></NewableSelect>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-form-group class="h-100" label="Post Content" label-for="textarea">
            <b-form-textarea
              id="textarea"
              v-model="form.text"
              placeholder="Enter something..."
              no-resize
              rows="20"
              style="height:500px"
            ></b-form-textarea>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Realtime Render">
            <b-card style="height:500px" no-body>
              <b-card-body style="overflow:scroll">
                <PostDisplay :raw="form.text" :format="form.format"></PostDisplay>
              </b-card-body>
            </b-card>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-button type="submit" variant="primary">Publish</b-button>
      <b-button class="ml-2" type="button" variant="secondary" @click="submit(false)">Save As Draft</b-button>
    </b-form>
  </div>
</template>

<script>
import errHandler from "../mixin/errHandler";
import NewableSelect from "../utils/NewableSelect";
import strCheck from "../mixin/strCheck";
import PostDisplay from "../utils/PostDisplay";
import netapi from "../mixin/netapi";

export default {
  name: "Edit",
  mixins: [errHandler, strCheck, netapi],
  components: { NewableSelect, PostDisplay },
  data() {
    return {
      form: {
        text: "# Markdown Here",
        title: "",
        format: "md",
        folder: "",
        folders: [],
        newFolderHint: "-- create a new folder --"
      }
    };
  },
  methods: {
    submit(publish) {
      if (!this.checkFileName(this.form.title)) {
        this.toastErr(
          "Submit failed",
          "Post title can not contain special chars."
        );
        return;
      }
      if (this.form.title.length > 500) {
        this.toastErr(
          "Submit failed",
          "Post title can not be longer than 500 characters."
        );
        return;
      }
      if (this.form.folder.length > 200) {
        this.toastErr(
          "Submit failed",
          "Folder title can not be longer than 200 characters"
        );
        return;
      }
      if (!this.checkFileName(this.form.folder)) {
        this.toastErr(
          "Submit failed",
          "Folder title can not contain special chars"
        );
        return;
      }
      this.apiPost(
        {
          route: "/submit/post",
          data: {
            title: this.form.title,
            folder: this.form.folder,
            format: this.form.format,
            content: this.form.text,
            published: publish
          }
        },
        () => {
          if (publish) {
            // redirect page to the post
            this.$router.push(
              "/" +
                this.$root.$data.user.username +
                "/posts/" +
                this.form.folder +
                "/" +
                this.form.title
            );
          } else {
            this.toastErr(
              "Succeed",
              "Your post has been saved successfully.",
              "success"
            );
          }
        },
        "Create post error"
      );
    },
    enter() {
      this.apiPost(
        { route: "/get/post/folders" },
        data => {
          if (data.folders.length) {
            this.form.folder = data.folders[0].title;
            this.form.folders = data.folders;
          } else {
            this.form.folder = this.form.newFolderHint;
          }
          // to designated folder
          if (this.$route.query.folder) {
            if (this.folders.filter(v => v.title == this.$route.query.folder))
              this.folder = this.$route.query.folder;
          }
        },
        "Error when getting folders"
      );
    }
  },
  computed: {
    folderOptions() {
      var result = [];
      this.form.folders.map(v => result.push(v.title));
      return result;
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
