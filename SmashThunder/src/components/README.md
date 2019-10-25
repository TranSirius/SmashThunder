# components folder

This folder provides all components used by the top level component `App.vue`.

## view folder

All top level components of `router-view` are stored in the `view` folder.

These components may need to implement navigation guards like `beforeRouteEnter` and `beforeRouteUpdate` to refresh their data. They may also need to watch `$root.user.loggedIn` to refresh the page when the login state is changed.

## utils folder

All components used by `Header.vue` and other `route-view` components are stored here.

These components may NOT implement navigation guards. Their data is passed by the view components.

## Header.vue

The header component provides the navbar and sign in/up form.

When user's login state is changed, navigation guards of view components should be called.