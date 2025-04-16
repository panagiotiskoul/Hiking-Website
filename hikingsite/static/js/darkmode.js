/* Script that applies Darkmode to the website */

$(document).ready(function(){
    // Check if dark mode is enabled from localStorage and apply it
    if(localStorage.getItem("darkMode") === "enabled") {
        $("body").addClass("dark-background");
        $("p, h1, h2, h3, h4, h5, h6, span, th, td, small, li").addClass("light-text");
        $("table").addClass("table-dark");
        $("thead").addClass("thead-dark");
        $(".card").addClass("dark-background-card");
        $("#navbar").addClass("navbar-dark bg-dark").removeClass("navbar-light bg-light");
        $("#welcome").addClass("welcome-box-dark").removeClass("welcome-box");
        $("#footer").addClass("footer-dark");
        $("#darkModeToggle").text("Light");
        $("hr").addClass("seperator-light").removeClass("seperator-dark");
        $(".contact-form label").css("color", "white");
        $(".contact-form textarea, .contact-form input, .contact-form select").css({
            "background-color": "#333840", // Dark gray background
            "color": "white" // White text color
        });
        $(".contact-form select option").css("color", "white"); // White text in select options
        $(".contact-form .text-muted").css("color", "white"); // White text in select options
        $(".taskfields label").css("color", "white");
        $(".taskfields input, .taskfields select").css({
            "background-color": "#333840", // Dark gray background
            "color": "white" // White text color
        });
        $(".taskfields select option").css("color", "white"); // White text in select options
        $(".no-decoration").css("color", "white");
        $(".list-group-item").addClass("bg-dark");

        // Add class to affect placeholder color
        $(".contact-form input, .contact-form textarea, .taskfields input").addClass("dark-placeholder");

        $("span.input-group-text").addClass("dark-field");
        $(".form-control.d-flex.h-auto").addClass("dark-field")
        $(".dropdown-menu").addClass("bg-dark");
        $(".list-group.list-group-flush").addClass("custom-list-group");

        // Set icon to sun and label to "Light"
        $("#darkModeToggle").html('<i class="bi bi-sun"></i> Light');
    }

    // Handle button click for dark mode toggle
    $("#darkModeToggle").click(function(){

        // Toggle classes for dark mode
        $("#navbar").toggleClass("navbar-light navbar-dark bg-light bg-dark");
        $("body").toggleClass("dark-background");
        $(".card").toggleClass("dark-background-card");
        $("p, h1, h2, h3, h4, h5, h6, span, th, td, small, li").toggleClass("light-text");
        $("table").toggleClass("table-dark");
        $("thead").toggleClass("thead-dark");
        $("#welcome").toggleClass("welcome-box-dark welcome-box");
        $("#footer").toggleClass("footer-dark");
        $("hr").toggleClass("seperator-light");
        $(".list-group-item").toggleClass("bg-dark");
        $("span.input-group-text").toggleClass("dark-field");
        $(".form-control.d-flex.h-auto").toggleClass("dark-field");
        $(".dropdown-menu").toggleClass("bg-dark");
        $(".list-group.list-group-flush").toggleClass("custom-list-group");


        // Toggle label colors in contact form
        var currentColor = $(".contact-form label").first().css("color");
        if (currentColor === "rgb(33, 37, 41)") {
            $(".contact-form label").css("color", "white");
        } else if (currentColor === "rgb(255, 255, 255)") {
            $(".contact-form label").css("color", "rgb(33, 37, 41)");
        }

        // Toggle form input background and text color
        var currentfieldColor = $(".contact-form input").first().css("background-color");
        if (currentfieldColor === "rgb(255, 255, 255)") { 
            $(".contact-form textarea, .contact-form input, .contact-form select").css({
                "background-color": "#333840",
                "color": "white"
            });
            $(".contact-form select option").css("color", "white");

            // Add placeholder style class
            $(".contact-form input, .contact-form textarea").addClass("dark-placeholder");

        } else {
            $(".contact-form textarea, .contact-form input, .contact-form select").css({
                "background-color": "white",
                "color": "rgb(33, 37, 41)"
            });
            $(".contact-form select option").css("color", "rgb(33, 37, 41)");

            // Remove placeholder style class
            $(".contact-form input, .contact-form textarea").removeClass("dark-placeholder");
        }

        // Toggle label colors in taskfields
        var taskfieldColor = $(".taskfields label").first().css("color");
        if (taskfieldColor === "rgb(33, 37, 41)") {
            $(".taskfields label").css("color", "white");
        } else if (taskfieldColor === "rgb(255, 255, 255)") {
            $(".taskfields label").css("color", "rgb(33, 37, 41)");
        }

        // Toggle taskfield input styling
        var currentfieldtaskColor = $(".taskfields input").first().css("background-color");
        if (currentfieldtaskColor === "rgb(255, 255, 255)") { 
            $(".taskfields input, .taskfields select").css({
                "background-color": "#333840",
                "color": "white"
            });
            $(".taskfields select option").css("color", "white");

            // 👇 NEW: Add placeholder style class
            $(".taskfields input").addClass("dark-placeholder");

        } else {
            $(".taskfields input, .taskfields select").css({
                "background-color": "white",
                "color": "rgb(33, 37, 41)"
            });
            $(".taskfields select option").css("color", "rgb(33, 37, 41)");

            // 👇 NEW: Remove placeholder style class
            $(".taskfields input").removeClass("dark-placeholder");
        }

        // Toggle help text
        var helpTextColor = $(".contact-form .form-text, .contact-form .text-muted").first().css("color");
        if (helpTextColor === "rgb(33, 37, 41)" || helpTextColor === "rgb(108, 117, 125)") {
            $(".contact-form .form-text, .contact-form .text-muted").css("color", "white");
        } else {
            $(".contact-form .form-text, .contact-form .text-muted").css("color", "rgb(108, 117, 125)");
        }

        // Toggle trip title link color
        var currentColor = $(".no-decoration").first().css("color");
        if (currentColor === "rgb(33, 37, 41)") {
            $(".no-decoration").css("color", "white");
        } else if (currentColor === "rgb(255, 255, 255)") {
            $(".no-decoration").css("color", "rgb(33, 37, 41)");
        }

        // Toggle button text and localStorage value
        var buttonText = $("#darkModeToggle").text().trim();
        if ($("#darkModeToggle").text().trim().includes("Dark")) {
            $("#darkModeToggle").html('<i class="bi bi-sun"></i> Light');
            localStorage.setItem("darkMode", "enabled");
        } else {
            $("#darkModeToggle").html('<i class="bi bi-moon"></i> Dark');
            localStorage.setItem("darkMode", "disabled");
        }
    });
});
