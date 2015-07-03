/*jslint vars: true, node: true, browser: true, white: true */
"use strict";

var $ = require("jquery");
global.jQuery = $; // required for formix -- XXX: should not be necessary
var spawnMap = require("./map");
var formix = require("formix");

init();

function init(subtree) {
	extract(".formix", subtree).each(function(i, form) {
		formix(form, { after: onUpdate });
		$("input:submit, button:submit", form).remove();
	});

	extract(".geo-coordinates", subtree).each(function(i, list) {
		spawnMap(list);
	});
}

function onUpdate(form, field, replacements, url, title) {
	init(replacements);
}

function extract(selector, subtree) {
	subtree = subtree || $(document.body);
	var descendants = subtree.find(selector);
	return subtree.filter(selector).add(descendants);
}
