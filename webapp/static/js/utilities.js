
function getSlider(
	slider_id, display_id,
	min, max, step,
	init, change){
	return function() {
		$(slider_id).slider({
			range: false,
			min: min,
			max: max,
			step: step,
			value: init,
			change: change,
			slide: function(event, ui) {
				$(display_id).html(ui.value);
			},
		});
		$(display_id).html($(slider_id).slider("value"));
	}
};

function getSliderValue(id){
	let value = $(id).slider("value");
	return value;
};

function getRangedSlider(
	slider_id, display_id,
	min, max, step,
	init_min, init_max, change){
	return function() {
		$(slider_id).slider({
			range: true,
			min: min,
			max: max,
			step: step,
			values: [init_min, init_max],
			change: change,
			slide: function(event, ui) {
				$(display_id).html(ui.values[0] + " - " + ui.values[1]);
			},
		});
		$(display_id).html($(slider_id).slider("values", 0) +
			" - " + $(slider_id).slider("values", 1));
	}
};

function getRangedSliderValues(id){
	let lower = $(id).slider("values", 0);
	let upper = $(id).slider("values", 1);
	return [lower, upper];
};

function getMeanStd(list, key){
	//list is a list of dictionaries containing key
	let vals = [];
	for (let i = 0; i < list.length; i++) {
		vals.push(list[i][key]);
	}
	let mean = math.mean(vals);
	let std = math.std(vals);
	return [mean, std];
};
