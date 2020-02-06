<!DOCTYPE html>
<html>
<head>
<script type="text/javascript" src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
<link href="{{ url_for('static', filename='css/bootstrap.css') }}" rel="stylesheet">
<link href="{{ url_for('static', filename='css/element.css') }}" rel="stylesheet">
<script type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>


<script type="text/javascript">
$(document).ready(function(){
  $("#label_status_blk").val("btc");
  $("#label_create_blk").val("btc");
  $("#label_get_info").val("btc");
  $("#label_control_gen").val("btc");
  $("#label_mining_gen").val("btc");
  $("#numbettohidden").show();
  $("#label_list_node").val("btc");


  $('input[name="optradio"]').click(function(){
    val=$(this).val();
    if(val=="btc"){
        $("#label_status_blk").val("btc");
        $("#label_list_node").val("btc");
        $("#label_create_blk").val("btc");
        $("#label_get_info").val("btc");
        $("#label_control_gen").val("btc");
        $("#label_mining_gen").val("btc");
    }
    if(val=="zch"){
        $("#label_status_blk").val("zch");
        $("#label_create_blk").val("zch");
        $("#label_get_info").val("zch");
        $("#label_list_node").val("zch");
        $("#label_control_gen").val("zch");
        $("#label_mining_gen").val("zch");
    }
  });

  $('input[name="opt_empty_random"]').click(function(){
      if($(this).attr("value")=="E"){
        $("#numbettohidden").show();
      }
      if($(this).attr("value")=="Y"){
        $("#numbettohidden").hide();
        $("#numtogen").val(0);
      } 
     if($(this).attr("value")=="R"){
        $("#numbettohidden").show();
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
<th scope="col" style="width:50%" >
<form class="ml-4" action = "/comingback" style="float:left; margin-left:5px" >
      <button type="submit" style="width:120px" class="btn btn-light" id="comingback">Net Board</button>
</form>
<form class="ml-4" action = "/listnode" method = "POST" style="float:left; margin-left:5px" >
      <input type="hidden" id="label_list_node" name="label_list_node" value="btc">
      <input type="hidden" id="whatpage" name="whatpage" value="2">
      <button onclick="on()"  type="submit" class="btn btn-light" id="listnode">List Nodes</button>
</form>
</th>
<th scope="col col-md-6" >
  <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio" id="optradio1" name="optradio" value="btc" checked>BITCOIN</label></div>
  <div class="radio form-check-inline" style="float:left; margin-left:10px">
      <label><input type="radio" id="optradio2" name="optradio" value="zch">ZCASH</label>
</div>
</th>
</thead>
</table>
<br>

<table class="table table-striped">
<tr>
<form action = "/get_info" class="form-inline" method= "POST" style="float:right; padding:5px;margin-right:5px;">
<th scope="col">
<h4>Info Node</h4></th>
<th scope="col">
  <div class="form-group row">
<label for="contnumb" class="col-form-label col-ml-2">Node Index </label>
 <div class="col-sm-10">
<input type="number" class="form-control col-md-2" id="contnumb" name="contnumb" value="1" min="1"></div>
</div>
</th>
<th scope="col">
<div class="form-check">
      <input type="radio" class="form-check-input" id="opt_info" name="opt_info" value="A" checked>
      <label class="form-check-label ml-3 font-weight-light" for="opt_info">Get all information</label></div>
<div class="form-check">
      <input type="radio" class="form-check-input" id="opt_info" name="opt_info" value="N">
      <label class="form-check-label ml-3 font-weight-light" for="opt_info">Get new address</label>
</div>
<div class="form-check">
      <input type="radio" class="form-check-input" id="opt_info" name="opt_info" value="L">
      <label class="form-check-label ml-3 font-weight-light" for="opt_info">Get listunspent</label>
</div>
</th>
<th scope="col">
<input type="hidden" id="label_get_info" name="label_get_info" value="btc">
<button type="submit" onclick="on()" class="btn btn-primary" id="get_info">Get Info</button><div>
</th>
</form>
</tr>
</table>

<table class="table table-striped">
<tr>
<th scope="col"><h4>Initialization and Generate Random Transaction</h4></th>
<th>
<form action = "/status_blockchain" method = "POST" style="float:right; padding:5px;margin-right:5px;" >
      <input type="hidden" id="label_status_blk" name="label_status_blk" value="btc">
      <button type="submit" onclick="on()" class="btn btn-primary" id="status_blk">Blockchain Status</button>
</form>
<form action = "/generate_blocks" method = "POST" style="float:right; padding:5px;margin-right:5px;">
<input type="hidden" id="label_create_blk" name="label_create_blk" value="btc">
<button type="submit" onclick="on()" class="btn btn-success" id="random_gen">Generate</button>
</th>
</tr>
<tr>
<th>
 <div class="form-check">
      <input type="radio" class="form-check-input" id="opt_empty_random" name="opt_empty_random" value="Y">
      <label class="form-check-label ml-3 font-weight-light" for="opt_empty_random">Send money to all wallet</label>
  </div>
   <div class="form-check">
      <input type="radio" class="form-check-input" id="opt_empty_random" name="opt_empty_random" value="E" checked>
      <label class="form-check-label ml-3 font-weight-light" for="empty">Generate empty blocks in order to create money
      </label>
  </div>
  <div class="form-check">
      <input type="radio" class="form-check-input" id="opt_empty_random" name="opt_empty_random" value="R">
      <label class="form-check-label ml-3 font-weight-light" for="random">Generate blocks with random transactions
      </label>
  </div>
</div>
</th>
<th scope="col">
<div class="form-row" id="numbettohidden">
<label for="num_gen" class="col-form-label">Blocks to generate</label>
<input type="number" class="form-control col-md-3" style="float:left; padding:5px;" id="numtogen" name="numtogen" value="0" min="0">
</th>
</form>
</tr>
</table>

<table class="table table-striped">
<tr>
<th scope="col" colspan="2"><h4>Generate Controlled Transaction</h4></th>
<th>
<form action = "/mining_gen" method = "POST" style="float:right; padding:5px;margin-right:5px;">
<input type="hidden" id="label_mining_gen" name="label_mining_gen" value="btc">
<button type="submit" onclick="on()" class="btn btn-success" id="mining_gen">Mine Block</button></form>
<form action = "/control_gen" method = "POST" style="float:right; padding:5px;margin-right:5px;">
<input type="hidden" id="label_control_gen" name="label_control_gen" value="btc">
<button type="submit" onclick="on()" class="btn btn-success" id="control_gen">Generate</button>
</th>
</tr>
<tr>
<th scope="col" colspan="4">
<div class="row">
<div class="form-group col-md-2">
<label for="fromaddress" class="col-form-label">From Node Index</label>
<input type="number" class="form-control" style="float:left; padding:5px;" id="fromaddress" name="fromaddress" value="1" min="1">
</div>
<div class="form-group col-md-6">
<label for="toaddress" class="col-form-label">To Address</label>
<input type="text" class="form-control" style="float:left; padding:5px;" id="toaddress" name="toaddress" placeholder="2Mt44abxuYakuKp9ud87SUvoVz7Qje4CFTZ" min="0" >
</div>
<div class="form-group col-md-2">
<label for="amount" class="col-form-label">Amount</label>
<input type="number" class="form-control" style="float:left; padding:5px;" id="amount" name="amount" value="0.00001000" min="0" step="0.00001000">
</div>
</div>
</th>
</form>
</tr>
</table>
<div>
 <div id="content">{% block content %}{% endblock %}</div>
</div>

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

