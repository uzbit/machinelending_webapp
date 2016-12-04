
function LendingClubSimulator() {
	this.lcIntRateSliderId = '#lcIntRateSlider';
	this.lcDefaultRateSliderId = '#lcDefaultRateSlider';
	this.lcNumLoansDisplayId = '#lcNumLoansDisplay';
	this.lcNumLoansFilteredDisplayId = '#lcNumLoansFilteredDisplay';
	this.lcAvgDefaultRateDisplayId = '#lcAvgDefaultRateDisplay';
	this.lcAvgIntRateDisplayId = '#lcAvgIntRateDisplay';
	this.lcAvgNARDisplayId = '#lcAvgNARDisplay';

	this.currentLoansJson = {};
	this.filteredLoansList = [];

}
LendingClubSimulator.prototype = new LendingClubSimulator();
LendingClubSimulator.prototype.constructor = LendingClubSimulator;
let lcSimulator = new LendingClubSimulator();

LendingClubSimulator.prototype.filterLoans = function(params){
	let json = this.currentLoansJson;
	let loans = json['loans'];
	this.filteredLoansList = [];
	for (let i = 0; i < loans.length; i++) {
		let defaultRate = (100*loans[i]['defaultProb']).toFixed(2);
		let intRate = loans[i]['intRate'].toFixed(2);
		let isInDefaultRateRange =  defaultRate >= params['defaultRates'][0] && defaultRate <= params['defaultRates'][1];
		let isInIntRateRange = intRate >= params['intRates'][0] && intRate <= params['intRates'][1];
		let include = isInDefaultRateRange && isInIntRateRange;
		if (include){
			this.filteredLoansList.push(loans[i]);
		}
	}
};


LendingClubSimulator.prototype.update = function(event, ui){
	let params = {
		'defaultRates': getRangedSliderValues(lcSimulator.lcDefaultRateSliderId),
		'intRates': getRangedSliderValues(lcSimulator.lcIntRateSliderId),
	};

	lcSimulator.filterLoans(params);
	let filtered = lcSimulator.filteredLoansList;

	lcInvest.update(filtered);

	$(lcSimulator.lcNumLoansDisplayId).html(lcSimulator.currentLoansJson['loans'].length);
	$(lcSimulator.lcNumLoansFilteredDisplayId).html(filtered.length);

	if (filtered.length > 0){
		let defaultProb = getMeanStd(filtered, 'defaultProb');
		$(lcSimulator.lcAvgDefaultRateDisplayId).html((100*defaultProb[0]).toFixed(2) + ' ± ' + (100*defaultProb[1]).toFixed(2));
		let intRate = getMeanStd(filtered, 'intRate');
		$(lcSimulator.lcAvgIntRateDisplayId).html(intRate[0].toFixed(2) + ' ± ' + intRate[1].toFixed(2));
		let NAR = (intRate[0] - 100*defaultProb[0] - 1.0).toFixed(2);
		$(lcSimulator.lcAvgNARDisplayId).html(NAR);
	} else{
		$(lcSimulator.lcAvgDefaultRateDisplayId).html("N/A");
		$(lcSimulator.lcAvgIntRateDisplayId).html("N/A");
		$(lcSimulator.lcAvgNARDisplayId).html("N/A");
	}

};

// $(function() {
//
// });
