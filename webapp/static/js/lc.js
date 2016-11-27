function LendingClubJS() {
	this.lcCurrentTableId = '#lcCurrentTable';
	this.lcAsOfDateId = '#lcAsOfDate';
	this.lcCurrentJson = {};
}
LendingClubJS.prototype = new LendingClubJS();
LendingClubJS.prototype.constructor = LendingClubJS;

LendingClubJS.prototype.getCurrentLoans = function(){
	var _this = this;
	if ($.isEmptyObject(this.lcCurrentJson)){
		$.getJSON('lcApi/', {},
			function(json){
				_this.lcCurrentJson = json;
				_this.makeTable();
			}
		).fail(function(jqxhr, textStatus, error ) {
			var err = textStatus + ", " + error;
		  console.log( "Request Failed: " + err );
		});
	} else {
			_this.makeTable();
	}
};

LendingClubJS.prototype.makeTable = function(){
	let json = this.lcCurrentJson;
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
