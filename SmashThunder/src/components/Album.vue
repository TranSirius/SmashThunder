<template>
  <div>
    <b-modal id="modalForm" title="Upload new image" hide-footer>
      <b-form @submit.prevent enctype="multipart/form-data" action="/submit/img" method="POST">
        <b-form-group label="Album" label-for="albumTitle">
          <b-form-select
            name="albumTitle"
            id="albumTitle"
            v-model="modalForm.albumTitle"
            :options="modalForm.options"
          ></b-form-select>
        </b-form-group>
        <b-form-group label="Files" label-for="files">
          <b-form-file
            id="files"
            name="files"
            v-model="modalForm.files"
            multiple
            placeholder="Choose files or drop them here..."
            drop-placeholder="Drop files here..."
          ></b-form-file>
        </b-form-group>
        <b-button type="submit" variant="primary">
          <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
          <span class="sr-only">Loading...</span> Upload
        </b-button>
      </b-form>
    </b-modal>
    <div v-for="album in albums" :key="album.title">
      <h2>{{ album.title }}</h2>
      <hr />
      <b-card-group columns>
        <b-card
          v-for="img in album.imgs"
          :key="img.time"
          overlay
          :img-src="img.url"
          :img-alt="img.title"
          text-variant="white"
          :title="img.title"
        ></b-card>
      </b-card-group>
      <b-button @click="showModal(album.title)">Upload</b-button>
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
        options: []
      },
      submitting: false
    };
  },
  methods: {
    showModal(current) {
      this.modalForm.albumTitle = current;
      this.modalForm.options = [];
      for (let i = 0; i < this.albums.length; ++i) {
        this.modalForm.options.push({ value: this.albums[i].title });
      }
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