$(function () {
    var body = $('body');

    $("div[data-type='widget']").each(function () {
        var widgetElement = $(this);
        var url = $(widgetElement).data('url');

        ajax(url, {
            done: function (result) {
                $(widgetElement).replaceWith(result);
            }
        });
    });

    $(body).on('click', 'a[data-type=widget-refresh]', function (e) {
        var widgetElement = $(this).parents('div[data-type=widget]');
        var url = $(widgetElement).data('url');

        $(widgetElement).fadeTo(100, 0.4);

        ajax(url, {
            done: function (result) {
                $(widgetElement).replaceWith(result);
            }, fail: function () {
                $(widgetElement).fadeTo(100, 1);
            }
        });

        e.preventDefault();
    });

    $(body).on('click', 'a[data-type=widget-action]', function (e) {
        var widgetElement = $(this).parents('div[data-type=widget]');
        var url = $(widgetElement).data('url');
        var data = $(this).data();

        $(widgetElement).fadeTo(100, 0.4);

        ajax(url, {
            done: function (result) {
                $(widgetElement).replaceWith(result);
            }, fail: function () {
                $(widgetElement).fadeTo(100, 1);
            }, data: data
        });

        e.preventDefault();
    });

    $(body).on('submit', 'form[data-type=widget-form]', function (e) {
        var widgetElement = $(this).parents('div[data-type=widget]');
        var url = $(widgetElement).data('url');
        var f = $(this);

        $(widgetElement).fadeTo(100, 0.4);

        ajaxForm(f, e, {
            url: url, done: function (result) {
                $(widgetElement).replaceWith(result);
            }, fail: function () {
                $(widgetElement).fadeTo(100, 1);
            }
        });
    });
});

