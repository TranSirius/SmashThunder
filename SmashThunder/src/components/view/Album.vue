<template>
  <div>
    <!-- modalForm -->
    <b-modal ref="modalForm" title="Upload new image" hide-footer>
      <!-- Form err msg -->
      <b-form @submit.prevent="submit">
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
        <b-form-group label="Files" label-for="files">
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
        <b-button variant="primary" block type="submit">
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
            <b-dropdown split text="Download" v-if="editable" @click="download(img.url, img.title)">
              <b-dropdown-item @click="showRenameForm(img.title, album.title)">Rename</b-dropdown-item>
              <b-dropdown-item @click="del(album.title, img.title)" variant="danger">Delete</b-dropdown-item>
            </b-dropdown>
            <b-button v-else @click="download(img.url, img.title)">Download</b-button>
          </b-card>
        </b-card-group>
        <h4 v-else>No image in this album.</h4>
      </b-collapse>
    </div>
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
import timeFilter from "../mixin/timeFilter";
import strCheck from "../mixin/strCheck";
import arrayCheck from "../mixin/arrayCheck";
import ModalInput from "../utils/ModalInput";
import netapi from "../mixin/netapi";
import downloadUtils from "../mixin/downloadUtils";

export default {
  name: "Album",
  mixins: [timeFilter, strCheck, netapi, arrayCheck, downloadUtils],
  components: { ModalInput },
  data() {
    return {
      /**
       * "albums": [{
       * "title": "str",
       * "show": "bool",
       * "createTime": "Unix Time Stamp(int)",
       * "imgs": [{
       *  "url": "str",
       *  "title": "str",
       *     "time": "Unix Time Stamp(int)"
       *   }]
       * }]
       */
      albums: [],
      modalForm: {
        albumTitle: "",
        files: [],
        options: [],
        newAlbumTitle: ""
      },
      submitting: false,
      newAlbumHint: "-- create a new album --",
      invalidFileNameHint:
        "Album/Image title can not contain !*'();:@&=+$,/?#[]",
      duplicatedImgHint:
        "Duplicate image title in same album. Old image will be replaced.",
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
     * `s` can be undefined.
     */
    showSubmitErr(s) {
      this.submitting = false;
      this.toastErr("Submit failed", s);
    },
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
      this.apiPost(
        {
          route: "/get/album",
          data: {
            username: this.$route.params.username,
            target: albumTitle
          }
        },
        data => {
          for (let i = 0; i < this.albums.length; ++i) {
            if (this.albums[i].title == albumTitle) {
              this.albums[i].imgs = data.albums[0].imgs;
              return;
            }
          }
          // albumTitle not found, this is a new album
          data.albums[0].show = true;
          this.albums.push(data.albums[0]);
        },
        "Refresh album failed"
      );
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
      this.submitting = true;
      // check album title validity
      var title = this.modalForm.newAlbumTitle || this.modalForm.albumTitle;
      if (!this.checkFileName(title)) {
        this.showSubmitErr(this.invalidFileNameHint);
        return;
      }
      if (title.length > 50) {
        this.showSubmitErr("Album title should be less than 50 characters");
        return;
      }
      // test if new album title is duplicated
      if (this.modalForm.albumTitle == this.newAlbumHint) {
        if (this.modalForm.newAlbumTitle == this.newAlbumHint) {
          this.showSubmitErr(this.invalidFileNameHint);
          return;
        }
        if (
          this.albums.filter(s => {
            return s.title == title;
          }).length
        ) {
          this.showSubmitErr("Duplicated album title!");
          return;
        }
      }
      // check img name validity
      for (let i = 0; i < this.modalForm.files.length; ++i) {
        if (!this.checkFileName(this.modalForm.files[i].name)) {
          this.showSubmitErr(this.invalidFileNameHint);
          return;
        }
        if (this.modalForm.files[i].name.length > 200) {
          this.showSubmitErr("Photo title should be less than 200 characters.");
          return;
        }
      }
      // construct data
      var data = new FormData();
      data.append("albumTitle", title);
      // TODO: remove `time` in data
      data.append("time", Date.now());
      for (var i = 0; i < this.modalForm.files.length; i++) {
        let file = this.modalForm.files[i];
        data.append("files", file);
      }
      this.apiPost(
        {
          route: "/submit/img",
          data,
          config: { headers: { "Content-Type": "multipart/form-data" } }
        },
        () => {
          this.refresh(title);
          this.$refs.modalForm.hide();
          this.submitting = false;
        },
        "Submit failed",
        () => (this.submitting = false)
      );
    },
    /**
     * This function is used by route guards. Reload this whole page, refresh all albums.
     */
    enter() {
      this.apiPost(
        {
          route: "/get/album",
          data: { username: this.$route.params.username }
        },
        data => {
          this.albums = [];
          for (let i = 0; i < data.albums.length; ++i) {
            data.albums[i].show = true;
            this.albums.push(data.albums[i]);
          }
        },
        "",
        () => this.to404()
      );
    },
    showDupImgErr() {
      this.toastErr("Warning", this.duplicatedImgHint, "warning");
    },
    /**
     * This funcion will be called when user has selected images to be uploaded.
     */
    checkDuplicateImg() {
      var toBeUploaded = []; // files name
      this.modalForm.files.map(file => toBeUploaded.push(file.name));
      // find the album
      for (let i = 0; i < this.albums.length; ++i) {
        if (this.albums[i].title == this.modalForm.albumTitle) {
          // get all img title
          var exist = []; // file names
          this.albums[i].imgs.map(img => exist.push(img.title));
          // duplicate with old imgs
          if (exist.filter(s => toBeUploaded.includes(s)).length > 0) {
            this.showDupImgErr();
            return;
          }
          // new imgs duplicate
          if (!this.checkUniqueness(toBeUploaded)) this.showDupImgErr();
          return;
        }
      }
      // new album, just check new imgs duplicate
      if (!this.checkUniqueness(toBeUploaded)) this.showDupImgErr();
    },
    showRenameForm(oldName, albumTitle) {
      this.renameForm.oldName = this.renameForm.newName = oldName;
      this.renameForm.albumTitle = albumTitle;
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
      var renameAlbum = !this.renameForm.albumTitle;
      // check title length
      if (renameAlbum) {
        if (this.renameForm.newName.length > 50) {
          this.showRenameErr(
            "Album title should be shorter than 50 characters."
          );
          return;
        }
      } else {
        if (this.renameForm.newName.length > 200) {
          this.showRenameErr("Image title should be shorter than 200.");
          return;
        }
      }
      // construct req params
      var route = renameAlbum ? "/edit/album/rename" : "/edit/img/rename";
      var data = renameAlbum
        ? {
            albumTitle: this.renameForm.oldName,
            newTitle: this.renameForm.newName
          }
        : {
            albumTitle: this.renameForm.albumTitle,
            imgTitle: this.renameForm.oldName,
            newTitle: this.renameForm.newName
          };
      // send req
      this.apiPost(
        { route, data },
        () => {
          if (renameAlbum) {
            for (let i = 0; i < this.albums.length; ++i) {
              if (this.albums[i].title == this.renameForm.oldName) {
                this.albums[i].title = this.renameForm.newName;
                return;
              }
            }
          } else {
            // rename img
            for (let i = 0; i < this.albums.length; ++i) {
              if (this.albums[i].title == this.renameForm.albumTitle) {
                for (let j = 0; j < this.albums[i].imgs.length; ++j) {
                  if (this.albums[i].imgs[j].title == this.renameForm.oldName) {
                    this.albums[i].imgs[j].title = this.renameForm.newName;
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
      this.apiPost(
        { route, data },
        () => {
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
            if (!this.albums.length) this.enter();
          }
        },
        "Delete failed"
      );
    }
  },
  beforeRouteUpdate(to, from, next) {
    next();
    this.enter();
  },
  beforeRouteEnter(to, from, next) {
    next(v => {
      v.enter();
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