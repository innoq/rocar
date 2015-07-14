module.exports = {
	use: ["postcss-import", "postcss-nested", "postcss-css-variables",
			"autoprefixer"],
	input: "rocar/styles/index.css",
	output: "rocar/static/bundle.css",
	autoprefixer: {
		browsers: ["> 5%"]
	}
};
