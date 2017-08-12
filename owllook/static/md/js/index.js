/**
 * Created by howie on 12/08/2017.
 */

var inst_drawer = new mdui.Drawer('#drawer');
document.getElementById('toggle').addEventListener('click', function () {
    inst_drawer.toggle();
});
