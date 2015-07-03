module.exports = {
	entry: "./rocar/scripts/index.js",
	output: {
		path: __dirname + "/rocar/static",
		filename: "bundle.js"
	},
	module: {
		loaders: [
			{ test: /\.coffee$/, loader: "coffee-loader" }
		]
	}
};
