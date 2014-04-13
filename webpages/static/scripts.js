// Functions for changing the search bar
function set_to_title(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by title",
      	pattern:"^[\'\":0-9A-Za-z\\s]+$",
    	title:"Enter only letters, numbers and whitespace"});
    $('#search_by').button("title");
    $("#search_form").attr({action:"/search/title/"});
    $("#search_bar_text").focus();
  }

function set_to_isbn(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by ISBN (no dashes)"
    	, pattern:"(^((\\s)*([0-9]-?){9}[0-9Xx](\\s)*)$)|(^((\\s)*(97[89]-?([0-9]-?){9}[0-9])(\\s)*)$)"
    	, title:"10 or 13 digit valid ISBN (no dashes)"
    	});
    $('#search_by').button("isbn");
    $("#search_form").attr({action:"/search/isbn/"});
    $("#search_bar_text").focus();
  }

$(document).ready(function()
{
  // the space after the title is essential (#hack)
  if($("title").text() == "tex search results ")
    set_to_isbn();
  else
    set_to_title();

  $("#search_by_title").click(set_to_title);
  $("#search_by_isbn").click(set_to_isbn);

  $("#search_by_author").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by author",
      	pattern:"^[A-Za-z\\s]+$",
    	title:"Enter only letters and spaces"});
    $('#search_by').button("author");
    $("#search_form").attr({action:"/search/author/"});
    $("#search_bar_text").focus();
  });

  $("#search_by_course").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by course (e.g. cos 333)",
    	pattern:"^(\\s)*[A-Za-z]{3}(\\s)*[0-9]{3}(\\s)*$",
    	title:'Enter a valid course name e.g COS 333'});
    $('#search_by').button("course");
    $("#search_form").attr({action:"/search/course/"});
    $("#search_bar_text").focus();
  });

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




});