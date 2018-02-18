/**
 * Created by howie on 14/03/2017.
 */
$(function () {
    $(".submitBtn").click(function () {
        var nickname = $("[name='nickname']").val();
        var email = $("[name='email']").val();
        var answer = $("[name='answer']").val();
        var password = $("[name='password']").val();
        var email_reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
        var str_email = email_reg.test(email);
        $("#errorInfo0").addClass("errorHidden0");
        $("#errorInfo1").addClass("errorHidden1");
        $("#errorInfo2").addClass("errorHidden2");
        $("#errorInfo3").addClass("errorHidden3");
        if (str_email) {
            if (password == "" || password != $("[name='password2']").val()) {
                $(".errorInfo").removeClass("errorHidden1");
            }
            else if (password.length < 6 || nickname.length <= 2) {
                $(".errorInfo").removeClass("errorHidden0");
            }
            else if (nickname == "" || email == "" || answer == "") {
                $(".errorInfo").removeClass("errorHidden2");
            }
            else {
                register_pd = {
                    'user': nickname,
                    'pwd': password,
                    'email': email,
                    'answer': answer
                };
                $.ajax({
                    type: "post",
                    contentType: "application/json",
                    url: "/operate/register",
                    data: register_pd,
                    dataType: 'json',
                    success: function (data) {
                        if (data.status == 1) {
                            window.location.href = '/';
                        }
                        if (data.status == -1) {
                            alert('用户名已存在 换个更好的名字吧');
                        }
                        if (data.status == -2) {
                            alert('回答错了^_^');
                        }
                        if (data.status == 0) {
                            alert('注册失败');
                        }
                    }
                });
            }
        } else {
            $(".errorInfo").removeClass("errorHidden3");
        }
    });
});