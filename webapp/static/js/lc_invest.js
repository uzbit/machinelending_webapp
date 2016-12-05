function LendingClubInvest() {
	this.filteredLoansList = [];
}
LendingClubInvest.prototype = new LendingClubInvest();
LendingClubInvest.prototype.constructor = LendingClubInvest;
let lcInvest = new LendingClubInvest();


LendingClubInvest.prototype.getNotesOwned = function(){
	var _this = this;
	if ($.isEmptyObject(this.currentLoansJson)){
		$.getJSON('lcApi/notesOwned/', {},
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

};

$(function() {
	let lcInvest = new LendingClubInvest();
	lcInvest.getNotesOwned();
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
