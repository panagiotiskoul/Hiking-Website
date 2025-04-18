$(document).ready(function () {
    var $slider = $('#id_rating');
    var $output = $('#ratingValue');

    function updateRatingValue(rating) {
        $output.text(rating);

        // Remove all possible color classes
        $output.removeClass('text-danger text-warning text-success');

        // Add the correct one
        if (rating <= 2) {
            $output.addClass('text-danger');
        } else if (rating == 3) {
            $output.addClass('text-warning');
        } else {
            $output.addClass('text-success');
        }
    }

    if ($slider.length && $output.length) {
        updateRatingValue($slider.val());

        $slider.on('input change', function () {
            updateRatingValue($(this).val());
        });
    }
});