<template>
  <div class="fixed-top">
    <b-collapse id="signInForm" v-if="!$root.$data.user.loggedIn">
      <div class="border-bottom" style="background-color:#fff">
        <b-container style="padding-top:80px;">
          <!-- Sign in form -->
          <b-jumbotron
            header="Welcome!"
            lead="SmashThunder is a very awsome blog management system."
          >
            <b-form @submit.prevent="submitClicked">
              <!-- Form mode -->
              <b-form-radio-group
                buttons
                size="sm"
                button-variant="outline-primary"
                :options="signInFormOptions"
                v-model="formMode"
                v-on:change="()=>{this.$root.$emit('bv::toggle::collapse', 'password2')}"
              ></b-form-radio-group>
              <hr />
              <!-- Inputs -->
              <b-form-group label="Username" label-for="signInUsername">
                <b-form-input
                  id="signInUsername"
                  v-model="$root.$data.user.username"
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
                  v-model="password"
                  required
                />
              </b-form-group>
              <!-- Collapsable password2 -->
              <b-collapse id="password2">
                <b-form-group label="Repeat Password" label-for="signInPassword2">
                  <b-form-input
                    type="password"
                    id="signInPassword2"
                    placeholder="Repeat password"
                    v-model="password2"
                  />
                </b-form-group>
              </b-collapse>
              <!-- Submit btn -->
              <b-button type="submit" variant="primary">
                <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
                <span class="sr-only">Loading...</span> Submit
              </b-button>
            </b-form>
          </b-jumbotron>
        </b-container>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import axios from "axios";
import sha256 from "js-sha256";
import netapi from "../mixin/netapi";

export default {
  name: "SignForm",
  mixins: [netapi],
  data() {
    return {
      password: "",
      password2: "",
      submitting: false,
      formMode: "Sign In", // can be 'Sign In' and 'Sign Up'
      signInFormOptions: ["Sign In", "Sign Up"]
    };
  },
  methods: {
    resetForm: function() {
      this.password = this.password2 = "";
      this.submitting = false;
      this.formMode = "Sign In";
    },
    checkUsername: function() {
      var t = this.$root.$data.user.username.match(/[A-Za-z0-9_]{7,50}/);
      if (t == null || t[0] != this.$root.$data.user.username) {
        this.showFormErr(
          "Username must consists of `A-Z`, `a-z`, `0-9` and `_`, and must be longer than 6 and shorter than 50!"
        );
        return false;
      }
      return true;
    },
    logout: function() {
      axios
        .post("/auth/logout")
        .then(() => {
          this.$root.$data.user.loggedIn = false;
        })
        .catch(() => {
          this.showFormErr();
        });
    },
    submitClicked: function() {
      this.submitting = true;
      if (!this.checkUsername()) return;
      var route = this.formMode == "Sign In" ? "/auth/login" : "/auth/register";
      this.apiPost(
        {
          route,
          data: {
            username: this.$root.$data.user.username,
            password: sha256(this.password)
          }
        },
        () => {
          this.$root.$data.user.loggedIn = true;
          this.resetForm();
        },
        this.formMode + " failed",
        () => {
          this.submitting = false;
        }
      );
    }
  },
  mounted: function() {
    axios
      .post("/auth/autoLogin")
      .then(res => {
        if (res.data.status == "ok") {
          this.$root.$data.user.username = res.data.username;
          this.$root.$data.user.loggedIn = true;
        }
      })
      .catch(() => {});
  }
};
</script>