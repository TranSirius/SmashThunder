# src folder

## App.vue

`App.vue` is the top level component.

`App.vue` contains a header component and a router view.

## main.js

`main.js` is the entry file. In this file, we do the following jobs:

- Register vue plugins such as BootstrapVue.
- Config global vue, set global data, global filter.
- Register routes.
- Initialize the root vue element.

The global data is the login state of user. All components can access it by using `this.$root.$data.user`.