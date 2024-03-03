// static/js/scripts.js
/*!
* Start Bootstrap - Agency v7.0.6 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Custom code for contact form submission
    var contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", function(e) {
            // Prevent the form from submitting
            e.preventDefault();

            // Log the values
            console.log("Name:", document.getElementById('name').value);
            console.log("Email:", document.getElementById('email').value);
            console.log("Phone:", document.getElementById('phone').value);
            console.log("Phone:", document.getElementById('message').value);

            // Proceed with the form submission if needed
            this.submit(); // Uncomment this line to allow the form to submit after logging
        });
    }

    // Custom code for AJAX contact form submission
var contactForm = document.getElementById("contactForm");
if (contactForm) {
    contactForm.addEventListener("submit", function(e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // FormData object to hold the form data
        var formData = new FormData(this);

        // Fetch API to submit form data via AJAX
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Necessary for Django to recognize it as an AJAX request
                // 'X-CSRFToken': csrfToken, // Add CSRF token here if not using FormData for CSRF
            },
        })
        .then(response => response.json()) // Assuming the server responds with JSON
        .then(data => {
            // Handle the response data
            console.log(data.message); // Log the success message
            // Optionally, display the message to the user in the UI
            const formResponse = document.getElementById('formResponse');
            if (formResponse) {
                formResponse.innerText = data.message;
                formResponse.classList.remove('d-none'); // Make sure to show the message if it was hidden
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Optionally, inform the user that an error occurred
            const formResponse = document.getElementById('formResponse');
            if (formResponse) {
                formResponse.innerText = 'An error occurred. Please try again.';
                formResponse.classList.remove('d-none'); // Show the message if it was hidden
            }
        });

        // Prevent form from submitting normally
        return false;
    });
}


});
