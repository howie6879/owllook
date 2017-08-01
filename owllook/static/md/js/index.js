/**
 * Created by howie on 29/07/2017.
 */
var inst_drawer = new mdui.Drawer('#drawer');
var inst_panel = new mdui.Panel('#panel');
document.getElementById('toggle').addEventListener('click', function () {
    inst_drawer.toggle();
});

document.getElementById('email-close').addEventListener('click', function () {
    inst_panel.close('#item-email');
});
document.getElementById('pass-close').addEventListener('click', function () {
    inst_panel.close('#item-pass');
});

$(".passSubmitBtn").click(function () {
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
    }

});

$(".emailSubmitBtn").click(function () {
    var email = $("[name='email']").val();
    var email_reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var str_email = email_reg.test(email);
    $(".email-error").css("visibility", "hidden");
    if (str_email) {
        alert(email)
    } else {
        $(".email-error").text("邮箱格式错误");
        $(".email-error").css("visibility", "visible");
    }
});