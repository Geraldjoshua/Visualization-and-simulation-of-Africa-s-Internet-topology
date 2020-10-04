//Handles all button clicks on the UI and updates the data

//Adds Node, updates "data", "dij", and "routing_table"
function addNode(){
    clearTable();
   // initMap();
   // var ID = document.getElementById("NodeName").value;
    //var type = document.getElementById("NodeType").value ;
    var lat1 = parseFloat(document.getElementById("LatName1").value );
    var lat2 = parseFloat(document.getElementById("LatName2").value) ;
    var long1 = parseFloat(document.getElementById("LongT1").value) ;
    var long2 = parseFloat(document.getElementById("LongT2").value );
    
    var uluru = {lat: lat1, lng: long1};
    var nairobi = {lat: lat2, lng: long2};
    var map =document.getElementById('map');
    marker1 = new google.maps.Marker({
        map: map,
        title:"Uluru Node",
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: uluru
      });

      marker = new google.maps.Marker({
        map: map,
        title:"Nairobi Node",
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: nairobi
      });

      var lineCoordinates = [
        {lat: lat1, lng: long1},
        {lat: lat2, lng: long2},
        
        
        
      ];
      var linePath = new google.maps.Polyline({
        path: lineCoordinates,
        geodesic: true,
        strokeColor: '#FF0000'
      });

      linePath.setMap(map);
      var bounds = map.getBounds();
      bounds.extend(nairobi);bounds.extend(uluru);
      fitAllBounds(bounds,map);


    // //check NodeName not already taken
    // if(findNode(ID)) {
    //     alert("Please be a bit more original with your node name.");
    //     return false;
    // }
    // if(!validType(type)) { //check if valid type
    //     alert("Please enter a valid type.");
    //     return false;
    // }

    // let graph = getData("data");
    // let dijData = getData("dij"); 
    // graph["nodes"].push({"id":ID, "type":type});
    // dijData[ID] = {}; //create new object for new node
    // //console.log(dijData);//trace
    
    // setData("data", graph); //the usual updates ...
    // setData("dij",dijData);
    // set_routing_table(); 
    // drawGraph(); //updates UI - see visualization class
    // return true;
}

//Adds Links, updates "data", "dij", and "routing_table"
function addLink(){
    clearTable();
    var source = document.getElementById("NodeName1").value
    var target = document.getElementById("NodeName2").value
    //need to check that source and target exist
    if(findLink(source, target)){
        alert("Connection is a duplicate")
        return false;
    }
    if (findNodes(source, target)){ //does error handling in findNodes...
        let graph = getData("data");
        graph["links"].push({"source":source, "target":target});
        setData("data", graph); //updates UI
        setDijLink(source, target)//update dijkstra input
        set_routing_table();//updates routing table
        drawGraph(); //updates UI - see visualization class
    }
}

//Deletes Node, updates "data", "dij", and "routing_table"
function delNode(){ 
    clearTable();
    var ID = document.getElementById("NodeNameD").value
    let graph = getData("data");
    let dijData = getData("dij"); 
    var nodes = []; //where we push the new nodes
    var links = []; //where we push the new links

    //Remove in nodes
    var notfound = true;
    for (let i = 0; i < graph.nodes.length; i++) {
        let element = graph["nodes"][i];
        //console.log(element);//trace
        if (element.id == ID){ //if node is found, don't push
            //alert("Found Node"); //trace
            notfound = false;
        }
        else { //push current node
            nodes.push(element);
        }
    }
    if(notfound){
        alert("Node not found");
        return false;
    }
    //console.log(newGraph); //trace

    //Remove in links - returns true if successful
    for (let j = 0; j < graph.links.length; j++) {
        let e = graph["links"][j];
        let src = graph["links"][j].source;
        let dest = graph["links"][j].target;
        if ( (src==ID) || (dest==ID) ){
            //alert("Found a link"); //trace
            delete dijData[src][dest]; //removes connections in dij data
        }
        else {
            links.push(e);
        }
    }
    var newGraph = {
        "nodes":nodes,
        "links":links
    }
    delete dijData[ID]; //removes src link fromd dij data
    //console.log(dijData);//trace
    
    setData("data", newGraph); //update UI data
    setData("dij", dijData); //update dij data
    set_routing_table(); //updates routing table
    drawGraph();//update UI - potentially make this part of the setData command...
    return true;
}

//updates UI, and updates dijkstra data
function delLink(){
    clearTable();
    var srcID = document.getElementById("NodeName1D").value
    var destID = document.getElementById("NodeName2D").value
    let graph = getData("data");
    let dijData = getData("dij");
    links = []
    var notfound = true;

    for (let j = 0; j < graph.links.length; j++) {
        let e = graph["links"][j];
        let src = graph["links"][j].source;
        let dest = graph["links"][j].target;
        if ( ((src==srcID) && (dest==destID)) || ((src==destID) && (dest==srcID))  ){
            //alert("Found the link"); //trace
            notfound = false;
        }
        else {
            links.push(e);
        }
    }
    if(notfound){
        alert("Link not found"); 
        return false;
    }
    delete dijData[srcID][destID];
    delete dijData[destID][srcID];
    //console.log(dijData);//trace
    
    graph["links"] = links;
    setData("data", graph);//update UI data
    setData("dij", dijData); //update dij data
    set_routing_table(); //update routing table
    drawGraph();
    return true;
}


//handles import csv: sets up UI "data", dij input "dij", and "routing_table"
const input = document.getElementById("importinput")
input.addEventListener("change", function (e){
    clearTable();
    readCSV(input.files[0]); //did this in seperate class for sake of cleanness
});

//makes import button visible
function  clickImport(){
    if (input.style.display === "none") {
        input.style.display = "block";
    } else {
        input.style.display = "none";
    }
}

//Exports to csv
function clickExport(){
    clearTable();
    exportCSV();//true exports routing data
}

//edit Routing Table function call
function editRT(){
    var srcID = document.getElementById("NodeName1E").value
    var destID = document.getElementById("NodeName2E").value
    var newNodeID = document.getElementById("NodeName3E").value
    let routing_table = getData("routing_table")

    if (!findNodes(srcID, destID)) {return false} // check src and dest
    if (!findNode(newNodeID)) {
        alert("New routing node not valid")
        return false
    } 
    if (!checkNeighbour(srcID, newNodeID)){
        alert("New Node is not a neighbour of Source Node");
        return false;
    }
    if (!checkPath(srcID, destID, newNodeID)){
        alert("Route is not valid in this graph")
        return false;
    }
    //console.log("Valid Path") // trace


    //No problems - push changes
    routing_table[srcID][destID] = newNodeID;
    setData("routing_table", routing_table)
    clearTable();
    return true;
}

function checkPath(src, dest, newNode){
    // Counter for both IX and peer links
    var ixPeerCount = 0;
    let dij = getData("dij")
    let path = get_path(src, dest)
    let newPath = get_path(newNode, dest)

    if (dest == newNode) return true; // valid change since path of 2 nodes only
    
    let currNode = src;
    for (let i = 1; i < path.length; i++) {
        var e = dij[currNode];
        // Get type of first connection
        let t = e[path[i]].type
        // If already been through 
        if (ixPCount>2 && t != "PC"){
            return false;
        }
        if (t == "IX") ixPCount+=1;
        if (t == "P") ixPCount+=2;
        
        currNode = path[i]
    }
    return true;
}

//Toggles visibility of Div where Routing Table is Displayed
function minRT(){
    $("#divRT").toggle();
}

var iClicks = 0; // check if first RT view
var prevTab = null; // Save previous nodes name for updating of RT
//Update routing table with paths available to a specific node's
function viewRT(){
    var div = document.getElementById("divRT")
    let start = document.getElementById("NodeNameV").value 
    let routing_table = getData("routing_table")   

    if (!findNode(start)) {
        alert("Node not found")
        return false;
    } // check if valid node
    div.style.visibility = "visible"
    // if first population - no row deletion needed
    if (iClicks==0){
        for (const x in routing_table){
            addRow(start, x) // add a path to RT
        }
        iClicks++;
    }else{
        //clear old rows
        for (const x in routing_table){
            let t = document.getElementById("routingTable")       
            t.deleteRow(-1) // Delete last row from RT
        }
        // Add new rows
        for (const x in routing_table){
            addRow(start, x) // add a path to RT
        }
    }
    // To get amount of rows in last RT
    prevTab = start;
}

// Add a new row into the routing table
function addRow(start, end){
    let table1 = document.getElementById("routingTable")
    let path = get_path(start, end)
    // Check for headers
    if (table1.rows.length == 0){
        var newRow = table1.insertRow()
        var startCell = newRow.insertCell(0)
        var endCell = newRow.insertCell(1)
        var pathCell = newRow.insertCell(2)
        var pathCostCell = newRow.insertCell(3)
        var pathDelayCell = newRow.insertCell(4)
        startCell.innerHTML = "Starting Node"
        endCell.innerHTML = "End Node"
        pathCell.innerHTML = "Path Traveled"
        pathCostCell.innerHTML = "Path Cost"
        pathDelayCell.innerHTML = "Path Delay"
    }
    //insert new row to end of table
    var newRow = table1.insertRow()
    var startCell = newRow.insertCell(0)
    var endCell = newRow.insertCell(1)
    var pathCell = newRow.insertCell(2)
    var pathCostCell = newRow.insertCell(3)
    var pathDelayCell = newRow.insertCell(4)
    //set cell content
    startCell.innerHTML = start
    endCell.innerHTML = end
    let tmp = get_path(start, end)
    // Check is path not possible from get_path methods
    if (tmp==null){
        pathCell.innerHTML = "Not accessible"
        pathCostCell.innerHTML = "Not applicable"
        pathDelayCell.innerHTML = "Not applicable"
    }else{
        pathCell.innerHTML = path
        pathCostCell.innerHTML = getCost(path)
        pathDelayCell.innerHTML = getDelay(path)
    }
}
// Returns a cost for a certain path
function getCost(path){
    let dij = getData("dij") 
    var cost = 0;
    var currNode = path[0]
    for (let i = 1; i < path.length; i++) {
        const e = dij[currNode];
        cost += parseInt(e[path[i]].cost)
        currNode = path[i]
    }
    return cost;
}
// Returns Delay for a given Path
function getDelay(path){
    let dij = getData("dij") 
    var delay = 0;
    var currNode = path[0]
    for (let i = 1; i < path.length; i++) {
        const e = dij[currNode];
        delay += parseInt(e[path[i]].delay)
        currNode = path[i]
    }
    return delay;
}
// Determine of testNode is neighbour of src node
function checkNeighbour(src, testNode){
    let dij = getData("dij")    
    if (testNode in dij[src]) {
        return true}
    else{
        return false}
}

// Removes all data structures when clear button is clicked
function clearGraph(){
    var result = confirm('Are you sure?');
    if (result==false){
        return false;
    }else{
        // clear all data structures
        let graph = {"nodes": [],"links": []}
        setData("data", graph)
        let costGraph = {}
        setData("dij", costGraph)
        let routing_table = {};
        setData("routing_table", routing_table);
        let newPaths = [];
        setData("sims", newPaths)       
        let newPath = [];
        setData("simscol", newPath)  

        drawGraph();
        clearTable();
    }
    return true;
}
// Resets table for any changes in graph
function clearTable(){
    var div = document.getElementById("divRT")
    div.style.visibility = "hidden"
    var table1 = document.getElementById("routingTable")
    while ( table1.rows.length > 1 )
    {
        table1.deleteRow(-1);
    }

}

//Slider for Duration //lasts between 0.1 and 10 seconds
var sliderDur = document.getElementById("sliderDuration");
var outD = document.getElementById("simDuration");
var durValue = parseInt(sliderDur.value)/10;

outD.innerHTML = "Simulation Duration: " +durValue; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
sliderDur.oninput = function() {
    durValue = parseInt(sliderDur.value)/10;
    setData("simspeed",[true,durValue*1000,1000]);
    outD.innerHTML = "Simulation Duration: " +durValue;
}

//Slider for Frequency //between 0.01 and 1 second per node
var sliderFre = document.getElementById("sliderFrequency");
var outF = document.getElementById("simFrequency");
var freValue = parseInt(sliderFre.value)/100;

outF.innerHTML = "Simulation Frequency: " +freValue; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
sliderFre.oninput = function() {
    var freValue = parseInt(sliderFre.value)/100;
    setData("simspeed",[false,1000,freValue*1000]);
    outF.innerHTML = "Simulation Frequency: " +freValue;
}

//updates 'dij' when new links are added
function setDijLink(src, targ){
    var newDijk = getData("dij");
    var newInfo1 = determineInfo(src, targ);
    var newInfo2 = determineInfo(targ, src);

    //console.log(newInfo1);//trace
    //console.log(newInfo2);//trace

    newDijk[src][targ] = newInfo1; //adds dest info to src
    newDijk[targ][src] = newInfo2; ////adds src info to info
    //console.log(newDijk); //trace
    setData("dij", newDijk)
    return true;
}

//determines link information - could be used for error checking
function determineInfo(src, targ){
    var sType = getType(src)
    var tType = getType(targ)
    let type;
    let cost = 0; //default cost
    let delay = 1; //default delay

    if ( (sType=="IX") || (tType=="IX") ){
        type  = ("IX")
        delay = 0;
    }
    else if (sType==tType){
        type  = ("P")
    } 
    else if ( ((sType=="T1") && (tType=="T2")) || ((sType=="T1") && (tType=="T3")) || ((sType=="T2") && (tType=="T3"))){
        type = ("PC")
    }
    else if ( ((sType=="T3") && (tType=="T2")) || ((sType=="T3") && (tType=="T1")) || ((sType=="T2") && (tType=="T1"))){
        type = ("CP")
        cost = 1
    }
    var arrInfo = {
        "cost":cost,
        "type":type,
        "delay":delay
    }

    return arrInfo;
}

//could optimize this ... 
function getType(name){ //returns type of a node
    for (let i = 0; i < graph.nodes.length; i++) {
        const currNode = graph.nodes[i];
        if (currNode.id == name){
            return currNode.type;
        }
    }
}


 function openFormDN() {
    document.getElementById("myFormDN").style.display = "block";
  }
  function closeFormDN() {
    document.getElementById("myFormDN").style.display = "none";
  }

function fitAllBounds(b,map) {

    // Get north east and south west markers bounds coordinates
    var ne = b.getNorthEast();
    var sw = b.getSouthWest();
  
    // Get the current map bounds
    var mapBounds = map.getBounds();
  
    // Check if map bounds contains both north east and south west points
    if (mapBounds.contains(ne) && mapBounds.contains(sw)) {
  
      // Everything fits
      return;
  
    } else {
  
      var mapZoom = map.getZoom();
  
      if (mapZoom > 0) {
  
        // Zoom out
        map.setZoom(mapZoom - 1);
  
        // Try again
        fitAllBounds(b);
      }
    }
  }