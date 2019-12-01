<template>
  <!-- This div is necessary for scroll-y -->
  <div>
    <iframe
      :srcdoc="resultHTML"
      src="/static/"
      width="100%"
      seamless
      frameborder="0"
      scrolling="no"
      v-resize="{
      /* For debug, enable `log` */
      /* log: true, */
      checkOrigin: false
      /* TODO: set `checkOrigin` to false may be dangerous */}"
    ></iframe>
  </div>
</template>

<script>
import { parse, HtmlGenerator } from "latex.js";
import showdown from "showdown";
import iFrameResize from "iframe-resizer/js/iframeResizer";
import math from "showdown-math";

var converter = new showdown.Converter({
  strikethrough: true,
  tables: true,
  tasklists: true,
  disableForced4SpacesIndentedSublists: true,
  emoji: true,
  // completeHTMLDocument: true,
  extensions: [math]
});
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
  directives: {
    // ref: https://github.com/davidjbradshaw/iframe-resizer/blob/master/docs/use_with/vue.md
    resize: {
      bind: function(el, { value = {} }) {
        el.addEventListener("load", () => iFrameResize(value, el));
      }
    }
  },
  computed: {
    resultHTML() {
      if (this.format == "md") {
        var result = `<head><base href="/data/${this.$route.params.username}/img/"></head>`;
        try {
          result += converter.makeHtml(this.raw);
        } catch (e) {
          result = e.message;
        }
        result +=
          '<link rel="stylesheet" href="/static/css/katex.css">' + // for markdown math
          "<style>body{margin:0;padding:20px}</style>" + // to make `body` has correct height
          '<script src="/static/js/iframeResizer.contentWindow.min.js"></' +
          "script>"; // for iframe-resizer
        return result;
      } else {
        try {
          generator.reset();
          // The path of resource file is `/static`
          var doc = parse(this.raw, {
            generator: generator
          }).htmlDocument(
            window.location.protocol + "//" + window.location.host + "/static/"
          );
          // append iframe resizer script
          // ref: https://stackoverflow.com/questions/9413737/how-to-append-script-script-in-javascript
          var s = doc.createElement("script");
          s.setAttribute(
            "src",
            "/static/js/iframeResizer.contentWindow.min.js" // for iframe resizer
          );
          doc.documentElement.appendChild(s);
          return doc.documentElement.outerHTML;
        } catch (e) {
          return e.message;
        }
      }
    }
  }
};
</script>