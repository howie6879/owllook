/**
 * Created by howie on 12/08/2017.
 */

var inst_drawer = new mdui.Drawer('#drawer');
document.getElementById('toggle').addEventListener('click', function () {
    inst_drawer.toggle();
});

var tab = new mdui.Tab('#owl-login-tab');
mdui.JQ('#owl-login').on('open.mdui.dialog', function () {
    tab.handleUpdate();
});

var userStatus = {
    logout: function () {
        $.ajax({
            type: "get",
            contentType: "application/json",
            url: "/operate/logout",
            dataType: 'json',
            success: function (data) {
                if (data.status == 1) {
                    window.location.reload()
                }
            }
        });
    },
    login: function () {
        var owllook_user = $("#owllook_user").val();
        var owllook_pass = $("#owllook_pass").val();
        if (owllook_user == "" || owllook_pass == "") {
            alert('不能有内容为空');
        } else {
            var login_pd = {'user': owllook_user, 'pwd': owllook_pass};
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/login",
                data: login_pd,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        window.location.reload()
                    }
                    if (data.status == -1) {
                        alert('用户名错误');
                    }
                    if (data.status == -2) {
                        alert('密码错误');
                    }
                }
            });
        }
    }
};