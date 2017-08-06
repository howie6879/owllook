/**
 * Created by howie on 06/08/2017.
 */

// $("#owllook-light").checked(function () {
//     alert('hello')
// });
//
$("#themeBtn").click(function () {
    var val = $('input:radio[name="owl-theme-layout"]:checked').val();
    if (val == null) {
        alert("干啥呢!");
        return false;
    }
    else {
        if (val == 'dark') {
            $("body").addClass("mdui-theme-layout-dark");
        } else {
            $("body").removeClass("mdui-theme-layout-dark");
        }
    }
});

