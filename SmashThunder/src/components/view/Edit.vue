<template>
  <div>
    <b-form @submit="submit" style="height:500px">
      <b-form-row>
        <b-form-group label="Post title" label-for="postTitle">
          <b-form-input
            id="postTitle"
            v-model="form.title"
            placeholder="Please input the post title"
          ></b-form-input>
        </b-form-group>
      </b-form-row>
      <!-- <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
        <b-form-input id="input-2" v-model="form.name" required placeholder="Enter name"></b-form-input>
      </b-form-group>-->
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
  </div>
</template>

<script>
import showdown from "showdown";

var converter = new showdown.Converter();

export default {
  name: "Edit",
  data() {
    return {
      form: {
        text: "# Markdown Here",
        title: ""
      }
    };
  },
  methods: {
    submit() {}
  },
  computed: {
    resultHTML() {
      return converter.makeHtml(this.form.text);
    }
  }
};
</script>