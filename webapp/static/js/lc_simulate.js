
function LendingClubSimulator() {
	this.lcIntRateSlider = '#lcIntRateSlider';
	this.lcLoanAmountSlider = '#lcLoanAmountSlider';
	this.lcDefaultRateSlider = '#lcDefaultRateSlider';
	this.lcEarlyPayoffRateSlider = '#lcEarlyPayoffRateSlider';
	this.lcNumLoansDisplay = '#lcNumLoansDisplay';
	this.lcNumLoansFilteredDisplay = '#lcNumLoansFilteredDisplay';
	this.lcAvgDefaultRateDisplay = '#lcAvgDefaultRateDisplay';
	this.lcAvgIntRateDisplay = '#lcAvgIntRateDisplay';
	this.lcAvgSimulatedReturnDisplay = '#lcAvgSimulatedReturnDisplay';
	this.lcCurrentTable = '#lcSimulateTable';
	this.lcAsOfDate = '#lcAsOfDate';
	this.lcSaveInvestParamsButton = '#lcSaveInvestParamsButton';

	this.currentLoansJson = {};
	this.filteredLoansList = [];

}
LendingClubSimulator.prototype = new LendingClubSimulator();
LendingClubSimulator.prototype.constructor = LendingClubSimulator;
let lcSimulator = new LendingClubSimulator();

LendingClubSimulator.prototype.saveInvestParams = function(){
	let params = lcSimulator.getSimulateParams();
	let backend_params = {
		'min_default_rate': params['defaultRates'][0]/100.0,
		'max_default_rate': params['defaultRates'][1]/100.0,
		'min_int_rate': params['intRates'][0],
		'max_int_rate': params['intRates'][1],
		'min_loan_amount': params['loanAmounts'][0],
		'max_loan_amount': params['loanAmounts'][1],
	};
	var _this = this;
	$.post('/lc/save_invest_params', backend_params,
		function(json){
			console.log(json);
		}
	).fail(function(jqxhr, textStatus, error ) {
		var err = textStatus + ", " + error;
	  console.log( "Request Failed: " + err );
	});
};

LendingClubSimulator.prototype.filterLoans = function(params){
	let json = this.currentLoansJson;
	let loans = json['loans'];
	this.filteredLoansList = [];
	for (let i = 0; i < loans.length; i++) {
		let defaultRate = (100*loans[i]['defaultProb']).toFixed(2);
		let intRate = loans[i]['intRate'].toFixed(2);
		let loanAmount = loans[i]['loanAmount'].toFixed(2);

		let isInDefaultRateRange =  defaultRate >= params['defaultRates'][0] && defaultRate <= params['defaultRates'][1];
		let isInIntRateRange = intRate >= params['intRates'][0] && intRate <= params['intRates'][1];
		let isInLoanAmountRange = loanAmount >= params['loanAmounts'][0] && loanAmount <= params['loanAmounts'][1];

		let include = isInDefaultRateRange &&
			isInIntRateRange && isInLoanAmountRange;
		if (include){
			this.filteredLoansList.push(loans[i]);
		}
	}
};


LendingClubSimulator.prototype.totalPaid = function(intRate, loanAmount, term){
	let r = intRate/12/100.;
	let t = term;
	let P = loanAmount;
	let A = r*P*math.pow(1+r, t)/(math.pow(1+r, t) - 1);
	return A*t;
}

LendingClubSimulator.prototype.remainingBalance = function(
		intRate, term, payment){
	let r = intRate/12/100.;
	let n = term;
	let P = payment;
	let rb = P*(1-math.pow(1+r, -(36-n)))/r;
	return rb;
}

LendingClubSimulator.prototype.simulate = function(loan, params){
	//console.log(params);
	let N = Number(params['numberIterations']);
	let payoffProb = Number(params['earlyPayoffRate'])/100.0;
	let term = Number(loan['term']);
	let defaultProb = Number(loan['defaultProb']);
	let intRate = Number(loan['intRate']);
	let loanAmount = 25;
	let totalPaid = this.totalPaid(intRate, loanAmount, term);
	let monthlyPayment = totalPaid/term;

	let returns = [];
	//console.log(payoffProb/term);
	for (let i = 0; i < N; i ++){
		let defaulted = false;
		let paidoffTerm = -1;
		for (let j = 0; j < term; j++){
			if (math.random() <= defaultProb/term){
				returns.push(100.*((monthlyPayment*j)/loanAmount - 1));
				defaulted = true;
				break;
			}
			if (math.random() <= payoffProb){
				paidoffTerm = j;
				break;
			}
		}
		//console.log(defaulted + " - " + paidoffTerm);
		if (!defaulted && paidoffTerm == -1){
			returns.push(100.*(totalPaid/loanAmount - 1));
		} else if (paidoffTerm >= 0){
			let remainingBalance = this.remainingBalance(intRate, paidoffTerm, monthlyPayment);
			let paid = (monthlyPayment*paidoffTerm) + remainingBalance;
			let ret = 100.*(paid/loanAmount - 1);
			//console.log(paidoffTerm + " " + paid + " " + ret + " " + intRate);
			returns.push(ret);
		}
	}
	return {
		'meanReturn': math.mean(returns),
		'stdReturn': math.std(returns)
	};
};
// NOTE: Calculate the chargoff distribution funciton from dataset.

LendingClubSimulator.prototype.getSimulateParams = function(){
	let params = {
		'defaultRates': getRangedSliderValues(lcSimulator.lcDefaultRateSlider),
		'intRates': getRangedSliderValues(lcSimulator.lcIntRateSlider),
		'loanAmounts': getRangedSliderValues(lcSimulator.lcLoanAmountSlider),
		'earlyPayoffRate': getSliderValue(lcSimulator.lcEarlyPayoffRateSlider),
		'numberIterations': 500,
	};
	return params;
};

LendingClubSimulator.prototype.update = function(event, ui){

	let params = lcSimulator.getSimulateParams();

	lcSimulator.filterLoans(params);
	let filtered = lcSimulator.filteredLoansList;

	lcInvest.update(filtered);

	let simulatedReturns = [];
	for (let i = 0; i < filtered.length; i++){
		simulatedReturns.push(lcSimulator.simulate(filtered[i], params));
	}
	//console.log(simulatedReturns);

	$(lcSimulator.lcNumLoansDisplay).html(lcSimulator.currentLoansJson['loans'].length);
	$(lcSimulator.lcNumLoansFilteredDisplay).html(filtered.length);

	if (filtered.length > 0){
		let defaultProb = getMeanStd(filtered, 'defaultProb');
		$(lcSimulator.lcAvgDefaultRateDisplay).html((100*defaultProb[0]).toFixed(2) + ' ± ' + (100*defaultProb[1]).toFixed(2));
		let intRate = getMeanStd(filtered, 'intRate');
		$(lcSimulator.lcAvgIntRateDisplay).html(intRate[0].toFixed(2) + ' ± ' + intRate[1].toFixed(2));
		let meanReturn = getMeanStd(simulatedReturns, 'meanReturn');
		//let stdReturn = getMeanStd(simulatedReturns, 'stdReturn');
		$(lcSimulator.lcAvgSimulatedReturnDisplay).html(meanReturn[0].toFixed(2) + ' ± ' + meanReturn[1].toFixed(2));
	} else{
		$(lcSimulator.lcAvgDefaultRateDisplay).html("N/A");
		$(lcSimulator.lcAvgIntRateDisplay).html("N/A");
		$(lcSimulator.lcAvgSimulatedReturnDisplay).html("N/A");
	}
	//if (!$.isEmptyObject(lcSimulator.filteredLoansList)){
		lcSimulator.makeTable();
	//}
};

LendingClubSimulator.prototype.makeTable = function(){
	let loans = this.filteredLoansList;
	//console.log(loans);
	let data = [];
	let columns = ['id', 'loanAmount', 'intRate', 'subGrade', 'purpose', 'term', 'defaultProb'];
	for (let i = 0; i < loans.length; i++) {
		let row = [];
		for (let j = 0; j < columns.length; j++){
			let col = columns[j];
			let val = loans[i][col];
			if (col == 'id'){
				val = "<a target='_blank' href='https://www.lendingclub.com/browse/loanDetail.action?loan_id="+val+"'>"+val+"</a>";
			}
			if (col == 'defaultProb'){
				val = (100*val).toFixed(2)
			}
			row.push(val);
		}
		data.push(row);
	}
	//$(this.lcAsOfDate).text("Data current as of: " + asOfDate);
	//console.log($(this.lcCurrentTable));
	columns = [
			{ title: "Loan Id" },
			{ title: "Loan Amount" },
			{ title: "Interest Rate (%)" },
			{ title: "Grade" },
			{ title: "Purpose" },
			{ title: "Term" },
			{ title: "Default Probability (%)" },
	];
	if ($.fn.dataTable.isDataTable(this.lcCurrentTable)){
		table = $(this.lcCurrentTable).DataTable();
		table.destroy();
	}
	$(this.lcCurrentTable).DataTable({
		"data": data,
		"columns": columns,
	});
};

LendingClubSimulator.prototype.addSaveInvestParamsButtonListener = function(){
	$(this.lcSaveInvestParamsButton).bind("click", this.saveInvestParams);
};

$(function() {
	lcSimulator.addSaveInvestParamsButtonListener();
});
