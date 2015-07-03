/*jslint vars: true, node: true, browser: true, white: true */
"use strict";

var spawnMap = require("./map");

init();

function init() {
	spawnMap(document.getElementById("geo-coordinates"));
}
