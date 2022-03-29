//api called
$("#FetchData").on("focusout",function() {
    var gstNo = $(this).val();
    gstNo =gstNo.toUpperCase();
    $(this).val(gstNo)
    if(gstNo.length >=15){
       var api ='https://gst-return-status.p.rapidapi.com/gstininfo/' + gstNo;
       $.ajax({
         type: 'GET',
         url: api,
         headers: {
             "Content-Type": "application/json",
            'X-RapidAPI-Host': "gst-return-status.p.rapidapi.com",
            "X-RapidAPI-Key": "b11e8602d0mshc7cc21e6c249368p164ebejsn727e73e31698"
         },
         success: function (data) {
                console.log("starting")
               if(data.success == true){
                    var address = data['data']['details']['principalplace']
                    address = address.replace(",,",",");
                    var arr = address.split(",");
                    var state = arr[arr.length - 1];
                    var name = data['data']['details']['tradename'];
                    var pincode = data['data']['details']['pincode'];
                    $("#StateApi").val(state);
                    $("#PartyApi").val(name);
                    address = address.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                       return letter.toUpperCase();
                     });
                    $("#AddressApi").val(address +" "+ pincode);
               }
               else {
                       alert(data);
               }
           }
       });
    }
});

//adding deleteing logic
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
//qty logic
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
//rate logic
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

//calculation logic
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

//round off logic
$('#RoundOff').on('change', function() {
        var roundOffValue =$("#RoundOff").val();
		grandTotal =(parseFloat($("#sub_total").val() ) + parseFloat($("#CGST").val() ) + parseFloat($("#SGST").val() )  + parseFloat($("#IGST").val() ) -
		parseFloat($("#RoundOff").val()));
		$("#GrandTotal").val(grandTotal.toFixed(2));

});
//product change logic
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
    //gst number details filed logic
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
  //get cookies logic
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

 $('#invoiceNumber').focus(function(){
    console.log("jay meldi ma ")
  	$.ajax({
				method : "get",
				url :'invoiceNumber/' ,
				success : function(data){
                    $("#invoiceNumber").val(data['invoiceNo'])
				}
			});
 });



