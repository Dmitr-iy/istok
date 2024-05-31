$(document).ready(function() {
    var modal = $('#loginModal');
    var loginFormContainer = $('#loginFormContainer');
    var registerFormContainer = $('#registerFormContainer');
    var registerPrompt = $('#registerPrompt');

    $('#openLoginModalBtn').click(function() {
        loginFormContainer.show();
        registerFormContainer.hide();
        registerPrompt.show();
        modal.show();
    });

    $('.close').click(function() {
        modal.hide();
    });

    $('#showRegisterForm').click(function() {
        loginFormContainer.hide();
        registerFormContainer.show();
        registerPrompt.hide();
    });

    $(window).click(function(event) {
        if ($(event.target).is(modal)) {
            modal.hide();
        }
    });
});
