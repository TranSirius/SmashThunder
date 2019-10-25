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
        <b-form-group label="Files" label-for="files">
          <b-form-file
            id="files"
            v-model="modalForm.files"
            multiple
            placeholder="Choose files or drop them here..."
            drop-placeholder="Drop files here..."
            style="overflow:hidden"
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
          <b-dropdown-item href="#">Rename</b-dropdown-item>
          <b-dropdown-item href="#" variant="danger">Delete</b-dropdown-item>
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
              <b-dropdown-item>Rename</b-dropdown-item>
              <b-dropdown-item variant="danger">Delete</b-dropdown-item>
            </b-dropdown>
            <b-button v-else @click="downloadImg(img.url, img.title)">Download</b-button>
          </b-card>
        </b-card-group>
        <h4 v-else>No image in this album.</h4>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Album",
  data() {
    return {
      albums: [],
      modalForm: {
        albumTitle: "",
        files: [],
        options: [],
        newAlbumTitle: "",
        err: ""
      },
      submitting: false,
      newAlbumHint: "-- create a new album --",
      imgFilter: ""
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
    }
  },
  beforeRouteEnter: (from, to, next) => {
    next(v => {
      axios
        .post("/get/album", {
          username: v.$route.params.username
        })
        .then(
          res => {
            if (res.data.status == "ok") {
              for (let i = 0; i < res.data.albums.length; ++i) {
                res.data.albums[i].show = true;
                v.albums.push(res.data.albums[i]);
              }
            }
          },
          () => {}
        );
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