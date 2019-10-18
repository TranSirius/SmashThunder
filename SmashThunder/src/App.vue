<template>
  <div id="app">
    <!-- Navbar -->
    <b-navbar toggleable="lg" fixed="top" type="dark" variant="dark">
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
          <b-nav-item href="#" v-b-toggle.signInForm>Sign In/Up</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <!-- Main content -->
    <b-container style="margin-top:80px">
      <!-- Sign in form -->
      <b-collapse id="signInForm">
        <b-card>
          <b-card-body>
            <b-form>
              <b-alert variant="danger">{{ formErr }}</b-alert>
              <b-form-radio-group
                buttons
                size="sm"
                button-variant="outline-primary"
                :options="signInFormOptions"
                v-model="formMode"
                v-on:change="()=>{this.$root.$emit('bv::toggle::collapse', 'password2')}"
              ></b-form-radio-group>
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
                <b-spinner label="loading" small v-if="submitting" type="grow"></b-spinner>
                <span class="sr-only">Loading...</span> Submit
              </b-button>
            </b-form>
          </b-card-body>
        </b-card>
      </b-collapse>
      <Content></Content>
    </b-container>
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
      formErr: "",
      username: "",
      password: "",
      password2: "",
      submitting: false,
      formMode: "sign-in", // '' means no form, 'sign-in' means show sign in form, 'sign up' means show sign up form
      signInFormOptions: [
        { text: "Sign In", value: "sign-in" },
        { text: "Sign Up", value: "sign-up" }
      ]
    };
  },
  methods: {
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