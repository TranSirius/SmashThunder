<template>
  <!-- Sign in form -->
  <b-collapse id="signInForm" v-if="!user.loggedIn">
    <b-jumbotron header="Welcome!" lead="SmashThunder is a very awsome blog management system.">
      <b-form>
        <b-form-radio-group
          buttons
          size="sm"
          button-variant="outline-primary"
          :options="signInFormOptions"
          v-model="formMode"
          v-on:change="()=>{this.$root.$emit('bv::toggle::collapse', 'password2')}"
        ></b-form-radio-group>
        <hr />
        <b-alert variant="danger" ref="formAlert">{{ formErr }}</b-alert>
        <b-form-group label="Username" label-for="signInUsername">
          <b-form-input
            id="signInUsername"
            v-model="user.username"
            placeholder="Enter username"
            type="text"
            required
          />
        </b-form-group>
        <b-form-group label="Password" label-for="signInPassword">
          <b-form-input
            type="password"
            id="signInPassword"
            placeholder="Password"
            v-model="user.password"
            required
          />
        </b-form-group>
        <b-collapse id="password2">
          <b-form-group label="Repeat Password" label-for="signInPassword2">
            <b-form-input
              type="password"
              id="signInPassword2"
              placeholder="Repeat password"
              v-model="password2"
              required
            />
          </b-form-group>
        </b-collapse>
        <b-button variant="primary" @click="submitClicked">
          <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
          <span class="sr-only">Loading...</span> Submit
        </b-button>
      </b-form>
    </b-jumbotron>
  </b-collapse>
</template>

<script>
import axios from "axios";
import sha256 from "js-sha256";

export default {
  name: "SignForm",
  props: {
    user: Object
  },
  data() {
    return {
      formErr: "",
      password2: "",
      submitting: false,
      formMode: "sign-in", // can be 'sign-in' and 'sign-up'
      signInFormOptions: [
        { text: "Sign In", value: "sign-in" },
        { text: "Sign Up", value: "sign-up" }
      ]
    };
  },
  methods: {
    showFormErr: function(msg) {
      this.formErr = msg;
      this.$refs.formAlert.localShow = true;
      this.submitting = false;
    },
    resetForm: function() {
      this.user.password = this.password2 = "";
      this.formErr = "";
      this.submitting = false;
      this.formMode = "sign-in";
    },
    checkUsername: function() {
      if (!this.user.username.match("[A-Za-z0-9_]{7,}")) {
        this.showFormErr(
          "Username must consists of `A-Z`, `a-z`, `0-9` and `_`, and must be longer than 6!"
        );
        return false;
      }
      return true;
    },
    logout: function() {
      axios.post("/auth/logout");
      this.user.loggedIn = false;
    },
    submitClicked: function() {
      this.submitting = true;
      this.$refs.formAlert.localShow = false;
      if (this.formMode == "sign-in") {
        // sign in
        if (!this.checkUsername()) return;
        axios
          .post("/auth/login", {
            username: this.user.username,
            password: sha256(this.user.password)
          })
          .then(res => {
            if (res.data.status == "ok") {
              this.user.loggedIn = true;
              this.resetForm();
            } else {
              this.showFormErr(res.data.status);
            }
          })
          .catch(() => {
            this.showFormErr("Internal Error in Server!");
          });
      } else if (this.formMode == "sign-up") {
        // sign up
        if (!this.checkUsername()) {
          return;
        }
        if (this.user.password != this.password2) {
          this.showFormErr("Different password!");
          return;
        }
        axios
          .post("/auth/register", {
            username: this.user.username,
            password: sha256(this.user.password)
          })
          .then(res => {
            if (res.data.status == "ok") {
              this.user.loggedIn = true;
              this.resetForm();
            } else {
              this.showFormErr(res.data.status);
            }
          })
          .catch(() => {
            this.showFormErr("Internal Error in Server!");
          });
      }
    }
  }
};
</script>