<template>
  <div>
    <!-- SignForm must be ahead of Navbar! Otherwise the z-index will be wrong! -->
    <SignForm ref="form"></SignForm>
    <b-navbar toggleable="lg" fixed="top" type="dark" variant="dark">
      <!-- Brand -->
      <img src="/icon.png" height="40" />
      <b-navbar-brand to="/">SmashThunder</b-navbar-brand>
      <!-- Collapse btn -->
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse is-nav id="nav-collapse">
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto mt-1 mb-auto">
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
        <b-navbar-nav v-if="$root.$data.user.loggedIn">
          <!-- if logged in -->
          <!-- <b-nav-item :to="user.username">{{ user.username }}</b-nav-item> -->
          <b-nav-item-dropdown :text="$root.$data.user.username" right class="text-right">
            <b-dropdown-item :to="'/'+$root.$data.user.username">Home</b-dropdown-item>
            <b-dropdown-item :to="'/'+$root.$data.user.username + '/album'">Album</b-dropdown-item>
            <b-dropdown-item :to="'/'+$root.$data.user.username + '/posts'">Posts</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item class="text-right" to="#">New</b-nav-item>
          <b-nav-item class="text-right" to="#" @click="()=>{this.$refs.form.logout()}">Sign out</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-else>
          <!-- not logged in -->
          <b-nav-item class="text-right" v-b-toggle.signInForm>Sign In/Up</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import SignForm from "./utils/SignForm.vue";

export default {
  name: "Navbar",
  components: {
    SignForm
  }
};
</script>