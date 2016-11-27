
function getRangedSlider(slider_id, display_id, min, max, init_min, init_max){
	return function() {
			$(slider_id).slider({
				range: true,
				min: float(min),
				max: float(max),
				values: [init_min, init_max],
				slide: function(event, ui) {
					$(display_id).val(ui.values[0] + " - " + ui.values[1]);
				}
			});
			$(display_id).val($(slider_id).slider("values", 0) +
				" - " + $(slider_id).slider("values", 1));
	}
}
