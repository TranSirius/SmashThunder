<template>
  <div>
    <!-- edit post form -->
    <b-form @submit="submit" style="height:500px">
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
            <b-form-select id="postFolder" v-model="form.folder" :options="folderOptions" required></b-form-select>
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
              <b-card-body v-html="resultHTML" style="overflow:scroll"></b-card-body>
            </b-card>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <!-- new folder form -->
    <!-- TODO: optimize this modal form to a component -->
    <b-modal ref="newFolderForm" title="Please enter the new folder's name" centered hide-footer>
      <b-form @submit.prevent="newFolder">
        <b-form-group>
          <b-form-input v-model="form.newFolder" placeholder="New folder name"></b-form-input>
        </b-form-group>
        <b-button variant="primary" type="submit" block>OK</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import showdown from "showdown";
import axios from "axios";
import errHandler from "../mixin/errHandler";

var converter = new showdown.Converter();

export default {
  name: "Edit",
  mixins: [errHandler],
  data() {
    return {
      form: {
        text: "# Markdown Here",
        title: "",
        format: "md",
        folder: "",
        folders: [],
        newFolder: "",
        newFolderHint: "-- create a new folder --"
      }
    };
  },
  methods: {
    submit() {},
    newFolder() {
      // test duplication
      for (let i = 0; i < this.folderOptions.length; i++)
        if (this.folderOptions[i] == this.newFolder) {
          this.toastErr("Error!", "Duplicate folder name!");
          return;
        }
      // test validation
      if (this.form.newFolder == this.form.newFolderHint) {
        this.toastErr("Error!", "Invalid folder name!");
        return;
      }
      // ok
      this.form.folders.push({ title: this.form.newFolder, posts: [] });
      this.form.folder = this.form.newFolder;
      this.$refs.newFolderForm.hide();
    },
    showGetFoldersErr(s) {
      this.toastErr("Error when getting folders", s);
    },
    enter() {
      axios
        .post("/get/post/folders")
        .then(res => {
          if (res.data.status == "ok") {
            if (res.data.folders.length) {
              this.form.folder = res.data.folders[0];
              this.form.folders = res.data.folders;
            } else {
              this.$refs.newFolderForm.show();
            }
          } else {
            this.showGetFoldersErr(res.data.status);
          }
        })
        .catch(() => this.showGetFoldersErr());
    }
  },
  computed: {
    resultHTML() {
      return converter.makeHtml(this.form.text);
    },
    folderOptions() {
      var result = [this.form.newFolderHint];
      this.form.folders.map(v => result.push(v.title));
      return result;
    }
  },
  watch: {
    "form.folder": function() {
      if (this.form.folder == this.form.newFolderHint) {
        this.form.newFolder = "";
        this.$refs.newFolderForm.show();
      }
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