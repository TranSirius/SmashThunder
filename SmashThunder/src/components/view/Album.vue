<template>
  <div>
    <!-- modalForm -->
    <b-modal ref="modalForm" title="Upload new image" hide-footer>
      <!-- Form err msg -->
      <b-alert variant="danger" show v-if="modalForm.err">{{ modalForm.err }}</b-alert>
      <b-form>
        <!-- Choose a album or create a new album-->
        <b-form-group label="Album" label-for="albumTitle">
          <b-form-select
            id="albumTitle"
            v-model="modalForm.albumTitle"
            :options="modalForm.options"
          ></b-form-select>
        </b-form-group>
        <b-form-group
          label="Name of the new album"
          label-for="newAlbumTitle"
          v-if="modalForm.albumTitle==newAlbumHint"
        >
          <b-form-input
            id="newAlbumTitle"
            v-model="modalForm.newAlbumTitle"
            type="text"
            placeholder="New album name"
          ></b-form-input>
        </b-form-group>
        <!-- Choose files -->
        <b-form-group
          label="Files"
          label-for="files"
          :description="modalForm.duplicatedImg?'Duplicate image detected!':''"
        >
          <b-form-file
            id="files"
            v-model="modalForm.files"
            multiple
            placeholder="Choose files or drop them here..."
            drop-placeholder="Drop files here..."
            style="overflow:hidden"
            @input="checkDuplicateImg"
          ></b-form-file>
        </b-form-group>
        <b-button variant="primary" block @click="submit">
          <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
          <span class="sr-only">Loading...</span> Upload
        </b-button>
      </b-form>
    </b-modal>
    <!-- Image Filter -->
    <b-form inline>
      <label label-for="img-filter" class="ml-auto mr-sm-2">Image Filter</label>
      <b-form-input id="img-filter" v-model="imgFilter" placeholder="Enter image filter..."></b-form-input>
    </b-form>
    <div v-for="album in sortedAlbums" :key="album.title" class="pb-5">
      <!-- Album title -->
      <h2>
        {{ album.title }}
        <b-dropdown
          split
          text="Upload"
          class="mb-1 ml-3"
          variant="primary"
          @click="showModal(album.title)"
          v-if="editable"
        >
          <b-dropdown-item @click="showRenameForm(album.title)">Rename</b-dropdown-item>
          <b-dropdown-item @click="del(album.title)" variant="danger">Delete</b-dropdown-item>
        </b-dropdown>
        <b-button
          class="mb-1 ml-3"
          variant="outline-info"
          :pressed.sync="album.show"
        >{{ album.show ? 'Hide' : 'Show' }}</b-button>
      </h2>
      <h6>Created at {{ album.createTime | peekDate }}.</h6>
      <hr />
      <!-- Imgs -->
      <b-collapse v-model="album.show">
        <b-card-group columns v-if="filtedImgs(album.imgs).length">
          <b-card
            v-for="img in sortedImgs(filtedImgs(album.imgs))"
            :key="img.title"
            :img-src="img.url"
            :img-alt="img.title"
          >
            <b-card-title>{{ img.title }}</b-card-title>
            <b-card-sub-title class="mb-2">Uploaded {{ img.time | timeOffset }} ago.</b-card-sub-title>
            <b-dropdown
              split
              text="Download"
              v-if="editable"
              @click="downloadImg(img.url, img.title)"
            >
              <b-dropdown-item @click="showRenameForm(img.title, album.title)">Rename</b-dropdown-item>
              <b-dropdown-item @click="del(album.title, img.title)" variant="danger">Delete</b-dropdown-item>
            </b-dropdown>
            <b-button v-else @click="downloadImg(img.url, img.title)">Download</b-button>
          </b-card>
        </b-card-group>
        <h4 v-else>No image in this album.</h4>
      </b-collapse>
    </div>
    <!-- rename form -->
    <b-modal ref="renameForm" title="Please enter the new name" centered @ok="rename">
      <b-form-input v-model="renameForm.newName" placeholder="New name"></b-form-input>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";

export default {
  name: "Album",
  mixins: [timeFilter, strCheck],
  data() {
    return {
      albums: [],
      modalForm: {
        albumTitle: "",
        files: [],
        options: [],
        newAlbumTitle: "",
        err: "",
        duplicatedImg: false
      },
      submitting: false,
      newAlbumHint: "-- create a new album --",
      imgFilter: "",
      renameForm: {
        newName: "",
        oldName: "",
        albumTitle: ""
      }
    };
  },
  methods: {
    /**
     * Reset form(set album title, get options, reset files, reset newAlbumTitle) then show form
     */
    showModal(current) {
      this.modalForm.albumTitle = current;
      this.modalForm.options = [this.newAlbumHint];
      for (let i = 0; i < this.albums.length; ++i) {
        this.modalForm.options.push(this.albums[i].title);
      }
      this.modalForm.files = [];
      this.modalForm.newAlbumTitle = "";
      this.$refs.modalForm.show();
    },
    /**
     * Reload the target album. If `albumTitle` not in `this.albums`, create it in `this.albums`
     */
    refresh(albumTitle) {
      axios
        .post("/get/album", {
          username: this.$route.params.username,
          target: albumTitle
        })
        .then(
          res => {
            if (res.data.status == "ok") {
              for (let i = 0; i < this.albums.length; ++i) {
                if (this.albums[i].title == albumTitle) {
                  this.albums[i].imgs = res.data.albums[0].imgs;
                  return;
                }
              }
              // albumTitle not found, this is a new album
              res.data.albums[0].show = true;
              this.albums.push(res.data.albums[0]);
            }
          },
          () => {}
        );
    },
    downloadImg(url, title) {
      var t = document.createElement("a");
      t.setAttribute("href", url);
      t.setAttribute("download", title);
      t.click();
    },
    filtedImgs(imgs) {
      return imgs.filter(i => {
        return i.title.includes(this.imgFilter);
      });
    },
    sortedImgs(imgs) {
      return imgs.sort((a, b) => {
        return b.time - a.time;
      });
    },
    submit() {
      this.modalForm.err = "";
      this.submitting = true;
      // test new album title validity
      if (
        !this.checkFileName(
          this.modalForm.newAlbumTitle || this.modalForm.albumTitle
        )
      ) {
        this.submitting = false;
        this.modalForm.err = "Invalid album title";
        return;
      }
      if (this.modalForm.albumTitle == this.newAlbumHint) {
        if (this.modalForm.newAlbumTitle == this.newAlbumHint) {
          this.modalForm.err = "Invalid album title!";
          this.submitting = false;
          return;
        }
        for (let i = 0; i < this.albums.length; ++i) {
          if (this.albums[i].title == this.modalForm.newAlbumTitle) {
            this.modalForm.err = "Duplicated album title!";
            this.submitting = false;
            return;
          }
        }
      }
      // check img name validity
      for (let i = 0; i < this.modalForm.files.length; ++i) {
        if (!this.checkFileName(this.modalForm.files[i].name)) {
          this.modalForm.err = "Invalid image title!";
          this.submitting = false;
          return;
        }
      }
      // construct data
      var data = new FormData();
      data.append(
        "albumTitle",
        this.modalForm.newAlbumTitle || this.modalForm.albumTitle
      );
      data.append("time", Date.now());
      for (var i = 0; i < this.modalForm.files.length; i++) {
        let file = this.modalForm.files[i];
        data.append("files", file);
      }
      axios({
        method: "post",
        url: "/submit/img",
        data: data,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      })
        .then(res => {
          if (res.data.status == "ok") {
            this.refresh(
              this.modalForm.newAlbumTitle || this.modalForm.albumTitle
            );
            this.$refs.modalForm.hide();
          } else {
            this.modalForm.err = res.data.status;
          }
          this.submitting = false;
        })
        .catch(() => {
          this.modalForm.err = "Internal Error in Server!";
          this.submitting = false;
        });
    },
    updatePage() {
      axios
        .post("/get/album", {
          username: this.$route.params.username
        })
        .then(
          res => {
            if (res.data.status == "ok") {
              this.albums = [];
              for (let i = 0; i < res.data.albums.length; ++i) {
                res.data.albums[i].show = true;
                this.albums.push(res.data.albums[i]);
              }
            }
          },
          () => {}
        );
    },
    checkDuplicateImg() {
      var toBeUploaded = [];
      for (let i = 0; i < this.modalForm.files.length; ++i) {
        toBeUploaded.push(this.modalForm.files[i].name);
      }
      // find the album
      for (let i = 0; i < this.albums.length; ++i) {
        if (this.albums[i].title == this.modalForm.albumTitle) {
          // get all img title
          var exist = [];
          for (let j = 0; j < this.albums[i].imgs.length; ++j) {
            exist.push(this.albums[i].imgs[j].title);
          }
          // duplicate with old imgs
          if (exist.filter(s => toBeUploaded.includes(s)).length > 0) {
            this.modalForm.duplicatedImg = true;
            return;
          }
          // new imgs duplicate
          if (
            toBeUploaded.slice().filter(s => toBeUploaded.includes(s)).length >
            0
          )
            this.modalForm.duplicatedImg = true;
          this.modalForm.duplicatedImg = false;
          return;
        }
      }
      // new album
      if (toBeUploaded.slice().filter(s => toBeUploaded.includes(s)).length > 0)
        this.duplicatedImg = true;
      this.duplicatedImg = false;
    },
    showRenameForm(oldName, albumTitle) {
      this.renameForm.oldName = this.renameForm.newName = oldName;
      this.renameForm.albumTitle = albumTitle;
      this.$refs.renameForm.show();
    },
    rename() {
      if (this.renameForm.oldName == this.renameForm.newName) return;
      // rename album
      if (!this.renameForm.albumTitle) {
        // check album name validity
        if (!this.checkFileName(this.renameForm.newName)) {
          this.$bvToast.toast("Invalid album title!", {
            title: "Rename failed",
            autoHideDelay: 5000
          });
          return;
        }
        axios
          .post("/edit/album/rename", {
            albumTitle: this.renameForm.oldName,
            newTitle: this.renameForm.newName
          })
          .then(
            res => {
              if (res.data.status != "ok") {
                this.$bvToast.toast(res.data.status, {
                  title: "Rename failed",
                  autoHideDelay: 5000
                });
              } else {
                for (let i = 0; i < this.albums.length; ++i) {
                  if (this.albums[i].title == this.renameForm.oldName) {
                    this.albums[i].title = this.renameForm.newName;
                    return;
                  }
                }
              }
            },
            () => {
              this.$bvToast.toast("Internal Error in Server!", {
                title: "Rename failed",
                autoHideDelay: 5000
              });
            }
          );
      } else {
        // rename img
        // check image title validity
        if (!this.checkFileName(this.renameForm.newName)) {
          this.$bvToast.toast("Invalid image title!", {
            title: "Rename failed",
            autoHideDelay: 5000
          });
          return;
        }
        axios
          .post("/edit/img/rename", {
            albumTitle: this.renameForm.albumTitle,
            imgTitle: this.renameForm.oldName,
            newTitle: this.renameForm.newName
          })
          .then(
            res => {
              if (res.data.status == "ok") {
                for (let i = 0; i < this.albums.length; ++i) {
                  if (this.albums[i].title == this.renameForm.albumTitle) {
                    for (let j = 0; j < this.albums[i].imgs.length; ++j) {
                      if (
                        this.albums[i].imgs[j].title == this.renameForm.oldName
                      ) {
                        this.albums[i].imgs[j].title = this.renameForm.newName;
                        return;
                      }
                    }
                  }
                }
              } else {
                this.$bvToast.toast(res.data.status, {
                  title: "Rename failed",
                  autoHideDelay: 5000
                });
              }
            },
            () => {
              this.$bvToast.toast("Internal Error in Server!", {
                title: "Rename failed",
                autoHideDelay: 5000
              });
            }
          );
      }
    },
    del(albumTitle, imgTitle) {
      var route;
      var data;
      if (imgTitle) {
        route = "/edit/img/delete";
        data = {
          albumTitle,
          imgTitle
        };
      } else {
        route = "/edit/album/delete";
        data = {
          albumTitle
        };
      }
      axios
        .post(route, data)
        .then(res => {
          if (res.data.status == "ok") {
            if (imgTitle) {
              // delete img
              for (let i = 0; i < this.albums.length; ++i) {
                if (this.albums[i].title == albumTitle) {
                  this.albums[i].imgs = this.albums[i].imgs.filter(s => {
                    return s.title != imgTitle;
                  });
                  return;
                }
              }
            } else {
              // delete album
              this.albums = this.albums.filter(s => {
                return s.title != albumTitle;
              });
              if (!this.albums.length) this.updatePage();
            }
          } else {
            this.$bvToast.toast(res.data.status, {
              title: "Delete failed",
              autoHideDelay: 5000
            });
          }
        })
        .catch(() => {
          this.$bvToast.toast("Internal Error in Server!", {
            title: "Delete failed",
            autoHideDelay: 5000
          });
        });
    }
  },
  beforeRouteUpdate(to, from, next) {
    next();
    this.updatePage();
  },
  beforeRouteEnter(to, from, next) {
    next(v => {
      v.updatePage();
    });
  },
  computed: {
    sortedAlbums() {
      return this.albums.slice().sort((a, b) => {
        return a.title.localeCompare(b.title);
      });
    },
    editable() {
      return (
        this.$root.$data.user.loggedIn &&
        this.$root.$data.user.username == this.$route.params.username
      );
    }
  }
};
</script>