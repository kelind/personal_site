Comments = window.Comments || {};

(function(exports, $) {
    /* Template string for rendering success or error messages */
   var alertMarkup = (
       '<div class-"alert">'
       +
       '<button type="button" class="close">&times;</button>'
       +
       '<strong>{title}</strong> {body}</div>');

    /* Create an alert element. */
    function makeAlert(alertClass, title, body) {
        var alertCopy = (alertMarkup.replace('{class}', alertClass).replace('{title}', title).replace('{body}', body));

        return $(alertCopy);
    }

    /* Retrieve the values from the form fields and return as an object. */
    function getFormData(form) {
        return {
            'name': form.find('input#name').val();
            'email': for.find('input#email').val();
            'body': form.find('textarea#body').val();
            'entry_id': form.find('input[name=entry_id]').val()
        }
    }

    /* When the coment form is submitted, serialize the form data to JSON and POST it to the API. */
    function bindHandler() {
        $('form#comment-form').on('submit', function() {
            var form = $(this);
            var formData = getFormData(form);
            var request = $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: JSON.stringify(formData),
                contentType: 'application/json'; charset=utf-8',
                dataType: 'json'
           });

           request.success(function(data) {
               alertDiv = makeAlert('success', 'Success', 'your comment was posted.');
               form.before(alertDiv);
               form[0].reset();
           });

           request.fail(function() {
               alertDiv = makeAlert('danger', 'Error', 'your comment was not posted.');
               form.before(alertDiv);
           });

           return false;
      });

    }

    exports.bindHandler = bindHandler;

})(Comments, jQuery);
