<template>
  <div class="w-100">
    <b-card-body
      v-if="format=='md'"
      v-html="resultHTML"
    ></b-card-body>
    <iframe
      v-else
      :srcdoc="resultHTML"
      width="100%"
      seamless
      frameborder="0"
      scrolling="no"
      @load="resizeHeight"
      ref="iframe"
    ></iframe>
  </div>
</template>

<script>
import { parse, HtmlGenerator } from "latex.js";
import showdown from "showdown";

var converter = new showdown.Converter();
var generator = new HtmlGenerator({
  hyphenate: true,
  languagePatterns: "en"
});

export default {
  name: "PostDisplay",
  props: {
    format: String,
    raw: String
  },
  methods: {
    /**
     * Set iframe height to its document body's height. So the body can NOT has margin top/bottom
     */
    resizeHeight() {
      this.$refs.iframe.style.height =
        this.$refs.iframe.contentWindow.document.documentElement.scrollHeight + "px";
    }
  },
  computed: {
    resultHTML() {
      if (this.format == "md") return converter.makeHtml(this.raw);
      else {
        try {
          generator.reset();
          // The path of resource file is `/static`
          var doc = parse(this.raw, {
            generator: generator
          }).htmlDocument(window.location.protocol+'//'+window.location.host+'/static');
          return doc.documentElement.outerHTML;
        } catch (e) {
          return e.message;
        }
      }
    }
  }
};
</script>