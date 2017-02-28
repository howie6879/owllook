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
    // bookmark
    $('#bookMark').click(function () {
        if ($(this).hasClass('bookMark')) {
            $(this).removeClass('bookMark');
            $(this).addClass('bookMarkAct');
        } else {
            $(this).removeClass('bookMarkAct');
            $(this).addClass('bookMark');
        }
    });
});