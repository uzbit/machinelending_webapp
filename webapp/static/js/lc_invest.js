function LendingClubInvest() {
	this.lcCurrentTableId = '#lcInvestTable';
	this.lcTotalLoansDisplay = '#lcTotalLoansDisplay';
	this.lcTotalNotesDisplay = '#lcTotalNotesDisplay';
	this.lcCostDisplay = '#lcCostDisplay';
	this.lcPurchaseButton = '#lcPurchaseButton';
	this.notesOwnedJson = {};
	this.filteredLoansList = [];
}
LendingClubInvest.prototype = new LendingClubInvest();
LendingClubInvest.prototype.constructor = LendingClubInvest;
let lcInvest = new LendingClubInvest();

LendingClubInvest.prototype.getNotesOwned = function(){
	var _this = this;
	if ($.isEmptyObject(_this.notesOwnedJson)){
		$.getJSON('lcApi/notesOwned/', {},
			function(json){
				_this.notesOwnedJson = json;
			}
		).fail(function(jqxhr, textStatus, error ) {
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
		});
	} else {
	}
};

LendingClubInvest.prototype.submitOrder = function(order){
	//console.log(order);
	if (!$.isEmptyObject(order)){
		$.post('lcApi/submitOrder/', order,
			function(json){
				console.log(json);
			}
		).fail(function(jqxhr, textStatus, error ) {
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
		});
	} else {
	}
};

LendingClubInvest.prototype.update = function(loanList){
	lcInvest.filteredLoansList = loanList;
	lcInvest.makeTable();
	lcInvest.calculateSummary();
};


LendingClubInvest.prototype.createOrder = function(){
	let order = {};
	let loans = lcInvest.filteredLoansList;
	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		//console.log($("#"+notesForId).val());
		let numToBuy = Number($("#"+notesForId).val());
		order[loans[i]['id']] = numToBuy;
	}
	lcInvest.submitOrder(order);
	
	//console.log(order);
};

LendingClubInvest.prototype.calculateSummary = function(){
	let loans = lcInvest.filteredLoansList;
	let totalLoans = 0;
	let totalNotes = 0;
	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		//console.log($("#"+notesForId).val());
		let numToBuy = Number($("#"+notesForId).val());
		if (numToBuy > 0){
			totalLoans++;
		}
		totalNotes += numToBuy;
	}
	$(lcInvest.lcTotalLoansDisplay).html(totalLoans);
	$(lcInvest.lcTotalNotesDisplay).html(totalNotes);
	$(lcInvest.lcCostDisplay).html('$ '+(25.0*totalNotes));

};

LendingClubInvest.prototype.makeTable = function(){
	let loans = this.filteredLoansList;
	let notesOwned = this.notesOwnedJson['notesOwned'];

	let data = [];
	let columns = ['numNotes', 'id', 'loanAmount', 'intRate', 'defaultProb'];
	for (let i = 0; i < loans.length; i++) {
		let row = [];
		let notesForId = "notesFor_"+loans[i]['id'];
		let numToBuy = 1;
		if (notesOwned)
			for (let j = 0; j < notesOwned.length; j++)
				if (notesOwned[j]['loanId'] == loans[i]['id']){
					numToBuy = 0;
					break;
				}

		// make the row
		for (let j = 0; j < columns.length; j++){
			let col = columns[j];
			let val = loans[i][col];
			let numToBuy = 1;

			if (col == 'numNotes'){
				val = "<input id='"+notesForId+"' type='text' style='width:50px;' value='"+numToBuy+"'>";
			}
			if (col == 'id'){
				val = "<a target='_blank' href='https://www.lendingclub.com/browse/loanDetail.action?loan_id="+val+"'>"+val+"</a>";
			}
			if (col == 'defaultProb'){
				val = (100*val).toFixed(2);
			}
			row.push(val);
		}
		data.push(row);
	}

	columns = [
			{ title: "Notes to Buy" },
			{ title: "Loan Id" },
			{ title: "Loan Amount" },
			{ title: "Interest Rate (%)" },
			/*{ title: "Grade" },
			{ title: "Purpose" },
			{ title: "Term" },*/
			{ title: "Default Probability (%)" },
	];
	if ($.fn.dataTable.isDataTable(this.lcCurrentTableId)){
		let table = $(this.lcCurrentTableId).DataTable();
		table.destroy();
	}
	$(this.lcCurrentTableId).DataTable({
		data: data,
		columns: columns,
		paging: false
	});
	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		$("#"+notesForId).change(this.calculateSummary);
	}
};

LendingClubInvest.prototype.addPurchaseButtonListener = function(){
	$(this.lcPurchaseButton).bind("click", this.createOrder);
};

$(function() {
	lcInvest.getNotesOwned();
	lcInvest.addPurchaseButtonListener();
});
