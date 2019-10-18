<template>
  <div id="app">
    <!-- Navbar -->
    <b-navbar class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
      <!-- Brand -->
      <b-navbar-brand href="/">SmashThunder</b-navbar-brand>
      <!-- Collapse btn -->
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse is-nav id="nav-collapse">
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <!-- Search bar -->
          <b-nav-form class="form-inline ml-auto mr-2">
            <b-input-group>
              <b-form-input size="sm" placeholder="User or post" />
              <b-input-group-append>
                <b-button variant="outline-light" size="sm">Search</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-nav-form>
        </b-navbar-nav>
        <b-navbar-nav v-if="loggedIn">
          <!-- if logged in -->
          <b-nav-item href="#">{{ username }}</b-nav-item>
          <b-nav-item href="#">New</b-nav-item>
          <b-nav-item href="#">Sign out</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-else>
          <!-- not logged in -->
          <b-nav-item href="#" @click="toggleForm('sign-in')">Sign in</b-nav-item>
          <b-nav-item href="#" @click="toggleForm('sign-up')">Sign up</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <!-- Main content -->
    <div class="container" style="margin-top:80px">
      <!-- Sign in form -->
      <div class="collapse" id="signInForm">
        <div class="card mb-3">
          <div class="card-body">
            <form>
              <div v-if="formErr">
                <div class="alert alert-danger" role="alert">{{ formErr }}</div>
              </div>
              <div class="form-group">
                <label for="signInUsername">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="signInUsername"
                  placeholder="Enter username"
                  v-model="username"
                />
              </div>
              <div class="form-group">
                <label for="signInPassword">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="signInPassword"
                  placeholder="Password"
                  v-model="password"
                />
              </div>
              <div class="collapse" id="password2">
                <div class="form-group">
                  <label for="signInPassword2">Repeat Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="signInPassword2"
                    placeholder="Repeat password"
                    v-model="password2"
                  />
                </div>
              </div>
              <button type="button" class="btn btn-primary" @click="submitClicked">
                <span
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                  v-if="submitting"
                ></span>
                <span class="sr-only">Loading...</span>Submit
              </button>
            </form>
          </div>
        </div>
      </div>
      <Content></Content>
    </div>
  </div>
</template>

<script>
import Content from "./components/Content.vue";

export default {
  name: "app",
  components: {
    Content
  },
  data() {
    return {
      loggedIn: false,
      formMode: "", // '' means no form, 'sign-in' means show sign in form, 'sign up' means show sign up form
      formErr: "",
      username: "",
      password: "",
      password2: "",
      submitting: false
    };
  },
  methods: {
    toggleForm: function(targetForm) {
      this.formMode = targetForm;
      // if (this.formMode == targetForm) {
      //   $("#signInForm").collapse("hide");
      //   this.formMode = "";
      // } else {
      //   if (targetForm == "sign-in") {
      //     $("#password2").collapse("hide");
      //     $("#signInForm").collapse("show");
      //   } else {
      //     // targetForm == 'sign-up'
      //     if (this.formMode == "") {
      //       $("#password2").addClass("show");
      //       $("#signInForm").collapse("show");
      //     } else {
      //       $("#password2").collapse("show");
      //     }
      //   }
      //   this.formMode = targetForm;
      // }
    },
    submitClicked: function() {
      this.submitting = true;
      if (this.formMode == "sign-in") {
        // sign in
      } else if (this.formMode == "sign-up") {
        // sign up
        if (this.password != this.password2) {
          this.formErr = "different password!";
          this.submitting = false;
        }
      }
    }
  }
};
</script>