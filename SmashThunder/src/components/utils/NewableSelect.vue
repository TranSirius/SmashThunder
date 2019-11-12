<template>
  <div>
    <b-form-select
      id="postFolder"
      :value="value"
      @input="$emit('input', $event)"
      :options="computedOptions"
    ></b-form-select>
    <ModalInput
      ref="modal"
      :title="modalTitle"
      :ok="ok"
      :value="newValue"
      @input="newValue=$event;$emit('input', computedOptions[0])"
      :placeholder="modalPlaceholder"
    ></ModalInput>
  </div>
</template>

<script>
import ModalInput from "../utils/ModalInput";
import errHandler from "../mixin/errHandler";

export default {
  name: "NewableSelect",
  mixins: [errHandler],
  components: { ModalInput },
  props: {
    options: Array,
    value: String,
    modalTitle: String,
    modalPlaceholder: String,
    hint: String
  },
  data() {
    return {
      newValue: ""
    };
  },
  methods: {
    ok() {
      // check duplicated option
      for (let i = 0; i < this.options.length; i++) {
        if (this.options[i] == this.newValue) {
          this.toastErr("Input error", "Value already exist:" + this.newValue);
          this.newValue = "";
          return;
        }
      }
      // check validation
      if (this.newValue == this.hint) {
        this.toastErr("Input error", "Invalid value: " + this.newValue);
        return;
      }
      this.$refs.modal.hide();
    }
  },
  watch: {
    value: function() {
      if (this.value == this.hint) this.$refs.modal.show();
    }
  },
  computed: {
    computedOptions() {
      var result = [];
      if (this.newValue) {
        result.push(this.newValue + "(new)");
      }
      result.push(this.hint);
      for (let i = 0; i < this.options.length; i++)
        result.push(this.options[i]);
      return result;
    }
  }
};
</script>