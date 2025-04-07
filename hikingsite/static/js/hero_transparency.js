/* Script that applies a transparency animation effect to the hero section */

$(document).ready(function() {

    // Apply hover effect to elements with the class "welcome-box"
    $(".welcome-box").hover(
        
        // First function: Triggered when the mouse enters the element
        function() {
            // Set the opacity to 1 (fully visible) when hovered
            $(this).css("opacity", "1");
        },
        
        // Second function: Triggered when the mouse leaves the element
        function() {
            // Set the opacity to 0.8 (slightly transparent) when hover ends
            $(this).css("opacity", "0.8");
        }
    );
});