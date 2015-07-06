/*jslint vars: true, node: true, browser: true, white: true */
"use strict";

var $ = require("jquery");
global.jQuery = $; // required for formix -- XXX: should not be necessary
var spawnMap = require("./map");
var formix = require("formix");
var simplete = require("simplete");

var historySupport = window.history && history.pushState;
if(historySupport) {
	window.addEventListener("popstate", onPopState);
}

init();

function init(subtree) {
	extract(".formix", subtree).each(function(i, form) {
		formix(form, { after: onUpdate });
		$("input:submit, button:submit", form).remove();
	});

	extract(".omnibox input[type=search]", subtree).each(function(i, field) {
		simplete(field);
	});

	extract(".geo-coordinates", subtree).each(function(i, list) {
		spawnMap(list);
	});
}

function onUpdate(form, field, replacements, url, title) {
	if(url && historySupport && url !== document.location.toString()) {
		history.pushState(null, title, url);
	}

	init(replacements);
}

function onPopState(ev) {
	// some browsers (notably Safari, but also older versions of Chrome) fire
	// the "popstate" event on initial page load, then without any state
	if(ev.state) {
		// reload to avoid application-specific caching
		document.location = document.location.toString();
	}
}

function extract(selector, subtree) {
	subtree = subtree || $(document.body);
	var descendants = subtree.find(selector);
	return subtree.filter(selector).add(descendants);
}
