
var paperData;

var __TEST__ = false;

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
// Fake XMLHttpRequest that returns data for the long poller
//*********************************************


function TestXMLHttpRequest() {

	this.onreadystatechange = function() {};
	this.responseText = "";
	this.readyState = 0;
	this.status = 0;

	this.timer;

	var self = this;
	var spoofDataI = 0;
	this.spoofFunc = function() {

		var data = dummyData[spoofDataI];

		self.responseText += data.responseTextAppend;

		var oldReadyState = self.readyState;
		self.readyState = data.readyState;

		if (oldReadyState != data.readyState) {
			self.onreadystatechange.call(self);
		}

		spoofDataI += 1;
		if (spoofDataI < dummyData.length)
			self.timer = setTimeout(self.spoofFunc, 1000);
	}

	var dummyData = [

		{ 
			readyState: 3,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "partial",
					"stats": {"indexed": 1, "duplicates": 0, "depth": 0}, 
					"paper": {"year": "1980", "authors": "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", "venue": "SC", "title": "BLAH, a system which explains its reasoning"}, 
				}))
		},
		{ 
			readyState: 3,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "partial",
					"stats": {"indexed": 2, "duplicates": 0, "depth": 1}, 
					"paper": {"year": "1980", "authors": "M. Medina, M. Barrientos, E. Elsen, E. Darve, J. Alonso, P. Hanrahan", "venue": "SC", "title": "KABLAM"}, 
				}))
		},
		{ 
			readyState: 3,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "partial",
					"stats": {"indexed": 3, "duplicates": 0, "depth": 1}, 
					"paper": {"year": "1980", "authors": "Z. DeVito, N. Joubert, J. Alonso, P. Hanrahan", "venue": "SC", "title": "Blooieee"}, 
				}))
		},
		{ 
			readyState: 3,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "partial",
					"stats": {"indexed": 4, "duplicates": 0, "depth": 2}, 
					"paper": {"year": "1980", "authors": "N. Joubert, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", "venue": "SC", "title": "Liszt a domain specific language for cool people doing cool things"}, 
				}))
		},

		{ 
			readyState: 3,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "meta",
					"data": "done"
				}))
		},


		{ 
			readyState: 4,
			responseTextAppend: packetify(JSON.stringify(
				{
					"type": "result",
					"stats": {"indexed": 4, "duplicates": 0, "depth": 0}, 
					"paper": {"year": "1980", "authors": "N. Joubert, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", "venue": "SC", "title": "Liszt a domain specific language for cool people doing cool things"}, 
				}))
		},

	]

}

TestXMLHttpRequest.prototype.open = function() { /* dummy */ }

TestXMLHttpRequest.prototype.send = function() {
	this.status = 200;
	this.timer = setTimeout(this.spoofFunc, 500);
}


TestXMLHttpRequest.prototype.abort = function() {
	clearTimeout(this.timer);
}


//*********************************************
// Long Poller
//*********************************************

function LongPoller(url, options) {
	this.frequency = options.frequency || 200;
	this.separator = options.separator || "***SEP***"
	this.url = url;
	this.parser = options.parser || function ident(s) { return s; }

	if (options.data && typeof options.data !== "string") {
		this.url = this.url + "?" + jQuery.param(options.data, false);
	}

	this.timeout;
	this.doneListeners = [];
	this.packetListeners = [];
	this.errorListeners = [];

	var xhr = this.xhr = options.xhr || new XMLHttpRequest();
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
			self.__emitPacket(self.parser(packets[i]));
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
		this.packetListeners[i].call(this, packet);
	}
}

//Internal function to emit done
LongPoller.prototype.__emitError = function() {
	for (var i = 0; i < this.errorListeners.length; i++) {
		this.errorListeners[i].call(this, this.xhr);
	}
}

//Internal function to emit done
LongPoller.prototype.__emitDone = function() {
	for (var i = 0; i < this.doneListeners.length; i++) {
		this.doneListeners[i].call(this, this.xhr);
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

var packetify = function(str) {
	return str + "***SEP***";
}

//***********************************************


//*********************************************
// Papers database being populate
//*********************************************

// NOTICE: This code written at 65mph on the 
// Coastal Starlight zipping past Santa Barbra :-)

var paperDB = Object.create({

	__previousPaperLists: [],

	__paperList: [],

	__stats: {},

	__listeners: [],

	__trigger: function(event, payload) {
		for (var i = 0; i < this.__listeners.length; i++) {
			var listener = this.__listeners[i];
			if (listener.ev == "all" || listener.ev == event) {
				listener.fn.call(listener.ctx, payload, event);				
			}
		}
	},

	//*** Public API ***

	goBack: function() {
		//Probably a good idea to make history accessible!
	},

	goNext: function() {
		//Probably a good idea to make history accessible!
	},

	clear: function() {
		this.__previousPaperLists.push(this.__paperList);
		this.__paperList = [];
		this.__stats = [];
		this.__trigger('clear');
	},

	//Add a paper to the DB.
	addPaper: function(paper) {
		paper.__id = this.__paperList.length;
		this.__paperList.push(paper);
		this.__trigger('add:paper', paper);
	},

	setStats: function(stats) {
		this.__stats = stats;
		this.__trigger('change:stats', stats);
	},

	//Register an observer for events from the database
	on: function(event, listener, context) {
		this.__listeners.push({
			ev:  event, 
			fn:  listener,
			ctx: context || this
		});
	},

	dumpAsJSON: function() {
		return JSON.stringify({
			db: this.__paperList
		})
	}

});


//*********************************************
// PaperGrid Display
//*********************************************


$.fn.animateHighlight = function(highlightColor, duration) {
    var highlightBg = highlightColor || "#FFFF9C";
    var animateMs = duration || 1500;
    var originalBg = this.css("backgroundColor");
    this.stop().css("background-color", highlightBg).animate({backgroundColor: originalBg}, animateMs);
};

var paperGrid = Object.create({
	
	__rootEl: null,

	//list of row elements.
	//it corresponds directly to the displayed rows
	__rowEls: [],

	__db: paperDB,

	__rowTempl: null, //Set this on initialization

	init: function(options) {

		this.__rootEl = options.rootEl;
		this.__rowTempl = options.template;
		this.__db = options.db;

		this.__db.on('add:paper', function(paper) {
			this.__createRow(paper);
		}, this);

		this.__db.on('clear', this.__clear, this);

	},

	__createRow: function(paper) {

		var el = document.createElement("div");
		el.className = "paperRow";
		el.innerHTML = this.__rowTempl({paper:paper});

		//then we decide where it should go...


		//and dynamically insert it
		this.__rootEl.append(el);

		//with a highlight animation



	},

	__clear: function() {
		console.log("CLEAR THE GRID");
		this.__rootEl.html("");
	}


})


// ***************************************


var displayFSM = new DisplayFSM();

$(document).ready(function() {

	//Here we set up the finite state machine for the display's states
	var displayContext = {
		searchContainer:       $("#searchContainer"),
		resultsContainer:      $("#resultsContainer"),
		
		popOverContainer:      $("#popOverContainer"),
		busyText: 	           $("#busyText"),

		resultsConfirmation:   $("#resultsConfirmation"),
		resultsData:           $("#resultsData"),

		errorContainer: 	   $("#errorContainer"),
		errorMessage: 		   $("#errorMessage"),

		resultsPartialSpinner: $("#resultsPartialSpinner")
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

	displayFSM.insertNewState("showPartialResults", displayContext, function() {
		this.resultsPartialSpinner.show();
		this.resultsData.show();
		this.resultsContainer.show();
		this.popOverContainer.hide();
		this.resultsConfirmation.hide();
		this.errorContainer.hide();
	});

	displayFSM.insertNewState("showResults", displayContext, function() {
		this.resultsPartialSpinner.hide();
		this.resultsData.show();
		this.resultsContainer.show();
		this.popOverContainer.hide();
		this.resultsConfirmation.hide();
		this.errorContainer.hide();
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


	var paperDeetsTemplate = _.template(document.getElementById('tmpl-paperDeets').innerHTML);
	
	paperGrid.init({ 
		rootEl: $("#resultsTable"),
		db: paperDB,
		template: _.template(document.getElementById('tmpl-paperRow').innerHTML),
	});


	paperDB.on('change:stats', function(stats) {
		console.log(stats);
		$("#resultsMetadata").html("Papers Indexed: " + stats.indexed + ", Duplicated removed: " + stats.duplicates + ", Tree Depth Explored: " + stats.depth);

	})

	var confirm = function() {

		var titleToSearchFor = $("#input_title").val();
		
		var longPoller = new LongPoller("/data/getAllCitingPapersIncremental", {
			
			data: {
				title: titleToSearchFor
			},
			parser: function(packet) {
				return JSON.parse(packet);
			},
			xhr: __TEST__ ? new TestXMLHttpRequest : new XMLHttpRequest()

		}).onPacket(function(packet) {
			
			if (packet.type == "partial") {

				paperDB.setStats(packet.stats);
				paperDB.addPaper(packet.paper);

				displayFSM.transitionToState('showPartialResults');

			} else if (packet.type == "meta") {

				displayFSM.transitionToState('showResults');

			} else if (packet.type == "result") {

				displayFSM.transitionToState('showResults');

			} else {

				debugger;
				displayFSM.transitionToState('error', { textStatus: "Packet received with no or unknown type flag!", errorThrown: packet })

			}


		}).onDone(function(xhr) {
			if (xhr.status == 200)
				displayFSM.transitionToState('showResults');
		}).onError(function(xhr) {
			displayFSM.transitionToState('error', {textStatus:xhr.status, errorThrown:"The server responded with an error"});
		});

		longPoller.start();
		displayFSM.transitionToState('waiting', "Firing up Google Scholar Scrapers");

		paperDB.clear();

		return false;

	}


	var submit = function() {

			var titleToSearchFor = $("#input_title").val();

			if (!titleToSearchFor) {
				displayFSM.transitionToState('error', {textStatus:"Please enter a paper title!", compact:true});
				return false;
			}

			displayFSM.transitionToState('waiting');

			if (__TEST__) {

	                var paperData = {
	                    "title"   : "Liszt: a domain specific language for building portable mesh-based PDE solvers",
	                    "authors" : "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan",
	                    "venue"   : "SC",
	                    "year"    : 2011
	                }

					$("#paperToSearchFor").html(paperDeetsTemplate({paper: paperData}));
					$("#input_title").val(paperData.title);

					displayFSM.transitionToState('confirmSearch');

			} else {

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

			}


			return false;

	}


	$("#submitbutton").click(submit);
	$("#submitform").submit(submit);

	$("#confirmbutton").click(confirm);
	$("#confirmform").submit(confirm);

	$("#testToggle").click(function() {
		__TEST__ = this.checked;
	})

	$("#resultsDownload a").click(function() {
		console.log(paperDB.dumpAsJSON());
		return false;
	})

});