$(document).ready(function() {
    //onchange of checkbox ..
    $(".outer input[type=checkbox]").on("change", function() {
      //get closest outer div and then -> next outer div->input
      var slector = $(this).closest(".outer").next().find("input")
      //check if the checkbox is checked or not..
      $(this).is(":checked") ? slector.prop("disabled", false) : slector.prop("disabled", true)
      //or to hide/show :
      //$(this).is(":checked") ? slector.closest(".outer").show() : slector.closest(".outer").hide()
    })
    $(".outer input[type=checkbox]").trigger("change")
  })
  //read more here -> https://api.jquery.com/category/traversing/tree-traversal/