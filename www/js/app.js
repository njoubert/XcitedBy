
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
// Long Polling
//*********************************************

function LongPoller(url, options) {
	this.frequency = options.frequency || 200;
	this.separator = options.separator || "***SEP***"
	this.url = url;

	this.timeout;
	this.doneListeners = [];
	this.packetListeners = [];
	this.errorListeners = [];

	var xhr = this.xhr = new XMLHttpRequest();
	xhr.timeout = options.timeout || 0;

	var self = this;
	xhr.onreadystatechange = function() {
		if (this.readyState == 4 && this.status != 200) {
			self.__emitError(this);
		}
	}
}

LongPoller.prototype.start = function() {
	var self = this;
	var xhr = this.xhr;

	this.xhr.open("GET", this.url, true);
	this.xhr.send();

	var dataSoFar = "";
	function parseOutPackets(newData) {
		dataSoFar += newData;

		//check whether we end with a separator:
		var completePackets = (dataSoFar.lastIndexOf(self.separator) === (dataSoFar.length - self.separator.length));

		//Now we traverse through dataSoFar to check for packet separators
		var packets = dataSoFar.split(self.separator);

		for (var i = 0; i < packets.length - 1; i++) {
			self.__emitPacket(packets[i]);
		}

		if (completePackets)
			dataSoFar = ""
		else
			dataSoFar = packets[packets.length-1];

	}

	var last_index = 0;
	function pollData() {
		if (xhr.readyState < 3) {
			self.timeout = setTimeout(pollData, self.frequency);
			return;
		}

	    var curr_index = xhr.responseText.length;

	    if (last_index == curr_index) {
	    	self.timeout = setTimeout(pollData, self.frequency); // No new data
	    	return;
	    }

	    var s = xhr.responseText.substring(last_index, curr_index);
	    last_index = curr_index;
	    parseOutPackets(s);

	    if (xhr.readyState != 4) { // As long as it's not done.
		    self.timeout = setTimeout(pollData, self.frequency);
		    return;
	    } else {
	    	self.__emitDone();
	    }

	}
	pollData();

}

LongPoller.prototype.abort = function() {
	xhr.abort();
	if (this.timeout)
		clearTimeout(this.timeout);
}

//Registering listeners
LongPoller.prototype.onPacket = function(func) {
	this.packetListeners.push(func);
	return this;
}
LongPoller.prototype.onDone = function(func) {
	this.doneListeners.push(func);
	return this;
}
LongPoller.prototype.onError = function(func) {
	this.errorListeners.push(func);
	return this;
}


//Internal function to emit a packet
LongPoller.prototype.__emitPacket = function(packet) {
	for (var i = 0; i < this.packetListeners.length; i++) {
		this.packetListeners[i](packet);
	}
}

//Internal function to emit done
LongPoller.prototype.__emitError = function() {
	for (var i = 0; i < this.errorListeners.length; i++) {
		this.errorListeners[i](this.xhr);
	}
}

//Internal function to emit done
LongPoller.prototype.__emitDone = function() {
	for (var i = 0; i < this.doneListeners.length; i++) {
		this.doneListeners[i](this.xhr);
	}
}
//***********************************************


//*********************************************
// String utils
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
			displayFSM.transitionToState('error', {textStatus:"Please enter a paper title!", compact:true});
			return false;
		}

		displayFSM.transitionToState('waiting');

		/*
		var longPoller = new LongPoller("/data/testLongPoll", {

		}).onPacket(function(packet) {
			displayFSM.transitionToState('waiting', packet);
		}).onDone(function(xhr) {
			if (xhr.status == 200)
				displayFSM.transitionToState('confirmSearch');
		}).onError(function(xhr) {
			displayFSM.transitionToState('error', {textStatus:xhr.status, errorThrown:"The server responded with an error"});
		});

		longPoller.start();
		*/ //

		$.ajax("/data/getPaper", {

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

				if (jqXHR.statusCode().status == 404) {
					displayFSM.transitionToState('error', {textStatus:textStatus, errorThrown:"The backend is currently offline"});
				} else {
					displayFSM.transitionToState('error', {textStatus:textStatus, errorThrown:errorThrown});

				}

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

	displayFSM.insertNewState("waiting", displayContext, function(message) {
		this.resultsContainer.hide();
		this.resultsData.hide();
		this.resultsConfirmation.hide();
		this.popOverContainer.show();
		this.errorContainer.hide();
		if (message) {
			this.busyText.html(message);			
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


	displayFSM.insertNewState("error", displayContext, function(options) {
		this.searchContainer.show();
		this.resultsContainer.hide();
		this.popOverContainer.hide();
		
		var errorText = "";
		if (options.textStatus)
			errorText += options.textStatus;
		if (options.textStatus && options.errorThrown)
			errorText += " - ";
		if (options.errorThrown)
			errorText += options.errorThrown;

		if (options.compact) {
			$("#errorTitle").hide();
			$("#errorFooter").hide();
		} else {
			$("#errorTitle").show();
			$("#errorFooter").show();
		}
		
		this.errorMessage.html(errorText);
		this.errorContainer.fadeIn('fast');

	});


	$("#submitbutton").click(submit);
	$("#submitform").submit(submit);

	$("#confirmbutton").click(confirm);
	$("#confirmform").submit(confirm);

	paperDeetsTemplate = _.template(document.getElementById('tmpl-paperDeets').innerHTML);


});