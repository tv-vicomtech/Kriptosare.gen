{% extends "index.js" %}
{% block title %}Index{% endblock %}
{% block head %}
{% endblock %}
{% block content %}
<div>
  <div style="float:left; width: 50%;">
  <p class="text-primary"><b>BITCOIN INFORMATION TERMINAL</b></p>
  </div>
  <div  style="float:left; width: 50%;">
  <p class="text-info"><b>ZCASH INFORMATION TERMINAL</b></p>
  </div>
  <div id="scrolldiv1" class="terminal pre-scrollable" >
  <samp style="font-size:11px;line-height:0.1;">
   {% for m1 in message_btc %}
      <p>{{m1}}<p>
   {% endfor %}
  </samp>
  </div>
  <div id="scrolldiv2" class="pre-scrollable terminal" >
  <samp style="font-size:11px;line-height:0.1;">
     {% for m2 in message_zch %}
      <p>{{m2}}<p>
    {% endfor %}
    </samp>
  </div>
</div>

<script type="text/javascript">
  $(document).ready(function(){
    var objDiv1 = document.getElementById("scrolldiv1");
    objDiv1.scrollTop = objDiv1.scrollHeight;
    var objDiv2 = document.getElementById("scrolldiv2");
    objDiv2.scrollTop = objDiv2.scrollHeight;
  });
</script>
{% endblock %}

