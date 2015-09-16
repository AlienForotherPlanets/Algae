var ViewState = (function() {
	// Data members
	var corpusData = null;
	var spotData = null;
	var clusterDB = {};
	var cb = null;
	var state = {
		page: "spot",
		args: null
	};

	// Functions
	var flush = function() {
		cb({
			state: state,
			corpusData: corpusData,
			spotData: spotData,
			clusterDB: clusterDB
		});
	};

	var start = function(callback) {
		// Install the cb
		cb = callback;

		// Download the corpus data
		$.get("/getcorpus", function(data) {
			corpusData = data;
			state.page = "evaluate";

			// Download the clusters
			corpusData.detectors.map(function(detector) {
				detector.assignments.map(function(assign) {
					// Grab the data
					var path = corpusData.corpus_path + detector.name + "/" + assign + "/clusters.json";
					var key = getClusterKey(false, assign, detector.name);

					$.get("/getclusters?path=" + path, function(clusters) {
						clusterDB[key] = clusters;

						// Flush the data
						flush();
					});
				});
			});
		}).fail(function() {
			console.log("Failed to retreive corpus info.");

			state.page = "import";

			flush();
		});
	};

	var importCorpus = function(path) {
		// Have the server perform the corpus import process
		$.get("/importcorpus?path=" + path, function(data) {
			// Get the new corpus data JSON (by calling start again)
			start(cb);
		});
	};

	var setSpotData = function(corpusPath, assignment, file) {
		// Set the spot data
		spotData = {
			corpusPath: corpusPath,
			assignment: assignment,
			file: file
		};

		// Downlaod the clusters

		// Update the cluster DB

		// Flush
		flush();
	};

	var setState = function(page, args) {
		state = {
			page: page,
			args: args
		};

		flush();
	};

	var getClusterKey = function(fromSpot, assignment, detectorOrFilename) {
		var spotString = fromSpot ? "SPOT" : "CORPUS";

		return spotString + "_" + assignment + "_" + detectorOrFilename;
	};

	var setCluster = function(clusterKey, index, evaluation) {
		// Update the DB

		// If not a spot check, send to server

		// Flush changes back
		flush();
	}

	// return out an interface
	return {
		start: start,
		importCorpus: importCorpus,
		setSpotData: setSpotData,
		setState: setState,
		getClusterKey: getClusterKey,
		setCluster: setCluster
	};

})();