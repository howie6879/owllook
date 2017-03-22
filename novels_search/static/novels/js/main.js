/**
 * Created by howie on 17/02/2017.
 */

$(function () {
    $('[data-toggle="popover"]').popover()
});


$(document).ready(function () {
    $('.move_up').click(function () {
        $('html, body').animate({scrollTop: 0}, 'slow');
        return false;
    });
    $('.move_down').click(function () {
        $('html, body, .content').animate({scrollTop: $(document).height()}, 300);
        return false;
    });
    // book
    $('#owllook_book').click(function () {
        var chapter_url = $("#chapter_url").val();
        var novels_name = $("#novels_name").val();
        if ($(this).hasClass('add-color')) {
            // delete book
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/delete_book?novels_name=" + novels_name + "&chapter_url=" + chapter_url,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        $('#owllook_book').removeClass('add-color');
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        } else {
            // add book
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/add_book?novels_name=" + novels_name + "&chapter_url=" + chapter_url,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        $('#owllook_book').addClass('add-color');
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        }
    });

    // bookmark
    $('#bookMark').click(function () {
        bookmarkurl = window.location.pathname + window.location.search;
        if ($(this).hasClass('bookMark')) {
            // add bookmark
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/add_bookmark?bookmarkurl=" + bookmarkurl,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        $('#bookMark').removeClass('bookMark');
                        $('#bookMark').addClass('bookMarkAct');
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        } else {
            // delete bookmark
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/delete_bookmark?bookmarkurl=" + bookmarkurl,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        $('#bookMark').removeClass('bookMarkAct');
                        $('#bookMark').addClass('bookMark');
                    }
                    if (data.status == -1) {
                        alert('您还没有登录');
                    }
                }
            });
        }
    });
    // login
    $("#owllook_login").click(function () {
        var owllook_user = $("#owllook_user").val();
        var owllook_pass = $("#owllook_pass").val();
        if (owllook_user == "" || owllook_pass == "") {
            alert('不能有内容为空');
        } else {
            $.ajax({
                type: "post",
                contentType: "application/json",
                url: "/operate/login?user=" + owllook_user + "&pwd=" + owllook_pass,
                dataType: 'json',
                success: function (data) {
                    if (data.status == 1) {
                        location.reload();
                    }
                }
            });
        }
    });
    // logout
    $("#logout").click(function () {
        $.ajax({
            type: "get",
            contentType: "application/json",
            url: "/operate/logout",
            dataType: 'json',
            success: function (data) {
                if (data.status == 1) {
                    location.reload();
                }
            }
        });
    })
});

// (function (i, s, o, g, r, a, m) {
//     i['GoogleAnalyticsObject'] = r;
//     i[r] = i[r] || function () {
//             (i[r].q = i[r].q || []).push(arguments)
//         }, i[r].l = 1 * new Date();
//     a = s.createElement(o),
//         m = s.getElementsByTagName(o)[0];
//     a.async = 1;
//     a.src = g;
//     m.parentNode.insertBefore(a, m)
// })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
//
// ga('create', 'UA-93675831-1', 'auto');
// ga('send', 'pageview');

