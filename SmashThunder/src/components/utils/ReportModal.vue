<template>
  <b-modal
    ref="modal"
    title="Report"
    header-bg-variant="danger"
    header-text-variant="light"
    centered
    hide-footer
  >
    <b-form @submit.prevent="report">
      <b-form-group :label="'You are reporting: '+target">
        <b-form-textarea v-model="reason" placeholder="Report reason..." rows="3" max-rows="6"></b-form-textarea>
      </b-form-group>
      <b-button type="submit" variant="danger" block>Report</b-button>
    </b-form>
  </b-modal>
</template>

<script>
import netapi from "../mixin/netapi";

export default {
  name: "ReportModal",
  mixins: [netapi],
  props: {
    target: String,
    reporter: String,
    reason: String
  },
  methods: {
    show() {
      this.$refs.modal.show();
    },
    hide() {
      this.$refs.modal.hide();
    },
    report() {
      this.hide();
      this.apiPost(
        {
          route: "/submit/report",
          data: {
            reporter: this.reporter,
            target: this.target,
            reason: this.reason
          }
        },
        () =>
          this.toastErr(
            "Succeed",
            "Your report has been submitted.",
            "success"
          ),
        "Report Error."
      );
    }
  }
};
</script>