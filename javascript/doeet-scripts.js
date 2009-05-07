function todo_status_modified(e) {
  var checkbox = e.target;
  if ( checkbox.checked ) {
    $.ajax({
      type: "PUT",
      url: "/todos/" + checkbox.value + '/done',
      data: ";o", // can't sent zilch, google gets upset
      success: function(msg) {
        var todo = eval('(' + msg + ')');
        if ( todo.date_done != '-' ) {
          $('#todo-' + todo.key).parent().addClass('done');
        }
      }
    })
  } else {
    $.ajax({
      type: "PUT",
      url: "/todos/" + checkbox.value + '/reopen',
      data: ";o", // can't sent zilch, google gets upset
      success: function(msg) {
        var todo = eval('(' + msg + ')');
        if ( todo.date_done == '-' ) {
          $('#todo-' + todo.key).parent().removeClass('done');
        }
      }
    })
  }
}

$( function(e) {
  var element_date = new Date();
  $('#todos input[type="checkbox"]').click(todo_status_modified);
  $('#todo_content, #todo_tags').focus(function(e) { $(this).parent('div').addClass('focused'); })
  $('#todo_content, #todo_tags').blur(function(e) { $(this).parent('div').removeClass('focused'); })
  $('li span.content').each(
    function(index,element) {
      z = element.innerHTML.match(/http:\/\/([^/]+)[^ ]+/);
      if ( z!= null) {
        element.innerHTML = element.innerHTML.replace(z[0], '<a href="'+z[0]+'">'+z[1]+'</a>')
      }
    }) 
  $('abbr.date').each( function(index, element) {
    element.innerHTML = prettyDate(element.title);
  })
});
