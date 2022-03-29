
$("#FetchData").on("focusout",function() {
    var gstNo = $(this).val();
    gstNo =  gstNo.toUpperCase();
    console.log(gstNo)
    if(gstNo.length >=15){
       var api ='https://sheet.gstincheck.co.in/check/368cf73ec7264094401941e475eaa4a0/' + gstNo;
       $.ajax({
         type: 'GET',
         url: api,
         success: function (data) {
               if(data.flag == true){
                   var partyName = data.data['tradeNam']
                   var address = data.data['pradr']['adr']
                   var state = data.data['pradr']['addr']['stcd']
                   $('#PartyApi').val(partyName);
                   $('#AddressApi').val(address)
                   $('#StateApi').val(state)
               }
               else {
                       alert(data);
               }
           }
       });
    }
});
var i=1;
$(document).ready(function(){
       $("#add_row").click(function(e){
        e.preventDefault();
       b=i-1;
      $('#addr'+i).html($('#addr'+b).html()).find('td:first-child').html(i+1);
      $('#tab_logic').append('<tr id="addr'+(i+1)+'"></tr>');
      i++;
  });
     $("#delete_row").click(function(e){
       e.preventDefault()
    	 if(i>1){
		 $("#addr"+(i-1)).html('');
		 i--;
		 }
	 });

});

$('#TBody').delegate(".qty",'keyup', function() {
            var qty = $(this);
            var tr = $(this).parent().parent();
            if (qty.val() == null || qty.val() == '') {
			      alert("Please enter a valid quantity");
		   }
		   else{
		      calculate();
		   }

});

$('#TBody').delegate(".rate",'keyup', function() {
           rate = $(this);
            var tr = $(this).parent().parent();
            if (rate.val() == null || rate.val() == '') {
			      alert("Please enter a valid quantity");
		   }else {
		        tr.find(".amount").val(rate.val() * tr.find(".qty").val());
		        calculate();
		       }
		   });
function calculate(){
        var sub_total = 0;
        $(".amount").each(function(){
		       sub_total += ($(this).val() * 1);
		});
		$("#sub_total").val(sub_total);
		var state = $("#Party_state").val().trim().toLowerCase();
        $("#RoundOff").val(0.00);
		if (state == "gujarat"){
		        var gst  = sub_total * 9 / 100;
		        var convertFixSize = gst.toFixed(2);
		        $("#CGST").val(convertFixSize);
		        $("#SGST").val(convertFixSize);
		        $("#IGST").val(0.00);
		}else{
		        var sub_total = sub_total * 18 / 100
		        var convertFixSize = sub_total.toFixed(2);
		        $("#CGST").val(0.00);
		        $("#SGST").val(0.00);
		        $("#IGST").val(convertFixSize);
		}
		var roundOffValue = parseFloat( $("#RoundOff").val());
		var grandTotal;
		grandTotal =sub_total + (parseFloat($("#CGST").val() ) + parseFloat($("#SGST").val() )  + parseFloat($("#IGST").val() ) -
		parseFloat($("#RoundOff").val() ) );
		$("#GrandTotal").val(grandTotal.toFixed(2));
}
$('#RoundOff').on('change', function() {
        var roundOffValue =$("#RoundOff").val();
		grandTotal =(parseFloat($("#sub_total").val() ) + parseFloat($("#CGST").val() ) + parseFloat($("#SGST").val() )  + parseFloat($("#IGST").val() ) -
		parseFloat($("#RoundOff").val()));
		$("#GrandTotal").val(grandTotal.toFixed(2));

});

$('#TBody').delegate(".orderName",'change', function() {
     var productId = $(this).val();
     var tr = $(this).parent().parent();
         $.ajax({
         type:"GET",
         url: "productOne/" + productId,
         success: function (data) {
                    tr.find(".hsn").val(data['product'][0]['hsn_code']);
                    tr.find(".per").val(data['product'][0]['per']);
               }
         });
  });

  $('#Meldi').on('change', function() {
        var partyId = $(this).val();
         $.ajax({
         type:"GET",
         url: "gstNo/" + partyId,
         success: function (data) {
                        var d = new Date();
                        var strDate = d.getDate() + "/" + (d.getMonth()+1) + "/" + d.getFullYear();
                         $("#PartyUnique").val(data['party'][0]["party_name"]);
                         $("#Party_state").val(data['party'][0]["state"]);
                         $("#Party_date").val(strDate);
                         $("#Party_mobile").val(data['party'][0]["phone_no"]);
                         $("#party_address").val(data['party'][0]["address"]);
               }
         });
  });
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
csrf_token = getCookie('csrftoken');

 $('#mainForm').on('submit', function(e){
    e.preventDefault();
    isValid = true;
    if(confirm('Are you want to print and insert the Invoice ?')){
     if($("#Meldi").val() == ""){
        alert("Gst number Not Selected")
        isValid=false;
     }
     if($(".orderName").val() == ""){
        alert("Product Name not Selected")
        isValid=false;
     }
     if($(".qty").val() == ""){
        alert("Qty Not filled");
        isValid=false;
     }
     if($(".rate").val() == ""){
        alert("Rate Not filled")
        isValid = false;
     }
     if(isValid == true){
   	$.ajax({
				url :'allData/' ,
				headers: { "X-CSRFToken":csrf_token },
				method : "POST",
				data : $('#mainForm').serialize() ,
				success : function(data){
                    window.location = "print/";
				}
			});
			}
    }
 });



