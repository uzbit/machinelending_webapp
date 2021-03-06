function LendingClubLoans() {
	this.lcCurrentTableId = '#lcCurrentTable';
	this.lcAsOfDateId = '#lcAsOfDate';
	this.currentLoansJson = {};
}
LendingClubLoans.prototype = new LendingClubLoans();
LendingClubLoans.prototype.constructor = LendingClubLoans;

LendingClubLoans.prototype.getCurrentLoans = function(){
	var _this = this;
	if ($.isEmptyObject(this.currentLoansJson)){
		$.getJSON('lcApi/listedLoans/', {},
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
};

LendingClubLoans.prototype.setCurrentLoansJson = function(obj){
	obj.currentLoansJson = this.currentLoansJson;
};

LendingClubLoans.prototype.makeTable = function(){
	let json = this.currentLoansJson;
	let loans = json['loans'];
	let asOfDate = json['asOfDate'];
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
	$(this.lcAsOfDateId).text("Data current as of: " + asOfDate);
	$(this.lcCurrentTableId).DataTable({
		 "data": data,
		 "columns": [
				 { title: "Loan Id" },
				 { title: "Loan Amount" },
				 { title: "Interest Rate (%)" },
				 { title: "Grade" },
				 { title: "Purpose" },
				 { title: "Term" },
				 { title: "Default Probability (%)" },
		 ]
 	});
};

$(function() {
	let lcLoans = new LendingClubLoans();
	lcLoans.getCurrentLoans();
});
