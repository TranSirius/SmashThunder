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
          <b-button size="sm" variant="secondary" @click="dismiss(data.item.id)">Dismiss</b-button>
          <b-button
            size="sm"
            class="ml-2"
            variant="outline-danger"
            @click="ban(data.item.id,data.item.target)"
          >Ban</b-button>
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
      <h5>Memory</h5>
      <b-progress :value="memory" show-progress class="mb-3"></b-progress>
      <h5>Storage</h5>
      <b-progress :value="storage" show-progress></b-progress>
    </b-card>
  </div>
</template>

<script>
import { Chart } from "chart.js";
import netapi from "../mixin/netapi";

export default {
  name: "Admin",
  mixins: [netapi],
  data() {
    return {
      search: "",
      cpu: 0,
      memory: 0,
      storage: 0,
      reportTable: {
        fields: [
          { key: "id", sortable: true },
          { key: "target", sortable: true },
          { key: "reporter", sortable: true },
          "reason",
          { key: "action", thStyle: { width: "150px" } }
        ],
        items: []
      },
      chart: {
        labels: [],
        data: [],
        title: "Latest Visits"
      }
    };
  },
  methods: {
    dismiss(id) {
      this.apiPost(
        { route: "/submit/dismiss", data: { target: id } },
        () => {
          this.reportTable.items = this.reportTable.items.filter(
            item => item.id != id
          );
        },
        "Dismiss failed."
      );
    },
    ban(id, target) {
      this.apiPost(
        { route: "/submit/ban", data: { target, report: id } },
        () => {
          this.reportTable.items = this.reportTable.items.filter(
            item => item.id != id
          );
        },
        "Ban failed."
      );
    },
    enter() {
      var ctx = document.getElementById("accessChart").getContext("2d");
      this.apiPost(
        { route: "/get/admin" },
        data => {
          this.reportTable.items = data.reports;
          this.cpu = data.cpu;
          this.memory = data.memory;
          this.storage = data.storage;
          this.chart = data.chart;
          try {
            new Chart(ctx, {
              type: "line",
              data: {
                labels: this.chart.labels,
                datasets: [
                  {
                    label: this.chart.title,
                    backgroundColor: "rgb(255, 99, 132)",
                    borderColor: "rgb(255, 99, 132)",
                    data: this.chart.data
                  }
                ]
              },
              options: {}
            });
          } catch (e) {
            this.toastErr(
              "Response format error",
              "Please contact developers."
            );
          }
        },
        "",
        () => this.to404()
      );
    }
  },
  beforeRouteEnter(to, from, next) {
    next(v => v.enter());
  }
};
</script>