module.exports = {
	use: ["postcss-import", "postcss-nested", "postcss-css-variables",
			"autoprefixer"],
	input: "rocar/styles/index.css",
	output: "rocar/static/bundle.css",
	"postcss-import": {
		onImport: function(sources) {
			var timestamp = new Date();
			timestamp = timestamp.toISOString().replace("T", " ");
			console.log("[" + timestamp + "] recompiled CSS");

			global.watchCSS(sources);
		}
	},
	autoprefixer: {
		browsers: ["> 5%"]
	}
};
