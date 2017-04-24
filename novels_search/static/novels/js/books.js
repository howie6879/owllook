/**
 * Created by howie on 24/04/2017.
 */

$(document).ready(function () {
    $(".del-book").click(function () {
        var msg = "您真的确定要删除吗？请确认！";
        if (confirm(msg)) {
            var book_url = $(this).find('a.book_url').attr("data-value");
            var del_pd = {"book_url": book_url};
            var del_object = $(this).parent();
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/delete_book",
                data: del_pd,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        del_object.remove();
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        }
    });
});