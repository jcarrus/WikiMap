var openRequests = 0;
var goalDepth;
var numOpen = 0;
var maxOpen = 10;
var startTime;
var q = queue(maxOpen);
q.add = function(){ increment(); this.defer.apply(this, arguments); };

var mwjs = MediaWikiJS('https://en.wikipedia.org');
var root;
// A function that takes a search string as a parameter and returns a node object.
var search = function(depth){
	startTime = new Date();
	console.log("begin search at ");
	console.log(startTime);
	goalDepth = depth;
	numNodes = 1;
	var rootName = "Amy B. Smith";
	root = new Node(rootName);
	q.add(getChildren, root, null);
	q.awaitAll(function(){
		console.log("complete after");
		console.log(((new Date()) - startTime)/1000);
		console.log("seconds");
		prune(root);
		newplot(root);
	});
};

function Node(title, parent){
	this.title = title;
	this.parent = parent;
	this.depth = (this.parent) ? this.parent.depth + 1 : 0;
	this.children = [];
}

function getChildren(root, myContinue, callback){
	var numResults = 500;
	var query = {
		action: 'query',
	    list: 'backlinks', 
	    bltitle: root.title,
	    blnamespace: '0', 
	    bllimit: numResults, 
	    blfilterredir: 'nonredirects'
	};
	if (myContinue){
		query.continue = myContinue.continue;
		query.blcontinue = myContinue.blcontinue;
	}
	mwjs.send(query, function (d){
		var links = d.query.backlinks.map(function(d){ return d.title; });
		for (var link in links){
			var child = new Node(links[link], root);
			root.children.push(child);
			if (child.depth < goalDepth){
				q.add(getChildren, child, null);
			}
		}
		if (d.continue){
			q.add(getChildren, root, d.continue);
		}
		callback(null, null);
	});
}

function prune(root){
	return root;
}

function increment(){
	if (++numNodes % 1000 === 0){
		var nps = numNodes / (new Date() - startTime) * 1000;
		console.log('Searched through %s nodes at %s nodes/second', numNodes, nps);
	}
}

var garbageBin;
window.onload = function (){
    if (typeof(garbageBin) === 'undefined'){
        //Here we are creating a 'garbage bin' object to temporarily 
        //store elements that are to be discarded
        garbageBin = document.createElement('div');
        garbageBin.style.display = 'none'; //Make sure it is not displayed
        document.body.appendChild(garbageBin);
    }
    
};

function discardElement(element){
        //The way this works is due to the phenomenon whereby child nodes
        //of an object with it's innerHTML emptied are removed from memory

        //Move the element to the garbage bin element
        garbageBin.appendChild(element);
        //Empty the garbage bin
        garbageBin.innerHTML = "";
    }