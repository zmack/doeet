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
  }
}

$( function(e) {
  $('#todos input[type="checkbox"]').click(todo_status_modified);
});
