<template>
  <div>
    <div v-if="folders.length">
      <div v-for="folder in folders" :key="folder.title">
        <!-- Folder title and action buttons -->
        <h2>
          {{ folder.title }}
          <b-dropdown
            split
            text="Rename"
            class="mb-1 ml-3"
            variant="secondary"
            v-if="editable"
            @click="showRenameForm(folder.title)"
          >
            <b-dropdown-item variant="danger" @click="deletePostOrFolder(folder.title)">Delete</b-dropdown-item>
          </b-dropdown>
          <b-button
            class="mb-1 ml-3"
            variant="outline-info"
            :pressed.sync="folder.show"
          >{{ folder.show ? 'Hide' : 'Show' }}</b-button>
        </h2>
        <h6>Created at {{ folder.createdTime | peekDate }}.</h6>
        <!-- Posts table -->
        <b-collapse v-model="folder.show">
          <b-table
            :items="folder.posts"
            :fields="table.fields"
            hover
            striped
            sticky-header
            sort-icon-left
            :tbodyTrClass="rowStyle"
          >
            <template v-slot:cell(title)="data">
              <b-link
                :to="'/'+$route.params.username+'/posts/'+folder.title+'/'+data.item.title"
              >{{ data.item.title }}</b-link>
            </template>
            <template v-slot:cell(format)="data">{{ data.item.format=='md'?'Markdown':'Latex' }}</template>
            <template v-slot:cell(createTime)="data">{{ data.item.createTime | peekDate }}</template>
            <template v-slot:cell(published)="data">{{ data.item.published ? 'Yes' : 'No' }}</template>
            <template v-slot:cell(actions)="data">
              <b-dropdown
                split
                :text="data.item.published ? 'Withdraw' : 'Publish'"
                class="mb-1 ml-3"
                variant="primary"
                v-if="editable"
                size="sm"
                @click="publishPost(folder.title, data.item.title,data.item.published)"
              >
                <b-dropdown-item
                  variant="secondary"
                  @click="showRenameForm(data.item.title,folder.title)"
                >Rename</b-dropdown-item>
                <b-dropdown-item
                  variant="danger"
                  @click="deletePostOrFolder(folder.title, data.item.title)"
                >Delete</b-dropdown-item>
              </b-dropdown>
            </template>
          </b-table>
        </b-collapse>
      </div>
    </div>
    <h2 v-else>No folders here.</h2>
    <!-- rename form -->
    <ModalInput
      ref="renameForm"
      title="Please enter the new name"
      :ok="rename"
      v-model="renameForm.newName"
      placeholder="New name"
    ></ModalInput>
  </div>
</template>

<script>
import netapi from "../mixin/netapi";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
import ModalInput from "../utils/ModalInput";

export default {
  name: "Posts",
  mixins: [timeFilter, strCheck, netapi, arrayCheck],
  components: { ModalInput },
  data() {
    return {
      
      table: {
        fields: [
          { key: "title", sortable: true },
          { key: "createTime", label: "Created At", sortable: true },
          { key: "format", sortable: true },
          { key: "published", sortable: true },
          { key: "stars", sortable: true },
          { key: "comments", sortable: true },
          "actions"
        ]
      },
      folders: [],
      renameForm: {
        newName: "",
        oldName: "",
        folderTitle: ""
      }
    };
  },
  methods: {
    rowStyle(item) {
      if (item.published) {
        return "table-success";
      }
    },
    enter() {
      this.apiPost(
        { route: "/get/post/foldersDetail" },
        data => {
          this.folders = [];
          for (let i = 0; i < data.folders.length; ++i) {
            data.folders[i].show = true;
            this.folders.push(data.folders[i]);
          }
        },
        "Get posts error"
      );
    },
    showRenameForm(oldName, folderTitle) {
      this.renameForm.oldName = this.renameForm.newName = oldName;
      this.renameForm.folderTitle = folderTitle;
      this.$refs.renameForm.show();
    },
    rename() {
      this.$refs.renameForm.hide();
      if (this.renameForm.oldName == this.renameForm.newName) return;
      // check file name validity
      if (!this.checkFileName(this.renameForm.newName)) {
        this.showRenameErr(this.invalidFileNameHint);
        return;
      }
      var renameFolder = !this.renameForm.folderTitle;
      // check title length
      if (renameFolder) {
        if (this.renameForm.newName.length > 50) {
          this.showRenameErr(
            "Folder title should be shorter than 50 characters."
          );
          return;
        }
      } else {
        if (this.renameForm.newName.length > 50) {
          this.showRenameErr("Post title should be shorter than 50.");
          return;
        }
      }
      // construct req params
      var route = renameFolder ? "/edit/folder/rename" : "/edit/post/rename";
      var data = renameFolder
        ? {
            old: this.renameForm.oldName,
            new: this.renameForm.newName
          }
        : {
            folder: this.renameForm.folderTitle,
            title: this.renameForm.oldName,
            newTitle: this.renameForm.newName
          };
      // send req
      this.apiPost(
        { route, data },
        () => {
          if (renameFolder) {
            for (let i = 0; i < this.folders.length; ++i) {
              if (this.folders[i].title == this.renameForm.oldName) {
                this.folders[i].title = this.renameForm.newName;
                return;
              }
            }
          } else {
            // rename post
            for (let i = 0; i < this.folders.length; ++i) {
              if (this.folders[i].title == this.renameForm.folderTitle) {
                for (let j = 0; j < this.folders[i].posts.length; ++j) {
                  if (
                    this.folders[i].posts[j].title == this.renameForm.oldName
                  ) {
                    this.folders[i].posts[j].title = this.renameForm.newName;
                    return;
                  }
                }
              }
            }
          }
        },
        "Rename failed"
      );
    },
    deletePostOrFolder(folderTitle, postTitle) {
      var route;
      var data;
      if (postTitle) {
        route = "/edit/post/delete";
        data = {
          folder: folderTitle,
          title: postTitle
        };
      } else {
        route = "/edit/folder/delete";
        data = {
          title: folderTitle
        };
      }
      this.apiPost(
        { route, data },
        () => {
          if (postTitle) {
            // delete post
            for (let i = 0; i < this.folders.length; ++i) {
              if (this.folders[i].title == folderTitle) {
                this.folders[i].posts = this.folders[i].posts.filter(s => {
                  return s.title != postTitle;
                });
                return;
              }
            }
          } else {
            // delete folder
            this.folders = this.folders.filter(s => {
              return s.title != folderTitle;
            });
            // if (!this.folders.length) this.updatePage();
          }
        },
        "Delete failed"
      );
    },
    publishPost(folderTitle, postTitle, isPublished) {
      var route = "/edit/post/publish";
      var data = {
        folder: folderTitle,
        title: postTitle,
        publish: !isPublished
      };
      this.apiPost(
        { route, data },
        () => {
          for (let i = 0; i < this.folders.length; ++i) {
            if (this.folders[i].title == folderTitle) {
              for (let j = 0; j < this.folders[i].posts.length; ++j) {
                if (this.folders[i].posts[j].title == postTitle) {
                  this.folders[i].posts[j].published = !isPublished;
                  return;
                }
              }
            }
          }
        },
        "Publish failed"
      );
    }
  },
  computed: {
    editable() {
      return (
        this.$root.$data.user.loggedIn &&
        this.$root.$data.user.username == this.$route.params.username
      );
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