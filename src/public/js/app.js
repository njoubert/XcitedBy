
var paperData;

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


//*********************************************
// Finite State Machine for handling display
//*********************************************

var chopString = function(str, maxlen) {
	if (str.length > maxlen) {
		return str.slice(0,maxlen) + "..."
	} else {
		return str;
	}
}

//***********************************************


var paperDeetsTemplate;

var confirm = function() {

	displayFSM.transitionToState('waiting', 3000);

	setTimeout(function() {

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

		var titleToSearchFor = $("#input_title").val();

		if (!titleToSearchFor) {
			return false;
		}

		displayFSM.transitionToState('waiting');

		$.ajax("/checkPaper", {

			timeout: 120000,

			data: {
				title: titleToSearchFor
			},

			success: function(data, textStatus, jqXHR) {

				paperData = data;

				$("#paperToSearchFor").html(paperDeetsTemplate({paper: paperData}));
				$("#input_title").val(paperData.title);

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
		this.popOverContainer.hide();
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
		this.popOverContainer.hide();
		this.errorMessage.html(textStatus + " - " + errorThrown);
		this.errorContainer.fadeIn('fast');

	});


	$("#submitbutton").click(submit);
	$("#submitform").submit(submit);

	$("#confirmbutton").click(confirm);
	$("#confirmform").submit(confirm);

	$("#input_title").click(function(){
    	// Select input field contents
    	this.select();
    	return false;
}	);

	paperDeetsTemplate = _.template(document.getElementById('tmpl-paperDeets').innerHTML);

});