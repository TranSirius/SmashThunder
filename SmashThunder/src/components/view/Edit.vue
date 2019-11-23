<template>
  <div>
    <!-- edit post form -->
    <b-form @submit.prevent="submit(true)" class="mb-3">
      <!-- row 1, post title, file format, folder -->
      <b-form-row>
        <b-col cols="6">
          <b-form-group label="Post title" label-for="postTitle">
            <b-form-input
              id="postTitle"
              v-model="form.title"
              placeholder="Please input the post title"
              required
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
              required
            ></NewableSelect>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!-- row 2, description, cover image -->
      <b-form-row>
        <b-col cols="6">
          <b-form-group label="Post description(optional)" label-for="postDescription">
            <b-form-input
              id="postDescription"
              v-model="form.description"
              placeholder="Post description"
              required
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="3">
          <b-form-group label="Cover image album(optional)">
            <b-form-select v-model="form.selectedAlbum" :options="form.albumTitles"></b-form-select>
          </b-form-group>
        </b-col>
        <b-col cols="3">
          <b-form-group label="Cover image title(optional)">
            <b-form-select v-model="form.selectedImage" :options="form.imageTitles"></b-form-select>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!-- row 3, post content, realtime renderer -->
      <b-form-row>
        <b-col cols="6">
          <b-form-group class="h-100" label="Post Content" label-for="textarea">
            <b-form-textarea
              id="textarea"
              v-model="form.text"
              placeholder="Enter something or drop a file..."
              no-resize
              rows="20"
              style="height:500px"
              @drop.prevent="dropFile"
            ></b-form-textarea>
            <template v-slot:description>
              You can use
              <pre style="display:inline">![title](album/img.png)</pre>to reference your images.
            </template>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group label="Realtime Renderer">
            <b-card style="height:500px;overflow-y:scroll" no-body>
              <PostDisplay :raw="form.text" :format="form.format"></PostDisplay>
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
        text: "",
        title: "",
        description: "",
        format: "md",
        folder: "",
        folders: [],
        newFolderHint: "-- create a new folder --",
        selectedImage: "",
        selectedAlbum: "",
        albumTitles: [],
        imageTitles: []
      }
    };
  },
  methods: {
    // ref: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
    // ref: https://developer.mozilla.org/zh-CN/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
    dropFile(e) {
      let droppedFiles = e.dataTransfer.files;
      for (let i = 0; i < droppedFiles.length; ++i) {
        if (this.form.text)
          this.toastErr(
            "Can not drop file",
            "Please delete post content first."
          );
        this.form.title = droppedFiles[i].name
          .split(".")
          .slice(0, -1)
          .join(".");
        if (
          droppedFiles[i].name.endsWith("html") ||
          droppedFiles[i].name.endsWith("md")
        )
          this.form.format = "md";
        else if (droppedFiles[i].name.endsWith("tex")) this.form.format = "tex";
        droppedFiles[i].text().then(t => (this.form.text = t));
        break; // only load one file
      }
    },
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
            published: publish,
            description: this.form.description,
            coverAlbum: this.form.selectedAlbum,
            coverImage: this.form.selectedImage
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
            if (
              this.form.folders.filter(v => v.title == this.$route.query.folder)
            )
              this.form.folder = this.$route.query.folder;
          }
          // edit existing post
          if (this.$route.query.post) {
            this.apiPost(
              {
                route: "/get/post",
                data: {
                  username: this.$route.params.username,
                  folder: this.$route.query.folder,
                  postTitle: this.$route.query.post
                }
              },
              data => {
                this.form.text = data.content;
                this.form.format = data.format;
                this.form.title = this.$route.query.post;
              }
            );
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
