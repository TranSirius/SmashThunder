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
import iFrameResize from "iframe-resizer";
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
        // for user img display
        var result = `<head><base href="/data/${this.$route.params.username}/img/"></head>`;
        // render markdown
        try {
          result += converter.makeHtml(this.raw);
        } catch (e) {
          result = e.message;
        }
        result +=
          '<link rel="stylesheet" href="/static/css/katex.css">' + // for markdown math
          "<style>body{margin:0;padding:20px}</style>" + // to make `body` has correct height
          '<script src="https://cdn.bootcss.com/iframe-resizer/4.2.1/iframeResizer.contentWindow.min.js"></' +
          "script>"; // for iframe-resizer
        return result;
      } else {
        try {
          generator.reset();
          // The path of resource file is `/static`
          var doc = parse(this.raw, {
            generator: generator
          }).htmlDocument("https://cdn.jsdelivr.net/npm/latex.js@0.11.1/dist/");

          // append iframe resizer script
          // ref: https://stackoverflow.com/questions/9413737/how-to-append-script-script-in-javascript
          var s = doc.createElement("script");
          s.setAttribute(
            "src",
            "https://cdn.bootcss.com/iframe-resizer/4.2.1/iframeResizer.contentWindow.min.js" // for iframe resizer
          );
          doc.documentElement.appendChild(s);

          // fix links in iframe
          [...doc.getElementsByTagName("a")].map(el => {
            var href = el.getAttribute("href");
            if (href.startsWith("#")) {
              // fix anchors in iframe
              // ref: https://stackoverflow.com/questions/42475012/how-to-make-href-anchors-in-iframe-srcdoc-actually-work/59004815#59004815
              el.setAttribute("href", "about:srcdoc" + href);
            } else {
              // open absolute link in parent page
              el.setAttribute("target", "_parent");
            }
          });

          return doc.documentElement.outerHTML;
        } catch (e) {
          return e.message;
        }
      }
    }
  }
};
</script>