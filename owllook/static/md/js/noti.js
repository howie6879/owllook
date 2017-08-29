/**
 * Created by howie on 12/08/2017.
 */

var inst_panel = new mdui.Panel('#panel');


$("#authorBtn").click(function () {
    var author_name = $("[name='author_name']").val();
    var author_pd = {"author_name": author_name};
    if (author_name == "") {
        mdui.snackbar({
            message: '请输入作者名',
            timeout: 3000
        });
    } else {
        $.ajax({
            type: "post",
            contentType: "application/json",
            url: "/operate/author_notification",
            data: author_pd,
            dataType: 'json',
            success: function (data) {
                if (data.status == 1) {
                    mdui.snackbar({
                        message: '添加作者成功',
                        onClose: function () {
                            location.reload();
                        }
                    });
                }
                if (data.status == -1) {
                    alert('您还没有登录');
                }
                if (data.status == 2) {
                    mdui.snackbar({
                        message: '暂无该作者',
                        timeout: 2000
                    });
                }
                if (data.status == 3) {
                    mdui.snackbar({
                        message: '作者已添加',
                        timeout: 2000
                    });
                }
                if (data.status == 4) {
                    mdui.snackbar({
                        message: '只能添加五位作者',
                        timeout: 2000
                    });
                }
                if (data.status == 0) {
                    mdui.snackbar({
                        message: '操作失败',
                        timeout: 1000
                    });
                }
            }
        });
    }
});