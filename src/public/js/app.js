

$(document).ready(function() {



	$("#submitbutton").click(function() {

		var rC = $("#resultsContainer");
		var rB = $("#resultsBox");
		var rS = $("#resultsSpinner");
		rB.html("");
		rC.hide();
		rS.show();
		rC.slideDown('slow');

		setTimeout(function() {

			rS.hide();
			rB.hide();
			rB.html("<p>sdfgsdfG</p><p>sdfgsdfG</p><p>sdfgsdfG</p><p>sdfgsdfG</p><p>sdfgsdfG</p>");
			rB.slideDown('slow');


		}, 2000);



	})

})