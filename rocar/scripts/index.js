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
	if(!subtree) {
		$(document.body).on("change focus blur", "label.fancy input",
				function(ev) {
			syncLabelState.apply(this, arguments);
		});
	}

	extract(".formix", subtree).each(function(i, form) {
		formix(form, { after: onUpdate });
		$("input:submit, button:submit", form).not(".manual").hide(); // XXX: bad class name
	});

	extract(".autocomplete input[type=search], input.autocomplete", subtree).
			each(function(i, field) {
		simplete(field, { autoselect: "first" });
	});

	extract(".geo-coordinates", subtree).each(function(i, list) {
		spawnMap(list);
	});

	extract("label input:checkbox, label input:radio", subtree).
			each(function(i, field) {
		var label = syncLabelState.call(field);
		label.addClass("fancy"); // TODO: rename
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

function syncLabelState(ev) {
	var field = $(this);
	var label = field.closest("label");
	if(!ev || ev.type === "change") { // XXX: overloading
		var selected = field.prop("checked");
		label.toggleClass("unselected", !selected).
			toggleClass("selected", selected);
		// reset deactivated radio buttons
		if(ev && selected && field.is(":radio")) {
			var name = field.attr("name");
			field.closest("form").find("input:radio").not(field).
					each(function(i, node) {
				if(node.name === name) {
					syncLabelState.call(node);
				}
			});
		}
	} else {
		label.toggleClass("focused", ev.type === "focusin");
	}
	return label;
}

function extract(selector, subtree) {
	subtree = subtree || $(document.body);
	var descendants = subtree.find(selector);
	return subtree.filter(selector).add(descendants);
}
