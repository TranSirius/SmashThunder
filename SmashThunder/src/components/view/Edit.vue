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
              <option value="lex">LaTeX(lex)</option>
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
            <b-card id = "card" style="height:500px" no-body>
              <b-card-body id = "cardBody" v-if="form.format=='md' || form.format=='lex'" v-html="resultHTML" style="overflow:scroll">
              </b-card-body>
            </b-card>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
import showdown from "showdown";
import axios from "axios";
import errHandler from "../mixin/errHandler";
import NewableSelect from "../utils/NewableSelect";
import { parse, HtmlGenerator } from "latex.js";

var converter = new showdown.Converter();
var generator = new HtmlGenerator({
    hyphenate: true,
    languagePatterns: 'en'
})



export default {
  name: "Edit",
  mixins: [errHandler],
  components: { NewableSelect },
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
    submit() {},
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
              this.form.folder = this.form.newFolderHint;
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
      
      if (this.form.format == "md"){
        var inHtml = converter.makeHtml(this.form.text);
        return inHtml;
      } 
      else {
        try {
          generator.reset();
          var doc = parse(this.form.text, { generator: generator }).htmlDocument();
          doc.body.appendChild(generator.stylesAndScripts("https://cdn.jsdelivr.net/npm/latex.js@0.11.1/dist/"));
          doc.body.appendChild(generator.domFragment());
          return doc.documentElement.outerHTML;
        } catch (e) {
          return e.message;
        }
      }
    },
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