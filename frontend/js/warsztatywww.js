window.tinymce_local_file_picker = function(cb, value, meta) {
    // https://www.tiny.cloud/docs/demo/file-picker/
    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.onchange = function () {
        var file = this.files[0];

        var reader = new FileReader();
        reader.onload = function () {
            var id = 'blobid' + (new Date()).getTime();
            var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
            var base64 = reader.result.split(',')[1];
            var blobInfo = blobCache.create(id, file, base64);
            blobCache.add(blobInfo);

            cb(blobInfo.blobUri(), { title: file.name });
        };
        reader.readAsDataURL(file);
    };
    input.click();
}

function send_points(elem, save_btn, workshop_participant_id) {
    var field_name = elem.attr('name');
    var saved_value = elem.val();
    var qualified_mark = elem.parents('tr').find('.qualified-mark');

    var mark_changed = function () {
        save_btn.attr('disabled', false);
        save_btn.find('.glyphicon').removeClass('glyphicon-floppy-open glyphicon-floppy-saved').addClass('glyphicon-floppy-disk');
    };

    var mark_saving = function () {
        save_btn.attr('disabled', true);
        save_btn.find('.glyphicon').removeClass('glyphicon-floppy-disk glyphicon-floppy-saved').addClass('glyphicon-floppy-open');
    };

    var mark_saved = function () {
        save_btn.attr('disabled', true);
        save_btn.find('.glyphicon').removeClass('glyphicon-floppy-disk glyphicon-floppy-open').addClass('glyphicon-floppy-saved');
    };

    mark_saved();
    save_btn.click(function() {
        var data = {'id': workshop_participant_id};
        data[field_name] = elem.val();
        mark_saving();
        $.ajax({
            'url': '/savePoints/',
            'data': data,
            'error': function(xhr, textStatus, errorThrown) {
                mark_changed();
                alert('Błąd: ' + errorThrown);
            },
            'method': 'POST',
            'success': function(value) {
                if(value.error) {
                    mark_changed();
                    alert('Błąd:\n' + value.error);
                } else {
                    saved_value = value[field_name];
                    elem.val(""); // For whatever reason, this is required to get the field to reformat with the correct comma. Don't ask.
                    elem.val(saved_value);
                    mark_saved();
                    qualified_mark.html(value.mark);
                }
            }
        });
    });

    elem.on('change keyup mouseup', function() {
        if(elem.val() != saved_value)
            mark_changed();
    });
}

$('button[data-save]').each(function() {
    var save_btn = $(this);
    var elem = $(save_btn.data('save'));
    var workshop_participant_id = save_btn.data('participantId');
    send_points(elem, save_btn, workshop_participant_id);
});

window.handle_registration_change = function(workshop_name_txt, register) {
    var proper_url;
    if(register) {
        proper_url = $("#" + workshop_name_txt).data('register');
    } else {
        proper_url = $("#" + workshop_name_txt).data('unregister');
    }

    function error(message) {
        var elem = $('<div class="alert alert-danger fade in"><a href="#" class="close" data-dismiss="alert">&times;</a>' +
                     '<strong>Error!</strong> <span></span></div>');
        elem.find('span').text(message);
        $("#" + workshop_name_txt).after(elem); // add the error to the dom
    }

    $.ajax({
        url : proper_url, // the endpoint
        type : "POST", // http method

        // handle a successful response
        success : function(json) {
            if (json.error) {
                error(json.error);
            }
            if (json.redirect) {
                window.location.href = json.redirect;
            }
            if (json.content) {
                $("#" + workshop_name_txt).find(".button-div").replaceWith(json.content);
            }
        },
        error: function(xhr, errmsg, errcode) {
            error('Wystąpił problem przy wysyłaniu danych (' + xhr.status + ': ' + errcode + ').');
        }
    });
}

$(function () {
    $('[data-toggle="popover"]').popover();

    // Automatically hide 'Saved successfully' alerts after 4 seconds
    $(".alert-auto-dismiss").delay(4000).fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });

    $('.dateinput').each(function (i, x) {
        var dates = [];
        for(var date = moment($(x).data('start-date')); date <= moment($(x).data('end-date')); date.add(1, 'days'))
            dates.push(date.toDate());
        $(x).datetimepicker({
            format: 'L',
            locale: 'pl',
            defaultDate: $(x).data('default-date'),
            enabledDates: dates,
        });
    });

    // Facebook fix your sh*t (╯°□°)╯︵ ┻━┻
    function fixBrokenUnresponsiveFacebook() {
        $('iframe').each(function() {
            var url = $(this).attr('src');
            if (url.indexOf('facebook.com/plugins/page.php') === -1)
                return;
            if($(this).width() == 0 || $(this).height() == 0)
                return;
            url = url.replace(/width=([0-9]+)/, 'width=' + $(this).width());
            url = url.replace(/height=([0-9]+)/, 'height=' + $(this).height());
            if ($(this).attr('src') != url)
                $(this).attr('src', url);
        });
    }
    fixBrokenUnresponsiveFacebook();
    $(window).resize(fixBrokenUnresponsiveFacebook);
});