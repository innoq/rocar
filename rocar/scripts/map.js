var leaflet = require("leaflet/dist/leaflet-src");
var dom = require("uitil/dom");

leaflet.Icon.Default.imagePath = "/static/vendor/leaflet_images"; // FIXME: hard-coded

module.exports = function(container) {
	var coordinates = extractCoordinates(container);
	var origin = coordinates[0] || [40, 5];

	// wrapper ensures consistent size -- XXX: should not be necessary!?
	var wrapper = document.createElement("div");
	wrapper.style.width = "100%"; // XXX: insufficiently generic?
	wrapper.style.height = "100%"; // XXX: insufficiently generic?
	dom.replaceNode(container, wrapper);

	var map = L.map(wrapper);
	L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	var markers = coordinates.map(function(latLong) {
		return L.marker(latLong).addTo(map);
	});
	map.setView(origin, 5);
	if(markers.length) { // auto-zoom
		var group = new L.featureGroup(markers);
		map.fitBounds(group.getBounds());
	}
};

function extractCoordinates(list) {
	var links = list.querySelectorAll("a");
	return [].reduce.call(links, function(memo, link) {
		var uri = link.href;
		if(uri.indexOf("geo:") !== 0) {
			return;
		}
		var coords = uri.substr(4).split(",");
		memo.push(coords);
		return memo;
	}, []);
}
