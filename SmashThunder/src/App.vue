<template>
  <div id="app">
    <!-- Navbar -->
    <b-navbar toggleable="lg" fixed type="dark" variant="dark">
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
      <b-collapse id="signInForm">
        <b-card>
          <b-card-body>
            <b-form>
              <b-alert variant="danger">{{ formErr }}</b-alert>
              <b-form-group label="Username" label-for="signInUsername">
                <b-form-input
                  id="signInUsername"
                  v-model="username"
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
                <b-spinner label="loading" v-if="submitting"></b-spinner>Submit
              </b-button>
            </b-form>
          </b-card-body>
        </b-card>
      </b-collapse>
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