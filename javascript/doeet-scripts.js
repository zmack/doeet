function todo_status_modified(e) {
  var checkbox = e.target;
  if ( checkbox.checked ) {
    $.ajax({
      type: "PUT",
      url: "/todos/" + checkbox.value + '/done',
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
  $('span.date').each( function(index,element) {
  })
  $('#todo_content, #todo_tags').focus(function(e) { $(this).parent('div').addClass('focused'); })
  $('#todo_content, #todo_tags').blur(function(e) { $(this).parent('div').removeClass('focused'); })
  $('abbr.date').each( function(index, element) {
    element.innerHTML = prettyDate(element.title);
  })
});
