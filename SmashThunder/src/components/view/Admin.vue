<template>
  <div>
    <!-- Search Bar -->
    <b-form inline class="mb-3">
      <label label-for="searchBar" class="ml-auto mr-sm-2">Search User</label>
      <b-form-input id="searchBar" v-model="search" placeholder="Enter username"></b-form-input>
    </b-form>
    <!-- Search Result -->
    <div></div>
    <!-- Reports -->
    <b-card title="Reports" class="mb-2">
      <b-table
        :items="reportTable.items"
        hover
        striped
        sticky-header
        sort-icon-left
        :fields="reportTable.fields"
        table-variant="danger"
        v-if="reportTable.items.length"
      >
        <template v-slot:cell(target)="data">
          <b-link :to="'/'+data.item.target">{{ data.item.target }}</b-link>
        </template>
        <template v-slot:cell(reporter)="data">
          <b-link :to="'/'+data.item.reporter">{{ data.item.reporter }}</b-link>
        </template>
        <template v-slot:cell(reason)="data">{{ data.item.reason }}</template>
        <template v-slot:cell(action)="data">
          <b-button size="sm" variant="secondary">Dismiss</b-button>
          <b-button size="sm" class="ml-2" variant="outline-danger">Ban</b-button>
        </template>
      </b-table>
      <div v-else>
        <hr />
        <h4>No undealt reports.</h4>
      </div>
    </b-card>
    <!-- Statistical Data -->
    <b-card title="Latest Visits" class="mb-2">
      <canvas id="accessChart"></canvas>
    </b-card>
    <b-card title="Backend Status">
      <hr />
      <h5>CPU usage</h5>
      <b-progress :value="cpu" show-progress class="mb-3"></b-progress>
      <!-- TODO: remove this -->
      <h5>Others</h5>
      <b-progress :value="others" show-progress></b-progress>
    </b-card>
  </div>
</template>

<script>
import { Chart } from "chart.js";

export default {
  name: "Admin",
  data() {
    return {
      search: "",
      cpu: 60,
      // TODO: remove this
      others: 80,
      reportTable: {
        fields: [
          { key: "id", sortable: true },
          { key: "target", sortable: true },
          { key: "reporter", sortable: true },
          "reason",
          { key: "action", thStyle: { width: "150px" } }
        ],
        items: [
          {
            id: 123,
            target: "someUsername",
            reporter: "anotherUsername",
            reason: "大佬真垃圾".repeat(10)
          }
        ]
      }
    };
  },
  methods: {
    enter() {
      var ctx = document.getElementById("accessChart").getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July"
          ],
          datasets: [
            {
              label: "My First dataset",
              backgroundColor: "rgb(255, 99, 132)",
              borderColor: "rgb(255, 99, 132)",
              data: [0, 10, 5, 2, 20, 30, 45]
            }
          ]
        },
        options: {}
      });
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
  }
};
</script>