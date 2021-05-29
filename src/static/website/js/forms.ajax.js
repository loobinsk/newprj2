String.prototype.hashCode = function(){
    var hash = 0;
    for (var i = 0; i < this.length; i++) {
        hash += this.charCodeAt(i);
    }
    return hash;
};

$(document).ready(function() {

$('form.ajax').submit(function (e) {

    e.preventDefault();

    // hash
    var hash_key = $(this).attr('data-hash');
    if (hash_key) {
        var value = $(this).find('input[name="'+ hash_key +'"]').val();
        if (value) $(this).find('input[name="secret_key"]').val(value.hashCode());
    }

    // Init
    var form = $(this);
    var formData = new FormData(this);
    var no_clear = form.is('[data-no-clear]');

    remove_errors(form);
    form.find('.success-text').hide();
    form.find('.error-text').hide();

    // Do ajax

    $.ajax({
        type: "POST",
        url: form.attr('action'),
        data: formData,
        dataType: "json",
        cache: false,
        contentType: false,
        async: false,
        processData: false
    }).done(function(data) {

        form.find('.success').show();
        if (!no_clear) {
            form.find("input[type=text], input[type=file], input[type=email], input[type=password], textarea").val("");
            form.find("input[type=checkbox]").removeAttr('checked');
            form.find("select").val($(this)[0].initialValue);
        }

        // Redirect
        try {
            var url = data.url;
            if (url) window.location.href = url;
            if (form.attr('data-url')) {
                window.location.href = form.attr('data-url');
            }
        } catch (e) {

        }

    }).fail(function(data) {
        $.each(data.responseJSON, function (key, v) {
            var input_o = form.find('[name="'+ key +'"]');
            input_o.addClass('input-error').prev().text(v).show();
            input_o.addClass('input-error').parents('ul').prev().text(v).show();

            //input_o.parents('tr').find('label').addClass('error');
        });

        //All errors
        try {
            var ea = data.responseJSON.__all__;
            if (ea) {
                form.find('.error-text').text(ea);
                form.find('.error-text').show();
            }
        } catch (e) {

        }

        set_error_element();

    });

});


});


function remove_errors(form) {
    form.find('.input-error').each(function() {
        $(this).removeClass('input-error').prev().text('').hide();
        $(this).removeClass('input-error').parents('ul').prev().text('').hide();
    });
}

function set_error_element() {
    // $('.input-error').focus(function () {
    //     $(this).removeClass('input-error').next().text('');
    //     $(this).parents('tr').find('label').removeClass('error');
    // });
}