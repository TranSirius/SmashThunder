<template>
  <div>
    <b-navbar toggleable="lg" fixed="top" type="dark" variant="dark">
      <!-- Brand -->
      <b-navbar-brand to="/">SmashThunder</b-navbar-brand>
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
        <b-navbar-nav v-if="user.loggedIn">
          <!-- if logged in -->
          <!-- <b-nav-item :to="user.username">{{ user.username }}</b-nav-item> -->
          <b-nav-item-dropdown :text="user.username" right>
            <b-dropdown-item :to="user.username">Home</b-dropdown-item>
            <b-dropdown-item :to="user.username + '/album'">Album</b-dropdown-item>
            <b-dropdown-item :to="user.username + '/posts'">Posts</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item to="#">New</b-nav-item>
          <b-nav-item to="#" @click="()=>{this.$refs.form.logout()}">Sign out</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-else>
          <!-- not logged in -->
          <b-nav-item v-b-toggle.signInForm>Sign In/Up</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div style="margin-top:80px"></div>
    <b-container>
      <SignForm :user="user" ref="form"></SignForm>
    </b-container>
  </div>
</template>

<script>
import SignForm from "./SignForm.vue";

export default {
  name: "Navbar",
  components: {
    SignForm
  },
  props: {
    user: Object
  }
};
</script>