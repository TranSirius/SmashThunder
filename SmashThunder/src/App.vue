<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
      <!-- Brand -->
      <a class="navbar-brand" href="/">SmashThunder</a>
      <!-- Collapse btn -->
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbar">
        <!-- Search bar -->
        <form class="form-inline ml-auto mr-2">
          <div class="input-group">
            <input
              type="text"
              class="form-control form-control-sm"
              placeholder="User or post"
              aria-label="Recipient's username"
              aria-describedby="basic-addon2"
            />
            <div class="input-group-append">
              <button class="btn btn-outline-light btn-sm" type="button">Search</button>
            </div>
          </div>
        </form>
        <!-- if logged in -->
        <div v-if="loggedIn">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#">{{ username }}</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">New</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Sign out</a>
            </li>
          </ul>
        </div>
        <!-- not logged in -->
        <div v-else>
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#" @click="toggleForm('sign-in')">Sign in</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="toggleForm('sign-up')">Sign up</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
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
import JQuery from 'jquery'
var $ = JQuery

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
      if (this.formMode == targetForm) {
        $("#signInForm").collapse("hide");
        this.formMode = "";
      } else {
        if (targetForm == "sign-in") {
          $("#password2").collapse("hide");
          $("#signInForm").collapse("show");
        } else {
          // targetForm == 'sign-up'
          if (this.formMode == "") {
            $("#password2").addClass("show");
            $("#signInForm").collapse("show");
          } else {
            $("#password2").collapse("show");
          }
        }
        this.formMode = targetForm;
      }
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