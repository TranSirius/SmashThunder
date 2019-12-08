const path = require("path");
const config = require("./webpack.config.js")

module.exports = {
  outputDir: "/share/SmashThunder",
  assetsDir: "static",
  configureWebpack: config, // https://cli.vuejs.org/zh/guide/webpack.html#%E7%AE%80%E5%8D%95%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F
}