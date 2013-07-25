
var actualTitle;
var actualAuthors;



//*********************************************
// Finite State Machine for handling display
//*********************************************
function DisplayFSM() {
	this.states = {};
	this.blank = true;
};

DisplayFSM.prototype.insertNewState = function(name, context, stateFunc) {
	this.states[name] = {
		context: context,
		func:    stateFunc
	}
	if (this.blank) {
		this.blank = false;
		this.transitionToState(name);
	}
}

DisplayFSM.prototype.transitionToState = function(name) {
	console.log("Display transtioning to ", name);
	var state = this.states[name];

	var args = Array.prototype.slice.call(arguments, 1);
	state.func.apply(state.context, args);
}


//***********************************************

var confirmCancel = function() {

	displayFSM.transitionToState('start');

}

var confirm = function() {

	displayFSM.transitionToState('waiting', 3000);

	setTimeout(function() {

	displayFSM.transitionToState('waiting', 2000);

	}, 1000);

	setTimeout(function() {

	displayFSM.transitionToState('waiting', 1000);

	}, 2000);

	setTimeout(function() {

		actualTitle = "Liszt: A Domain Specific Language for Building Portable Mesh-based PDE Solvers";

		$("#resultsTitle").html(actualTitle);

		$('#example1').simple_datagrid({
			data: [
				["1", "23", "Liszt: A cool thing for cool people", "Z. Devito, N. Joubert", 2011, "SUPERCOMPUTING"],
				["1", "5", "Mojo as a way to make more awesome even more awesome", "M. Roberts, G. Bobsquat, F. You", 2013, "Nature"],
				["2", "2", "Liszt: A cool thing for cool people", "Z. Devito, N. Joubert", 2011, "SUPERCOMPUTING"]
			]
		});

		displayFSM.transitionToState('showResults');



	}, 3000);

	return false;

}


var submit = function() {

		displayFSM.transitionToState('waiting');

		var titleToSearchFor = $("#submitform").val();

		$.ajax("/checkPaper", {
			success: function(jqXHR, textStatus, errorThrown) {

				actualTitle = "Liszt: A Domain Specific Language for Building Portable Mesh-based PDE Solvers";
				actualAuthors = "Zachary DeVito, Niels Joubert, Francisco Palacios, Stephen Oakley, Montserrat Medina, Mike Barrientos, Erich Elsen, Frank Ham, Alex Aiken, Karthik Duraisamy, Eric Darve, Juan Alonso, Pat Hanrahan"

				$("#resultsTitle").html(actualTitle);
				$("#resultsAuthors").html(actualAuthors);


				displayFSM.transitionToState('confirmSearch');

			},
			error: function(jqXHR, textStatus, errorThrown) {

				displayFSM.transitionToState('error', textStatus, errorThrown);

			}

		});

		return false;

}

var displayFSM = new DisplayFSM();

$(document).ready(function() {



	//Here we set up the finite state machine for the display's states
	// start - when we only have the search box
	// waiting - when we're waiting for data back from the server
	// confirmSearch - when we want the user to confirm his search
	// showResults - 
	var displayContext = {
		searchContainer:     $("#searchContainer"),
		resultsContainer:    $("#resultsContainer"),
		
		popOverContainer:    $("#popOverContainer"),
		busyText: 	         $("#busyText"),

		resultsConfirmation: $("#resultsConfirmation"),
		resultsData:         $("#resultsData"),

		errorContainer: 	 $("#errorContainer"),
		errorMessage: 		 $("#errorMessage")
	}

	displayFSM.insertNewState("start", displayContext, function() {
		this.searchContainer.show();
		this.resultsContainer.hide();
		this.errorContainer.hide();
	});

	displayFSM.insertNewState("waiting", displayContext, function(waitTime) {
		this.resultsContainer.hide();
		this.resultsData.hide();
		this.resultsConfirmation.hide();
		this.popOverContainer.show();
		this.errorContainer.hide();
		if (waitTime) {
			this.busyText.html("Expected wait time: " + waitTime/1000 + "s");			
		} else {
			this.busyText.html("");
		}
		//this.resultsContainer.slideDown('fast');
	});

	displayFSM.insertNewState("confirmSearch", displayContext, function() {
		this.searchContainer.show();
		this.resultsContainer.show();
		this.popOverContainer.hide();
		this.resultsData.hide();
		this.errorContainer.hide();
		this.resultsConfirmation.slideDown('fast');
	});

	displayFSM.insertNewState("showResults", displayContext, function() {
		this.resultsData.hide();
		this.resultsContainer.show();
		this.popOverContainer.hide();
		this.resultsConfirmation.hide();
		this.errorContainer.hide();
		this.resultsData.slideDown('fast');
	});


	displayFSM.insertNewState("error", displayContext, function(textStatus, errorThrown) {
		this.searchContainer.show();
		this.resultsContainer.hide();
		this.errorMessage.html(textStatus + " - " + errorThrown);
		this.errorContainer.fadeIn('fast');

	});


	$("#submitbutton").click(submit);
	$("#submitform").submit(submit);

	$("#confirmbutton").click(confirm);
	$("#confirmform").submit(confirm);
	$("#confirmcancelbutton").click(confirmCancel);


});