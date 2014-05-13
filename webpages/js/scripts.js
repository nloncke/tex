// Functions for changing the search bar
function set_to_title(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by title",
    	title:"Enter only letters, numbers and whitespace"});
    $("#search_bar_text").removeAttr("pattern");
    $('#search_by').button("title");
    $("#search_form").attr({action:"/search/title/"});
    $("#search_bar_text").focus();
  }

function set_to_isbn(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by ISBN"
    	, pattern:"(^((\\s)*([0-9]-?){9}[0-9Xx](\\s)*)$)|(^((\\s)*(97[89]-?([0-9]-?){9}[0-9])(\\s)*)$)"
    	, title:"10 or 13 digit valid ISBN"
    	});
    $('#search_by').button("isbn");
    $("#search_form").attr({action:"/search/isbn/"});
    $("#search_bar_text").focus();
  }

function set_to_author(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by author",
      	pattern:"^[A-Za-z\\s\.]+$",
    	title:"Enter only letters and spaces"});
    $('#search_by').button("author");
    $("#search_form").attr({action:"/search/author/"});
    $("#search_bar_text").focus();
  }

function set_to_course(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by course (e.g. cos 333)",
      pattern:"^(\\s)*[A-Za-z]{3}(\\s)*[0-9]{3}(\\s)*$",
    	title:'Enter a valid course name e.g COS 333'});
    $('#search_by').button("course");
    $("#search_form").attr({action:"/search/course/"});
    $("#search_bar_text").focus();
  }

// dynamic responses to user inputs
$(document).ready(function()
{
  $("#search_by_title").click(set_to_title);
  $("#search_by_isbn").click(set_to_isbn);
  $("#search_by_author").click(set_to_author);
  $("#search_by_course").click(set_to_course);

  $("#buy_price_info").popover({
    trigger:"hover",
    title:"Buy now price?",
    content:"Someone who bids this price automatically \
    buys the book and closes the auction."
  });

  $("#current_price_info").popover({
    trigger:"hover",
    title:"Start price?",
    content:"The auction starts at this price; bidders \
    cannot bid below this amount.",
  });


  $("#current_price").change( function()  {
    $("#price").attr({"min": $("#current_price").val()});
  });

  $("#price").change( function() {
    $("#current_price").attr({"max": $("#price").val()});
  });

  $("#bid").change( function() {
  	var current_price = $("#current_price").val();
  	var buy_now_price = $("#buy_now_price").val();
  	$("#bid").attr({"max":buy_now_price - current_price - 1 });
  });

  // sell form scripts to follow...
  $("#is_auction").click(function () {
    if ($("#is_auction").is(':checked')) {
      $(".auction").toggle();
      $("#end_time").attr('required',true);
      $("#current_price").attr('required',true);
      $("#is_auction").val("yes");
    }
    else {
      $(".auction").toggle();
      $("#end_time").attr('required',false);
      $("#current_price").attr('required',false);
    }
  });

$("#buyback_submit").click(function () {
    var val;
    var est;
    var result;
    val = $("#buyback_price").val();
    if($("#buyback_new").is(':checked')) {
      est = val * 0.25;
    }
    else if($("#buyback_used").is(':checked')) {
      est = val * 0.2;
    }
    result = "Buyback estimate: $ "+ est.toFixed(2);
    $("#estimate").html(result);
  });


  // For toggling the navbar
  $("#collapse").on("show.bs.collapse", function() {
  	$(".nav-wrapper").height(250);
  	$("body").css("margin-top", 250);
  });

  $("#collapse").on("hide.bs.collapse", function() {
  	$(".nav-wrapper").height(72);
  	$("body").css("margin-top", 72);
  });
  
  // $('#buy-affix').affix({
    // offset: 100,
   // });

});

// -----------END OF DOCUMENT.READY-----------

// called when user clicks a link on results page
function send_isbn(isbn) {
  var idstr = '#book_result_' + isbn;
  $(idstr).submit();
  return false;
}

//	$('.countdown').countdown({
  //      date: "4/19/14 15:03:26"
    //});


// fades out prompt and fades in confirmation for buyer
// function confirm_purchase() {
  // $("#modal_body").animate( {opacity: 0}, "slow", function(){
    // $("#modal_body").html('Sweet! You just bought \
    // "{{ book.title }}" from {{ seller_id }} for ${{ offer.buy_price }}. \
    // We\'ve sent you both emails with the next steps. Enjoy!');
  // });
  // $("#modal_body").animate( {opacity: 1} );
// }


  // Unneccesary functions JUST IN CASE

  //For changing the color of the search bar when in focus
  // $("#search_bar_text").focus(function(){
    // $(this).css("background-color","#cccccc");
  // });
  // $("#search_bar_text").blur(function(){
    // $(this).css("background-color","#000000");
  // });




