/**
 * Created by howie on 29/07/2017.
 */
var inst_panel = new mdui.Panel('#panel');

document.getElementById('email-close').addEventListener('click', function () {
    inst_panel.close('#item-email');
});
document.getElementById('pass-close').addEventListener('click', function () {
    inst_panel.close('#item-pass');
});

$("#passSubmitBtn").click(function () {
    var old_pass = $("[name='old_pass']").val();
    var new_pass = $("[name='new_pass']").val();
    var new_pass1 = $("[name='new_pass1']").val();
    $(".pass-error").css("visibility", "hidden");
    if (old_pass == "" || new_pass == "" || new_pass1 == "") {
        $(".pass-error").text("密码不能为空");
        $(".pass-error").css("visibility", "visible");
    } else if (new_pass != new_pass1) {
        $(".pass-error").text("两次密码输入不一致");
        $(".pass-error").css("visibility", "visible");
    } else if (new_pass.length < 6) {
        $(".pass-error").text("密码不能小于6位数");
        $(".pass-error").css("visibility", "visible");
    } else {
        var pass_pd = {"new_pass": new_pass, "old_pass": old_pass};
        $.ajax({
            type: "post",
            contentType: "application/json",
            url: "/operate/change_pass",
            data: pass_pd,
            dataType: 'json',
            success: function (data) {
                if (data.status == 1) {
                    mdui.snackbar({
                        message: '密码修改成功',
                        timeout: 3000
                    });
                    inst_panel.close('#item-pass');
                }
                if (data.status == -2) {
                    $(".pass-error").text("原始密码错误");
                    $(".pass-error").css("visibility", "visible");
                }
                if (data.status == -1) {
                    alert('您还没有登录');
                }
            }
        });
    }

});

$("#emailSubmitBtn").click(function () {
    var email = $("[name='email']").val();
    var email_reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var str_email = email_reg.test(email);
    $(".email-error").css("visibility", "hidden");
    if (str_email) {
        var email_pd = {"email": email};
        $.ajax({
            type: "post",
            contentType: "application/json",
            url: "/operate/change_email",
            data: email_pd,
            dataType: 'json',
            success: function (data) {
                if (data.status == 1) {
                    inst_panel.close('#item-email');
                    mdui.snackbar({
                        message: '邮箱修改成功',
                        timeout: 3000
                    });
                    $("#owl-email").html(email);
                    //location.reload();
                }
                if (data.status == -1) {
                    alert('您还没有登录');
                }
            }
        });
    } else {
        $(".email-error").text("邮箱格式错误");
        $(".email-error").css("visibility", "visible");
    }
});