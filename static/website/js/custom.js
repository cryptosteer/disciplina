$(document).ready(function() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function loadform(form_url){
  var modal = $('#modal');
  $.ajax({
    url: form_url,
    context: document.body
  }).done(function(response) {
    modal.html(response);
  });
}

var form_options = { 
    success: function(response) {
        $('#data-table').DataTable().ajax.reload(null, false);
        $('#modal').modal('hide');
        toastr.success(response);
    },
    error: function() {
        $('#data-table').DataTable().ajax.reload(null, false);
        $('#modal').modal('hide');
        toastr.error("Error, please contact the system administrator");
    }
};

toastr.options = {
  "closeButton": true,
  "newestOnTop": false,
  "progressBar": true,
  "debug": false,
  "positionClass": "toast-top-right",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

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

function save_order(url){
  var table = $('#data-table').DataTable();
  toupdate = "{";
  n = table.rows().data().length;
  for (i = 0; i < n; i++) { 
      toupdate += '"' + table.row(i).data().id + '":' + table.row(i).data().order;
      if (i != n-1) {
          toupdate += ", ";
      }
  }
  toupdate
  toupdate += "}"
  $.ajax({
      method: "POST",
      url: url,
      data: { toupdate: toupdate }
  })
  .done(function( msg ) {
      $('#data-table').DataTable().ajax.reload();
      toastr.success(msg);

  }).error(function() {
      toastr.error("Error, please contact the system administrator");
  });
}
