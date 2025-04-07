/* Script that applies Darkmode to the website */

$(document).ready(function(){
    // Check if dark mode is enabled from localStorage and apply it
    if(localStorage.getItem("darkMode") === "enabled") {
        $("body").addClass("dark-background");
        $("p, h1, h2, h3, h4, h5, h6").addClass("light-text");
        $("#navbar").addClass("navbar-dark bg-dark").removeClass("navbar-light bg-light");
        $("#welcome").addClass("welcome-box-dark").removeClass("welcome-box");
        $("#footer").addClass("footer-dark");
        $("#darkModeToggle").text("Light");
        $("hr").addClass("seperator"); // Add .separator to all <hr> elements
        $(".contact-form label").css("color", "white");
        $(".contact-form textarea, .contact-form input, .contact-form select").css({
            "background-color": "#333840", // Dark gray background
            "color": "white" // White text color
        });
        $(".contact-form select option").css("color", "white"); // White text in select options
        $(".taskfields label").css("color", "white");
        $(".taskfields input, .taskfields select").css({
            "background-color": "#333840", // Dark gray background
            "color": "white" // White text color
        });
        $(".taskfields select option").css("color", "white"); // White text in select options
    }

    // Handle button click for dark mode toggle
    $("#darkModeToggle").click(function(){
        // Toggle classes for dark mode
        $("#navbar").toggleClass("navbar-light navbar-dark bg-light bg-dark");

        // Toggle background color of the page
        $("body").toggleClass("dark-background");

        // Toggle text color for paragraphs and headers
        $("p, h1, h2, h3, h4, h5, h6").toggleClass("light-text");

        // Toggle welcome-box classes for the #welcome div
        $("#welcome").toggleClass("welcome-box-dark welcome-box");

        // Toggle footer-dark class on footer
        $("#footer").toggleClass("footer-dark");

        // Toggle .separator class on all <hr> elements
        $("hr").toggleClass("separator");

        // CToggle Dark Mode for the Contact Form Labels
        // Check the color of the first label
        var currentColor = $(".contact-form label").first().css("color");
        // If the color is rgb(33, 37, 41), change it to white, otherwise change to rgb(33, 37, 41)
        if (currentColor === "rgb(33, 37, 41)") {
            $(".contact-form label").css("color", "white");
        } else if (currentColor === "rgb(255, 255, 255)") {
            $(".contact-form label").css("color", "rgb(33, 37, 41)");
        }

        // Toggle Dark Mode for the contact form fields
        var currentfieldColor = $(".contact-form input").first().css("background-color");
        if (currentfieldColor === "rgb(255, 255, 255)") { 
            $(".contact-form textarea, .contact-form input, .contact-form select").css({
                "background-color": "#333840", // Dark gray background
                "color": "white" // White text color
            });
            $(".contact-form select option").css("color", "white"); // White text in select options
        } else {
            $(".contact-form textarea, .contact-form input, .contact-form select").css({
                "background-color": "white", // Light background
                "color": "rgb(33, 37, 41)" // Dark text color
            });
            $(".contact-form select option").css("color", "rgb(33, 37, 41)"); // Dark text in select options
        }

        // CToggle Dark Mode for the Contact Form Labels
        // Check the color of the first label
        var taskfieldColor = $(".taskfields label").first().css("color");
        // If the color is rgb(33, 37, 41), change it to white, otherwise change to rgb(33, 37, 41)
        if (taskfieldColor === "rgb(33, 37, 41)") {
            $(".taskfields label").css("color", "white");
        } else if (taskfieldColor === "rgb(255, 255, 255)") {
            $(".taskfields label").css("color", "rgb(33, 37, 41)");
        }

        // Toggle Dark Mode for the contact form fields
        var currentfieldtaskColor = $(".taskfields input").first().css("background-color");
        if (currentfieldtaskColor === "rgb(255, 255, 255)") { 
            $(".taskfields input, .taskfields select").css({
                "background-color": "#333840", // Dark gray background
                "color": "white" // White text color
            });
            $(".taskfields select option").css("color", "white"); // White text in select options
        } else {
            $(".taskfields input, .taskfields select").css({
                "background-color": "white", // Light background
                "color": "rgb(33, 37, 41)" // Dark text color
            });
            $(".taskfields select option").css("color", "rgb(33, 37, 41)"); // Dark text in select options
        }

        // Change the button text between "Dark" and "Light"
        var buttonText = $("#darkModeToggle").text().trim();
        if (buttonText === "Dark") {
            $("#darkModeToggle").text("Light");
            localStorage.setItem("darkMode", "enabled"); // Save dark mode state
        } else {
            $("#darkModeToggle").text("Dark");
            localStorage.setItem("darkMode", "disabled"); // Save dark mode state
        }
    });
});