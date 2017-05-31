/**
 * Created by howie on 24/04/2017.
 */

$(document).ready(function () {
    $(".del-bookmark").click(function () {
        var msg = "您真的确定要删除吗？请确认！";
        if (confirm(msg)) {
            var bookmarkurl = $(this).find('a.bookmark_url').attr("data-value");
            var del_bm_pd = {"bookmarkurl": bookmarkurl};
            var del_bm_object = $(this).parent();
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/delete_bookmark",
                data: del_bm_pd,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        del_bm_object.remove();
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        }
    });
});