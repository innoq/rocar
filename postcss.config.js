module.exports = {
	use: "postcss-use",
	input: "rocar/styles/index.css",
	output: "rocar/static/bundle.css",
	"postcss-use": {
		modules: ["postcss-import", "postcss-nested", "postcss-css-variables",
				"autoprefixer"]
	}
};
