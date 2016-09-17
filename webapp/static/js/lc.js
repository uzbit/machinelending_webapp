function LendingClubJS() {
	this.lcTableId = '#lcTable';
	this.lcAsOfDateId = '#lcAsOfDate';
}
LendingClubJS.prototype = new LendingClubJS();
LendingClubJS.prototype.constructor = LendingClubJS;

LendingClubJS.prototype.getCurrentLoans = function(){
	var this_ = this;
	console.log("HERE");
			
	$.getJSON('lcApi/', {},
		function(json){
			console.log("HERE2");
			this_.makeTable(json);
		}
	).fail(function(jqxhr, textStatus, error ) {
		var err = textStatus + ", " + error;
	    console.log( "Request Failed: " + err );
	});
};

LendingClubJS.prototype.makeTable = function(json){
	let loans = json['loans'];
	let asOfDate = json['asOfDate'];
	let data = [];
	let columns = ['id', 'loanAmount', 'intRate', 'subGrade', 'purpose', 'defaultProb'];
	for (let i = 0; i < loans.length; i++) {
		let row = [];
		for (let j = 0; j < columns.length; j++){
			let col = columns[j];
			let val = loans[i][col];
			if (col == 'id'){
				val = "<a target='_blank' href='https://www.lendingclub.com/browse/loanDetail.action?loan_id="+val+"'>"+val+"</a>";
			}
			row.push(val);
		}
		data.push(row);
	}
	$(this.lcAsOfDateId).text("Data current as of: " + asOfDate);
	$(this.lcTableId).DataTable({
		 "data": data,
		 "columns": [
				 { title: "Loan Id" },
				 { title: "Loan Amount" },
				 { title: "Interest Rate" },
				 { title: "Grade" },
				 { title: "Purpose" },
				 { title: "Default Probability" },
		 ]
 	});
};

$(function() {
	let lcJS = new LendingClubJS();
	lcJS.getCurrentLoans();
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
