<!DOCTYPE html>
<html>
<head>
<script type="text/javascript" src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
<link href="{{ url_for('static', filename='css/bootstrap.css') }}" rel="stylesheet">
<link href="{{ url_for('static', filename='css/element.css') }}" rel="stylesheet">
<script type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>

<script type="text/javascript">
$(document).ready(function(){
  $("#statoshi").show();
  $("#blocksci").show();
  $("#label_list_node").val("btc");
  $("#label_create_dash").val("btc");
  $("#label_remove_dash").val("btc");
  $("#label_create_network").val("btc");
  $("#label_remove_network").val("btc");

  $('input[name="optradio"]').click(function(){
    val=$(this).val();
    if(val=="btc"){
      $("#statoshi").show();
      $("#blocksci").show();
      $("#label_list_node").val("btc");
      $("#label_create_dash").val("btc");
      $("#label_remove_dash").val("btc");
      $("#label_create_network").val("btc");
      $("#label_remove_network").val("btc");
    }
    if(val=="zch"){
      $("#statoshi").hide();
      $("#blocksci").hide();
      $("#label_list_node").val("zch");
      $("#label_create_dash").val("zch");
      $("#label_remove_dash").val("zch");
      $("#label_create_network").val("zch");
      $("#label_remove_network").val("zch");
    }

  });
});
</script>

<style>
#overlay {
    position: fixed;
    display: none;
    width: 100%;
    height: 120%;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0,0,0,0.5);
    z-index: 1;
}

#sk-circle{
    position: absolute;
    top: 50%;
    left: 50%;
    color:red;
}

</style>
</head>
<body>
<div id="overlay">
<div class="sk-circle">
  <div class="sk-circle1 sk-child"></div>
  <div class="sk-circle2 sk-child"></div>
  <div class="sk-circle3 sk-child"></div>
  <div class="sk-circle4 sk-child"></div>
  <div class="sk-circle5 sk-child"></div>
  <div class="sk-circle6 sk-child"></div>
  <div class="sk-circle7 sk-child"></div>
  <div class="sk-circle8 sk-child"></div>
  <div class="sk-circle9 sk-child"></div>
  <div class="sk-circle10 sk-child"></div>
  <div class="sk-circle11 sk-child"></div>
  <div class="sk-circle12 sk-child"></div>
</div>
</div>

<table class="table table-dark">
  <thead>
  <th scope="col" style="width:15%">
      <img src="../static/img/shield.png" class="rounded" style="margin-left:30px;width:40%" alt="Titanium img">
      </th>
     <th scope="col"><center>
      <h2 class="h2">Kriptosare: Cryptocurrencies Testbed Simulator</h2></center>
      </th>
      <th scope="col" style="width:15%">
      <img src="../static/img/logo.png" class="rounded" style="width:100%" alt="Vicomtech img">
     </th>
  </thead>
</table>

<table class="table table-dark">
<thead>
<th scope="col" style="width:50%">
<form class="ml-4" action = "/transactionboard" style="float:left; margin-left:5px" >
      <button type="submit" style="width:120px" class="btn btn-light" id="transactionboard">Tx Board</button>
</form>
<form class="ml-4" action = "/listnode" method = "POST" style="float:left; margin-left:5px" >
      <input type="hidden" id="label_list_node" name="label_list_node" value="btc">
      <input type="hidden" id="whatpage" name="whatpage" value="1">
      <button onclick="on()"  type="submit" class="btn btn-light" id="listnode">List Nodes</button>
</form>
</th>
<th scope="col col-md-6" >
  <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio"  id="optradio1" name="optradio" value="btc" checked>BITCOIN</label>
  </div>
  <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio"  id="optradio2" name="optradio" value="zch">ZCASH</label>
  </div>
</th>
</thead>
</table>

<br>

<div id="scrollall" class="pre-scrollable-mod">
<table class="table table-striped">
<tr>
<th scope="col"><h4>Creating Network</h4></th>
<th scope="col"><form action = "/status_network" method = "POST" style="float:right; padding:5px; margin-right:5px;">
      <button type="submit" onclick="on()" class="btn btn-primary" id="status">Network Status</button>
</form>
<form action = "/delete_network" method = "POST" style="float:right; padding:5px;margin-right:5px;">
      <input type="hidden" id="label_remove_network" name="label_remove_network" value="btc">
      <button onclick="on()" type="submit" class="btn btn-danger" id="remove" >Delete</button>
</form>
<form action = "/create_network" method = "POST" style="float:right; padding:5px;margin-right:5px;">
      <input type="hidden" id="label_create_network" name="label_create_network" value="btc">
  <button onclick="on()" type="submit" class="btn btn-success" id="create">Create</button>
</th>
</tr>
<tr>
<th scope="col" >
 <div class="form-row">
<label for="node" class="col-form-label">Nodes number</label>
      <input type="number" class="form-control col-md-3" style="float:left; padding:5px;" id="node" name="node" value="2" min="2">
</div>
</th><th></th>
</form>
</tr>
</table>

<table class="table table-striped">
<tr>
<th scope="col"><h4>Analytics tools</h4></th>
<th><form action = "/remove_dashboard" method = "POST" style="float:right; margin-right:5px; margin-right:5px;" >
      <input type="hidden" id="label_remove_dash" name="label_remove_dash" value="btc">
      <button onclick="on()" type="submit" class="btn btn-danger" id="removedash">Delete Dashboard</button>
</form>
<form class="ml-4" action = "/create_dash" method = "POST" style="float:right; margin-right:5px;">
      <input type="hidden" id="label_create_dash" name="label_create_dash" value="btc">
      <button onclick="on()" type="submit" class="btn btn-success" id="create_dash">Create Dashboard</button>
</th>
</tr>

<tr>
<th scope="col">
  <div class="form-check">
      <input type="checkbox" class="form-check-input" id="statoshi" name="statoshi" value="S">
      <label class="form-check-label ml-3 font-weight-light" for="statoshi">STATOSHI -><samp> port:3010</samp></label>
  </div>
  <div class="form-check">
      <input type="checkbox" class="form-check-input" id="blocksci" name="blocksci" value="B">
      <label class="form-check-label ml-3 font-weight-light" for="blocksci">BLOCKSCI -><samp> port:8868</samp></label>
  </div>
  <div class="form-check">
      <input type="checkbox" class="form-check-input" id="graphsense" name="graphsense" value="G">
      <label class="form-check-label ml-3 font-weight-light" for="graphsense">GRAPHSENSE -> <samp>btc port:8000, zch port:8010</samp></label>
  </div>
</th><th></th>
</form>
</tr>
</table>
</div>
<br><br>
 <div id="content">{% block content %}{% endblock %}</div>
<script>
function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}
</script>
</body>
</html>

