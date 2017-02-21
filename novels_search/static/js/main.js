/**
 * Created by howie on 17/02/2017.
 */

$(function () {
    $('[data-toggle="popover"]').popover()
});


$(document).ready(function () {
    var content_url = $("#content_url").val();
    $("a").each(function () {
        var url = $(this).attr('href');
        if (typeof(url) != "undefined") {
            if (url.indexOf("owllook") < 0) {
                var name = $(this).text();
                var show_url = "owllook_content?url=" + content_url + url + "&name=" + name;
                console.log(show_url);
                $(this).attr('href', show_url);
                $(this).attr('target', '_blank');
            }
        }
    });
});