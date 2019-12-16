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
import sha256 from "js-sha256";
import netapi from "../mixin/netapi";
import errHandler from "../mixin/errHandler";

export default {
  name: "SignForm",
  mixins: [netapi, errHandler],
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
    showFormErr: function(msg) {
      this.toastErr(this.formMode + " failed", msg);
      this.submitting = false;
    },
    resetForm: function() {
      this.password = this.password2 = "";
      this.submitting = false;
      this.formMode = "Sign In";
    },
    checkUsername: function() {
      if (
        this.$root.$data.user.username.length < 7 ||
        this.$root.$data.user.username.length > 50
      ) {
        this.showFormErr("Username must be between 7 and 50 characters");
        return false;
      }
      if (!this.urlSafe(this.$root.$data.user.username)) {
        this.showFormErr(
          "Username cannot contain " + this.urlInvalidCharacters.join(",")
        );
        return false;
      }
      return true;
    },
    logout: function() {
      this.apiPost(
        { route: "/auth/logout" },
        () => {
          this.$root.$data.user.loggedIn = false;
        },
        "Logout failed.",
        () => {
          this.submitting = false;
        }
      );
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
    this.apiPost(
      { route: "/auth/autoLogin" },
      data => {
        this.$root.$data.user.username = data.username;
        this.$root.$data.user.loggedIn = true;
      },
      "" // empty err title, no toast will be shown
    );
  }
};
</script>