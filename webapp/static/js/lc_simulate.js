function LendingClubSimulator() {
	this.lcIntRateSliderId = '#lcIntRateSlider';
	this.lcDefaultRateSliderId = '#lcDefaultRateSlider';
}
LendingClubSimulator.prototype = new LendingClubSimulator();
LendingClubSimulator.prototype.constructor = LendingClubSimulator;
let lcSimulator = new LendingClubSimulator();

LendingClubSimulator.prototype.update = function(event, ui){
	if (event){
		let intRates = getRangedSliderValues(lcSimulator.lcIntRateSliderId);
		let defaultRates = getRangedSliderValues(lcSimulator.lcDefaultRateSliderId);
		console.log(intRates);
		console.log(defaultRates);
	}
};

$(function() {
	lcSimulator.update(null, null);
});
