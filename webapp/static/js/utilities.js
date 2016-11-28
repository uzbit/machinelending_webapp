
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
				slide: function(event, ui) {
					$(display_id).val(ui.values[0] + " - " + ui.values[1]);
				},
				change: change,
			});
			$(display_id).val($(slider_id).slider("values", 0) +
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
