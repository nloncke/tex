// should we accept spaces at the beginning of a query?

$(document).ready(function()
{
  $("#search_by_title").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by title"});
    $('#search_by').button("title");
    $("#search_form").attr({action:"/search/title/"});
    $("#search_bar_text").focus();
  });

  $("#search_by_isbn").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by isbn",
    	pattern:"([0-9]{10})|([0-9]{13})",
    	oninvalid:"setCustomValidity('Enter a 10 or 13 digit valid ISBN')"});
    $('#search_by').button("isbn");
    $("#search_form").attr({action:"/search/isbn/"});
    $("#search_bar_text").focus();
  });

  $("#search_by_author").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by author",
    	pattern:"[A-Za-z\\s]+",
    	oninvalid:"setCustomValidity('Enter only letters and spaces')"});
    $('#search_by').button("author");
    $("#search_form").attr({action:"/search/author/"});
    $("#search_bar_text").focus();
  });

  $("#search_by_course").click(function(){
    $("#search_bar_text").attr(
    	{placeholder:"Search by course (e.g. cos 333)",
    	pattern:"[A-Za-z]{3}(\\s)*[0-9]{3}(\\s)*",
    	oninvalid:"setCustomValidity('Enter a valid course name e.g COS 333')"});
    $('#search_by').button("course");
    $("#search_form").attr({action:"/search/course/"});
    $("#search_bar_text").focus();
  });
});