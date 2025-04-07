/* Script that makes images of 'about' page black and white when mouse hovers over them */

$(document).ready(function () {
    $(".panos-img img").hover(
        function () {
            $(this).attr("src", "/static/images/Our_Team/PanosBNW.jpg");
        },
        function () {
            $(this).attr("src", "/static/images/Our_Team/Panos.jpg");
        }
    );

    $(".andreas-img img").hover(
        function () {
            $(this).attr("src", "/static/images/Our_Team/AndreasBNW.jpg");
        },
        function () {
            $(this).attr("src", "/static/images/Our_Team/Andreas.jpg");
        }
    );

    $(".pandelis-img img").hover(
        function () {
            $(this).attr("src", "/static/images/Our_Team/PandelisBNW.jpg");
        },
        function () {
            $(this).attr("src", "/static/images/Our_Team/Pandelis.jpg");
        }
    );

    $(".nikolas-img img").hover(
        function () {
            $(this).attr("src", "/static/images/Our_Team/NikolasBNW.jpg");
        },
        function () {
            $(this).attr("src", "/static/images/Our_Team/Nikolas.jpg");
        }
    );
});
