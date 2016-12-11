
function LendingClubSimulator() {
	this.lcIntRateSliderId = '#lcIntRateSlider';
	this.lcDefaultRateSliderId = '#lcDefaultRateSlider';
	this.lcEarlyPayoffRateSlider = '#lcEarlyPayoffRateSlider';
	this.lcNumLoansDisplayId = '#lcNumLoansDisplay';
	this.lcNumLoansFilteredDisplayId = '#lcNumLoansFilteredDisplay';
	this.lcAvgDefaultRateDisplayId = '#lcAvgDefaultRateDisplay';
	this.lcAvgIntRateDisplayId = '#lcAvgIntRateDisplay';
	this.lcAvgSimulatedReturnDisplayId = '#lcAvgSimulatedReturnDisplay';
	this.lcCurrentTableId = '#lcInvestTable';
	this.lcAsOfDateId = '#lcAsOfDate';

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
	let payoffProb = Number(params['EarlyPayoffRate'])/100.0;
	let term = Number(loan['term']);
	let defaultProb = Number(loan['defaultProb']);
	let intRate = Number(loan['intRate']);
	let loanAmount = 25;//Number(loan['loanAmount']);
	let totalPaid = this.totalPaid(intRate, loanAmount, term);
	let monthlyPayment = totalPaid/term;

	let returns = [];
	//console.log(payoffProb/term);
	for (let i = 0; i < N; i ++){
		let defaulted = false;
		let paidoffTerm = 0;
		for (let j = 0; j < term; j++){
			if (math.random() <= defaultProb/term){
				returns.push(100.*((monthlyPayment*j)/loanAmount - 1));
				defaulted = true;
				break;
			}
			if (math.random() <= payoffProb/term){
				paidoffTerm = j+1;
				break;
			}
		}
		//console.log(defaulted + " - " + paidoffTerm);
		if (!defaulted && paidoffTerm == 0){
			returns.push(100.*(totalPaid/loanAmount - 1));
		} else if (paidoffTerm > 0){
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

LendingClubSimulator.prototype.update = function(event, ui){
	let params = {
		'defaultRates': getRangedSliderValues(lcSimulator.lcDefaultRateSliderId),
		'intRates': getRangedSliderValues(lcSimulator.lcIntRateSliderId),
		'EarlyPayoffRate': getSliderValue(lcSimulator.lcEarlyPayoffRateSlider),
		'numberIterations': 500,
	};

	lcSimulator.filterLoans(params);
	let filtered = lcSimulator.filteredLoansList;

	lcInvest.update(filtered);

	let simulatedReturns = [];
	for (let i = 0; i < filtered.length; i++){
		simulatedReturns.push(lcSimulator.simulate(filtered[i], params));
	}
	//console.log(simulatedReturns);

	$(lcSimulator.lcNumLoansDisplayId).html(lcSimulator.currentLoansJson['loans'].length);
	$(lcSimulator.lcNumLoansFilteredDisplayId).html(filtered.length);

	if (filtered.length > 0){
		let defaultProb = getMeanStd(filtered, 'defaultProb');
		$(lcSimulator.lcAvgDefaultRateDisplayId).html((100*defaultProb[0]).toFixed(2) + ' ± ' + (100*defaultProb[1]).toFixed(2));
		let intRate = getMeanStd(filtered, 'intRate');
		$(lcSimulator.lcAvgIntRateDisplayId).html(intRate[0].toFixed(2) + ' ± ' + intRate[1].toFixed(2));
		let meanReturn = getMeanStd(simulatedReturns, 'meanReturn');
		//let stdReturn = getMeanStd(simulatedReturns, 'stdReturn');
		$(lcSimulator.lcAvgSimulatedReturnDisplayId).html(meanReturn[0].toFixed(2) + ' ± ' + meanReturn[1].toFixed(2));
	} else{
		$(lcSimulator.lcAvgDefaultRateDisplayId).html("N/A");
		$(lcSimulator.lcAvgIntRateDisplayId).html("N/A");
		$(lcSimulator.lcAvgSimulatedReturnDisplayId).html("N/A");
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
	//$(this.lcAsOfDateId).text("Data current as of: " + asOfDate);
	//console.log($(this.lcCurrentTableId));
	columns = [
			{ title: "Loan Id" },
			{ title: "Loan Amount" },
			{ title: "Interest Rate (%)" },
			{ title: "Grade" },
			{ title: "Purpose" },
			{ title: "Term" },
			{ title: "Default Probability (%)" },
	];
	if ($.fn.dataTable.isDataTable(this.lcCurrentTableId)){
		table = $(this.lcCurrentTableId).DataTable();
		table.destroy();
	}
	$(this.lcCurrentTableId).DataTable({
		"data": data,
		"columns": columns,
	});
};
