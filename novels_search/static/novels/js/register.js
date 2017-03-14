/**
 * Created by howie on 14/03/2017.
 */
$(function () {
    $(".submitBtn").click(function () {
        alert("暂时不支持注册，可在反馈出申请账号内侧。有书架奖励哟！");
        if ($("[name='password']").val() != $("[name='password2']").val()) {
            $(".errorInfo").removeClass("errorHidden");
        } else {
            //$("#register").submit();
        }
    });
});