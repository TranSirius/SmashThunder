<template>
  <div class="w-100 h-100">
    <b-card-body v-if="format=='md'" v-html="resultHTML" class="w-100 h-100" style="overflow:scroll"></b-card-body>
    <iframe v-else :srcdoc="resultHTML" height="100%" width="100%" seamless frameborder="0"></iframe>
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
  computed: {
    resultHTML() {
      if (this.format == "md") return converter.makeHtml(this.raw);
      else {
        try {
          generator.reset();
          var doc = parse(this.raw, {
            generator: generator
          }).htmlDocument();
          // doc.body.appendChild(generator.stylesAndScripts("https://cdn.jsdelivr.net/npm/latex.js@0.11.1/dist/"));
          doc.body.appendChild(generator.domFragment());
          return doc.documentElement.outerHTML;
        } catch (e) {
          return e.message;
        }
      }
    }
  }
};
</script>