<template>
  <div>
    <b-modal ref="modalForm" title="Upload new image" hide-footer>
      <b-alert variant="danger" show v-if="modalForm.err">{{ modalForm.err }}</b-alert>
      <b-form>
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
        <b-form-group label="Files" label-for="files">
          <b-form-file
            id="files"
            v-model="modalForm.files"
            multiple
            placeholder="Choose files or drop them here..."
            drop-placeholder="Drop files here..."
          ></b-form-file>
        </b-form-group>
        <b-button variant="primary" block @click="submit">
          <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
          <span class="sr-only">Loading...</span> Upload
        </b-button>
      </b-form>
    </b-modal>
    <div v-for="album in albums" :key="album.title">
      <h2>
        {{ album.title }}
        <b-dropdown
          split
          text="Upload"
          class="mb-1 ml-3"
          variant="primary"
          @click="showModal(album.title)"
        >
          <b-dropdown-item href="#">Rename</b-dropdown-item>
          <b-dropdown-item href="#" variant="danger">Delete</b-dropdown-item>
        </b-dropdown>
      </h2>
      <h6>Created at {{ album.createTime | peekDate }}.</h6>
      <hr />
      <b-card-group columns>
        <b-card v-for="img in album.imgs" :key="img.time" :img-src="img.url" :img-alt="img.title">
          <b-card-title>{{ img.title }}</b-card-title>
          <b-card-sub-title class="mb-2">Uploaded {{ img.time | timeOffset }} ago.</b-card-sub-title>
          <b-dropdown split text="Download">
            <b-dropdown-item>Rename</b-dropdown-item>
            <b-dropdown-item variant="danger">Delete</b-dropdown-item>
          </b-dropdown>
        </b-card>
      </b-card-group>
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
      newAlbumHint: "-- create a new album --"
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
                  this.albums[i] = res.data.albums[0].imgs;
                  return;
                }
              }
              // albumTitle not found, this is a new album
              this.albums = [res.data.albums[0]] + this.albums;
            }
          },
          () => {}
        );
    },
    submit() {
      this.modalForm.err = "";
      this.submitting = true;
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
            this.$refs.modalForm.hide();
            this.refresh(
              this.modalForm.newAlbumTitle || this.modalForm.albumTitle
            );
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
            if (res.data.status == "ok") v.albums = res.data.albums;
          },
          () => {}
        );
    });
  }
};
</script>