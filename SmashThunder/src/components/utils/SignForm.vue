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
              <!-- Form err msg -->
              <b-alert variant="danger" show v-if="formErr">{{ formErr }}</b-alert>
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

export default {
  name: "SignForm",
  data() {
    return {
      formErr: "",
      password: "",
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
    /**
     * `msg` default to 'Internal Error in Server!'
     */
    showFormErr: function(msg) {
      this.formErr = msg || "Internal Error in Server!";
      this.submitting = false;
    },
    resetForm: function() {
      this.password = this.password2 = "";
      this.formErr = "";
      this.submitting = false;
      this.formMode = "sign-in";
    },
    checkUsername: function() {
      var t = this.$root.$data.user.username.match(/[A-Za-z0-9_]{7,}/);
      if (t == null || t[0] != this.$root.$data.user.username) {
        this.showFormErr(
          "Username must consists of `A-Z`, `a-z`, `0-9` and `_`, and must be longer than 6!"
        );
        return false;
      }
      return true;
    },
    logout: function() {
      axios.post("/auth/logout").then(
        () => {
          this.$root.$data.user.loggedIn = false;
        },
        () => {
          this.showFormErr();
        }
      );
    },
    submitClicked: function() {
      this.submitting = true;
      this.formErr = "";
      if (!this.checkUsername()) return;
      if (this.formMode == "sign-in") {
        // sign in
        axios
          .post("/auth/login", {
            username: this.$root.$data.user.username,
            password: sha256(this.password)
          })
          .then(res => {
            if (res.data.status == "ok") {
              this.$root.$data.user.loggedIn = true;
              this.resetForm();
            } else {
              this.showFormErr(res.data.status);
            }
          })
          .catch(() => {
            this.showFormErr();
          });
      } else if (this.formMode == "sign-up") {
        // sign up
        if (this.password != this.password2) {
          this.showFormErr("Different password!");
          return;
        }
        axios
          .post("/auth/register", {
            username: this.$root.$data.user.username,
            password: sha256(this.password)
          })
          .then(res => {
            if (res.data.status == "ok") {
              this.$root.$data.user.loggedIn = true;
              this.resetForm();
            } else {
              this.showFormErr(res.data.status);
            }
          })
          .catch(() => {
            this.showFormErr();
          });
      }
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