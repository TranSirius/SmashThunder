<template>
  <div class="Content">
    <!-- Friends Activities -->
    <div v-if="loggedIn">
      <h2>Friends Activities</h2>
      <hr />
    </div>
    <!-- New posts -->
    <h2>News</h2>
    <hr />
    <div class="card-columns">
      <div class="card" v-for="num in 50" :key="num">
        <div class="card-body">
          <h5 class="card-title">Blog's Title</h5>
          <h6 class="card-subtitle mb-2">
            <a href="#">Author</a>
          </h6>
          <p
            class="card-text"
          >{{ "Blog's subtitle and other description.".repeat((Math.floor(Math.random() * 10) + 1)) }}</p>
          <p class="card-text">
            <small class="text-muted">
              Last updated {{ Math.floor(Math.random() * 10) + 1 }} mins
              ago
            </small>
          </p>
          <a href="#" class="btn btn-primary">Star</a>
          <a href="#" class="btn btn-primary">Detail</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Content"
  // props: {
  //   msg: String
  // }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
} */
</style>
