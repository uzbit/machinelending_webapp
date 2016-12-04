function LendingClubInvest() {
	this.lcCurrentTableId = '#lcInvestTable';
	this.lcAsOfDateId = '#lcAsOfDate';
	this.filteredLoansList = [];
}
LendingClubInvest.prototype = new LendingClubInvest();
LendingClubInvest.prototype.constructor = LendingClubInvest;
let lcInvest = new LendingClubInvest();

/*
LendingClubInvest.prototype.getCurrentLoans = function(){
	var _this = this;
	if ($.isEmptyObject(this.currentLoansJson)){
		$.getJSON('lcApi/', {},
			function(json){
				_this.currentLoansJson = json;
				_this.makeTable();
				_this.setCurrentLoansJson(lcSimulator);
				lcSimulator.update(null, null);
			}
		).fail(function(jqxhr, textStatus, error ) {
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
		});
	} else {
			_this.makeTable();
	}
};*/

LendingClubInvest.prototype.update = function(loanList){
 	this.filteredLoansList = loanList;
	if (!$.isEmptyObject(this.filteredLoansList)){
		this.makeTable();
	}
};

LendingClubInvest.prototype.makeTable = function(){
	let loans = this.filteredLoansList;
	console.log(loans);
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
	console.log($(this.lcCurrentTableId));
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

$(function() {

});
/*
Important stuff here:
$(function() {
	 $('a#calculate').bind('click', function() {
		 $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
			 a: $('input[name="a"]').val(),
			 b: $('input[name="b"]').val()
		 }, function(data) {
			 $("#result").text(data.result);
		 });
		 return false;
	 });
 });*/
