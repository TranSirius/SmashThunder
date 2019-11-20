<template>
  <b-modal :title="title" centered hide-footer ref="modal">
    <b-form @submit.prevent="ok">
      <b-form-group>
        <b-form-input
          required
          :value="value"
          :placeholder="placeholder"
          @input="$emit('input', $event)"
        ></b-form-input>
      </b-form-group>
      <b-button variant="primary" type="submit" block>OK</b-button>
    </b-form>
  </b-modal>
</template>

<script>
/**
 * Please use `v-model` to bind value with ModalInput
 */
export default {
  name: "ModalInput",
  props: {
    title: String,
    ok: Function,
    value: String,
    placeholder: String
  },
  methods: {
    show() {
      this.$refs.modal.show();
    },
    hide() {
      this.$refs.modal.hide();
    }
  }
};
</script>