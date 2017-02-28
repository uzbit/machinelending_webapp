function LendingClubInvest() {
	this.lcCurrentTable = '#lcInvestTable';
	this.lcTotalLoansDisplay = '#lcTotalLoansDisplay';
	this.lcTotalNotesDisplay = '#lcTotalNotesDisplay';
	this.lcCostDisplay = '#lcCostDisplay';
	this.lcAvailableCashDisplay = '#lcAvailableCashDisplay';
	this.lcPurchaseButton = '#lcPurchaseButton';
	this.lcConfirmDialog = '#lcConfirmDialog';
	this.lcConfirmationTable = '#lcConfirmationTable';
	this.lcConfirmationSuccessDisplay = '#lcConfirmationSuccessDisplay';
	this.lcConfirmationErrorDisplay = '#lcConfirmationErrorDisplay';
	this.lcOrderInstruct = '#lcOrderInstructId';

	this.notesOwnedJson = {};
	this.availableCashJson = {};
	this.orderConfirmationsJson = {};
	this.filteredLoansList = [];
	this.errorsJson = {};
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

LendingClubInvest.prototype.getAvailableCash = function(){
	var _this = this;
	if ($.isEmptyObject(_this.availableCashJson)){
		$.getJSON('lcApi/availableCash/', {},
			function(json){
				_this.availableCashJson = json;
				_this.updateAvailableCash();
				//console.log(_this.availableCashJson);
			}
		).fail(function(jqxhr, textStatus, error ) {
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
		});
	} else {
	}
};

LendingClubInvest.prototype.submitOrder = function(order){
	var _this = this;
	_this.orderConfirmationsJson = {};
	if (!$.isEmptyObject(order)){
		$.post('lcApi/submitOrder/', order,
			function(json){
				if ('error' in json){
					console.log(json['error']);
					
				}
				_this.orderConfirmationsJson = json;
				_this.makeConfirmationsTable();
				_this.showConfirmationsTab(true);
				console.log(json);
			}
		).fail(function(jqxhr, textStatus, error ) {
			_this.orderConfirmationsJson = {};
			_this.errorsJson = jqxhr;
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
			_this.showConfirmationsTab(false);
		});
	} else {
	}
};

LendingClubInvest.prototype.update = function(loanList){
	lcInvest.filteredLoansList = loanList;
	lcInvest.makeTable();
	lcInvest.calculateSummary();
};

LendingClubInvest.prototype.updateConfirmations = function(loanList){

};

LendingClubInvest.prototype.createOrder = function(){
	let order = {};
	let loans = lcInvest.filteredLoansList;
	let availableCash = lcInvest.availableCashJson['availableCash'];
	let totalCost = 0;

	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		let val = $("#"+notesForId).val();
		if (!isNaN(val)){
			let numToBuy = Number(val);
			totalCost += 25*numToBuy;
			if (totalCost > availableCash){
				return {};
			}
			order[loans[i]['id']] = numToBuy;
		}
	}
	return order;
};

LendingClubInvest.prototype.calculateSummary = function(){
	let loans = lcInvest.filteredLoansList;
	let totalLoans = loans.length;
	let totalNotes = 0;
	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		//console.log($("#"+notesForId).val());
		let val = $("#"+notesForId).val();
		if (!isNaN(val)){
			let numToBuy = Number(val);
			totalNotes += numToBuy;
		}
	}
	$(lcInvest.lcTotalLoansDisplay).html(totalLoans);
	$(lcInvest.lcTotalNotesDisplay).html(totalNotes);
	$(lcInvest.lcCostDisplay).html('$ '+(25.0*totalNotes));
	lcInvest.updateAvailableCash();
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

			if (col == 'numNotes'){
				if (numToBuy > 0)
					val = "<input id='"+notesForId+"' type='text' style='width:55px;' value='"+numToBuy+"'>";
				else
					val = "<input id='"+notesForId+"' type='text' style='width:55px;' value='owned'>";
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
	if ($.fn.dataTable.isDataTable(this.lcCurrentTable)){
		let table = $(this.lcCurrentTable).DataTable();
		table.destroy();
	}
	$(this.lcCurrentTable).DataTable({
		data: data,
		columns: columns,
		paging: false
	});
	for (let i = 0; i < loans.length; i++) {
		let notesForId = "notesFor_"+loans[i]['id'];
		$("#"+notesForId).change(this.calculateSummary);
	}
};

LendingClubInvest.prototype.updateAvailableCash = function(){
	let message = "<a href='/settings/lc'>Input LC Account Info</a>"
	if (lcInvest.availableCashJson['availableCash']){
		message = '$ '+lcInvest.availableCashJson['availableCash'];
	}
	$(lcInvest.lcAvailableCashDisplay).html(message);
};

LendingClubInvest.prototype.showConfirmationsTab = function(hideErrors){
	if (hideErrors){
		$(this.lcConfirmationErrorDisplay).hide();
		$(this.lcConfirmationSuccessDisplay).show();
	} else {
		$(this.lcConfirmationErrorDisplay).show();
		$(this.lcConfirmationSuccessDisplay).hide();
	}
	$('.nav-tabs li:eq(3) a').tab('show')
};

LendingClubInvest.prototype.makeConfirmationsTable = function(){
	let json = this.orderConfirmationsJson;
	let confirmations = json['orderConfirmations'];
	let orderInstructId = json['orderInstructId'];
	let data = [];
	let columns = ['loanId', 'requestedAmount', 'investedAmount', 'executionStatus'];
	for (let i = 0; i < confirmations.length; i++) {
		let row = [];
		for (let j = 0; j < columns.length; j++){
			let col = columns[j];
			let val = confirmations[i][col];
			if (col == 'loanId'){
				val = "<a target='_blank' href='https://www.lendingclub.com/browse/loanDetail.action?loan_id="+val+"'>"+val+"</a>";
			}
			row.push(val);
		}
		data.push(row);
	}
	$(this.lcConfirmationTable).DataTable({
		 "data": data,
		 "columns": [
				 { title: "Loan Id" },
				 { title: "Requested Amount" },
				 { title: "Invested Amount" },
				 { title: "Execution Status" },
		 ]
 	});
	$(this.lcOrderInstruct).html("Order #<b>"+orderInstructId+"</b> fulfilled.<p></p>");

};

LendingClubInvest.prototype.openConfirmationDialog = function(){
	lcInvest.setupConfirmationDialog();
	$(lcInvest.lcConfirmDialog).dialog("open");
};

LendingClubInvest.prototype.addPurchaseButtonListener = function(){
	$(this.lcPurchaseButton).bind("click", this.openConfirmationDialog);
};

LendingClubInvest.prototype.setupConfirmationDialog = function(){
	let order = lcInvest.createOrder();
	let buttons = [];
	//console.log(order.length);
	if ($.isEmptyObject(order)){
		$(lcInvest.lcConfirmDialog).html("Insufficient funds or invalid order.");
		buttons = [
			{
				text: "Close",
				click: function() {
					$(this).dialog("close");
				}
			}
		];

	} else if (!lcInvest.availableCashJson['availableCash']){
		$(lcInvest.lcConfirmDialog).html("Have you input your <a href='/settings/lc'>LC Account Info</a> in yet?");
		buttons = [
			{
				text: "No",
				click: function() {
					$(this).dialog("close");
				}
			}
		];
	} else {
		$(lcInvest.lcConfirmDialog).html("Are you sure you wish to purchase these notes?");
		buttons = [
			{
				text: "Yes",
				click: function() {
					lcInvest.submitOrder(order);
					$(this).dialog("close");
				}
			},
			{
				text: "No",
				click: function() {
					$(this).dialog("close");
				}
			}
		];
	}

	$(lcInvest.lcConfirmDialog).dialog({
		autoOpen: false,
		modal: true,
		dialogClass: "no-close",
		buttons: buttons,
	});
};

$(function() {
	lcInvest.getNotesOwned();
	lcInvest.getAvailableCash();
	lcInvest.addPurchaseButtonListener();
});
