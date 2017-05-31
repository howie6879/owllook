/**
 * Created by howie on 21/02/2017.
 */
$(document).ready(function () {
    var content_url = $("#content_url").val();
    var chapter_url = $("#url").val();
    var novels_name = $("#novels_name").val();
    $(".container a").each(function () {
        var url = $(this).attr('href');
        if (typeof(url) != "undefined") {
            if (url.indexOf("owllook") < 0) {
                var name = $(this).text();
                // 当content_url为1，表示该链接不用拼接
                if (content_url == '1') {
                    content_url = ''
                } else if (content_url == '0') {
                    // content_url=0表示章节网页需要当前url拼接
                    content_url = chapter_url;
                } else if (content_url == '-1') {
                    // content_url=-1 表示特殊情况
                    content_url = chapter_url;
                }
                show_url = "owllook_content?url=" + content_url + url + "&name=" + name + "&chapter_url=" + chapter_url + "&novels_name=" + novels_name;
                $(this).attr('href', show_url);
                $(this).attr('target', '_blank');
            }
        }
    });
});