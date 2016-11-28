function LendingClubSimulator() {
	this.lcIntRateSliderId = '#lcIntRateSlider';
	this.lcDefaultRateSliderId = '#lcDefaultRateSlider';
	this.lcNumLoansFilteredDisplayId = '#lcNumLoansFilteredDisplay';
	this.currentLoansJson = null;
}
LendingClubSimulator.prototype = new LendingClubSimulator();
LendingClubSimulator.prototype.constructor = LendingClubSimulator;
let lcSimulator = new LendingClubSimulator();

LendingClubSimulator.prototype.filterLoans = function(params){
	let json = this.currentLoansJson;
	let loans = json['loans'];
	let filtered = [];
	for (let i = 0; i < loans.length; i++) {
		let defaultRate = (100*loans[i]['defaultProb']).toFixed(2);
		let intRate = loans[i]['intRate'].toFixed(2);
		let isInDefaultRateRange =  defaultRate >= params['defaultRates'][0] && defaultRate <= params['defaultRates'][1];
		let isInIntRateRange = intRate >= params['intRates'][0] && intRate <= params['intRates'][1];
		let include = isInDefaultRateRange && isInIntRateRange;
		if (include){
			filtered.push(loans[i]);
		}
	}
	return filtered;
};

LendingClubSimulator.prototype.update = function(event, ui){
	let defaultRates = getRangedSliderValues(lcSimulator.lcDefaultRateSliderId);
	let intRates = getRangedSliderValues(lcSimulator.lcIntRateSliderId);
	let params = {
		'defaultRates': defaultRates,
		'intRates': intRates,
	};
	let filtered = lcSimulator.filterLoans(params);
	$(lcSimulator.lcNumLoansFilteredDisplayId).val(filtered.length);
};

// $(function() {
//
// });
