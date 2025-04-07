$(document).ready(function () {
    $(".navbar-brand img").hover(
        function () {
            const hoverImg = $(this).data("logo-hover");
            $(this).attr("src", hoverImg);
        },
        function () {
            const defaultImg = $(this).data("logo-default");
            $(this).attr("src", defaultImg);
        }
    );
});
