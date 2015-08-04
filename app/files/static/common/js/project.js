function initializeElements() {
    $("[data-type=dateandtimepicker]").datetimepicker({
        format: "DD/MM/YYYY HH:mm", showClose: true
    });
}
function initializeAjax() {
    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
            }
            console.log("beforeSend");
        }, complete: function (jqXHR, textStatus) {
            console.log("complete");
            initializeElements();
        }
    });
}
function getDoc(frame) {
    var doc = null;

    // IE8 cascading access check
    try {
        if (frame.contentWindow) {
            doc = frame.contentWindow.document;
        }
    } catch (err) {
    }

    if (doc) { // successful getting content
        return doc;
    }

    try { // simply checking may throw in ie8 under ssl or mismatched protocol
        doc = frame.contentDocument ? frame.contentDocument : frame.document;
    } catch (err) {
        // last attempt
        doc = frame.document;
    }
    return doc;
}
window.showProcessing = function () {
    $("#ajax-processing-container").show();
};
window.hideProcessing = function () {
    $("#ajax-processing-container").hide();
};
window.ajax = function (url, i) {
    /*
     Possible attributes of 'i':
     type        type of request, 'GET' or 'POST'
     data        ajax data object
     done        function
     fail        function
     always      function
     */
    showProcessing();

    var requestType = i && i.type ? i.type : 'GET';

    var params = {
        url: url, type: requestType
    };
    if (i && i.data) {
        params['data'] = i.data;
    }
    $.ajax(params).done(function (result, textStatus, jqXHR) {
        if (i && i.done) {
            i.done(result, textStatus, jqXHR)
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("Start of error variables:");
        console.log(jqXHR, textStatus, errorThrown);
        console.log("End of error variables.");
        alert("Unexpected error occurred. Please see console for details.");
        if (i && i.fail) {
            i.fail(jqXHR, textStatus, errorThrown);
        }
    }).always(function () {
        if (i && i.always) {
            i.always();
        }
        hideProcessing();
    });
};
window.ajaxForm = function (f, e, i) {
    /*
     Possible attributes of 'i':
     url        url to use instead of form's action
     done       function
     fail       function
     always     function
     */
    showProcessing();

    var formObj = $(f);
    var formURL = i && i.url ? i.url : formObj.attr("action");

    if (window.FormData !== undefined)  // for HTML5 browsers
    {
        //var formData = new FormData(f);
        var formData = $(f).serialize();
        $.ajax({
            url: formURL, type: "POST", data: formData, //mimeType: "multipart/form-data",
            //contentType: false,
            //cache: false,
            //processData: false,
            success: function (data, textStatus, jqXHR) {
                if (i && i.done) {
                    i.done(data, textStatus, jqXHR);
                }
            }, error: function (jqXHR, textStatus, errorThrown) {
                console.log("Start of error variables:");
                console.log(jqXHR, textStatus, errorThrown);
                console.log("End of error variables.");
                alert("Unexpected error occurred. Please see console for details.");
                if (i && i.fail) {
                    i.fail(jqXHR, textStatus, errorThrown);
                }
            }, complete: function (jqXHR, textStatus) {
                hideProcessing();
                if (i && i.always) {
                    i.always();
                }
            }
        });
        e.preventDefault();
        //e.unbind();
    } else  // for olden browsers
    {
        // generate a random id
        var iframeId = 'unique' + (new Date().getTime());

        // create an empty iframe
        var iframe = $('<iframe src="javascript:false;" name="' + iframeId + '" />');

        // hide it
        iframe.hide();

        // set form target to iframe
        formObj.attr('target', iframeId);

        // add iframe to body
        iframe.appendTo('body');
        iframe.load(function (e) {
            hideProcessing();
            var doc = getDoc(iframe[0]);
            var docRoot = doc.body ? doc.body : doc.documentElement;
            var data = docRoot.innerHTML;
            //data is returned from server.
        });
    }
};

$(function () {
    if (!$("#ajax-processing-container").length) {
        var ajaxProcessingContainerHtml = "<div id='ajax-processing-container'>...</div>";
        $('body').append(ajaxProcessingContainerHtml);
    }

    initializeElements();
    initializeAjax();
});

var bodyElement = $('body');

// AJAX Action

$(bodyElement).on('click', 'a[data-type=ajax-action]', function (e) {
    var url = $(this).data('url');
    var data = $(this).data();

    ajax(url, {
        data: data, done: function (result) {
            if (result.is_successful) {
                alert("Done!");
            } else {
                alert(result.message);
            }
        }
    });

    e.preventDefault();
});

// AJAX Form

$(bodyElement).on('submit', 'form[data-type=ajax-form]', function (e) {
    ajaxForm(this, e)
});

