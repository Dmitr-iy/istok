$(document).ready(function() {
    var modal = $('#loginModal');
    var loginFormContainer = $('#loginFormContainer');
    var registerFormContainer = $('#registerFormContainer');

    $('#openLoginModalBtn').click(function() {
        loginFormContainer.show();
        registerFormContainer.hide();
        modal.removeClass('register-open');
        modal.show();
    });

    $('.close').click(function() {
        modal.hide();
    });
    $('.close-login').click(function() {
        modal.hide();
    });

    $('#showRegisterForm').click(function() {
        loginFormContainer.hide();
        registerFormContainer.show();
        modal.addClass('register-open');
    });

    $('#showRegisterFormFromLogin').click(function() {
        loginFormContainer.hide();
        registerFormContainer.show();
        modal.addClass('register-open');
    });

    $(window).click(function(event) {
        if ($(event.target).is(modal)) {
            modal.hide();
        }
    });

    $('#registerForm').submit(function(event) {
        event.preventDefault(); // предотвращение стандартного поведения формы
        var form = $(this);
        var url = form.attr('action');
        var data = form.serialize();

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function(response) {
                // Очищаем старые ошибки
                form.find('.error').html('');
                if (response.success) {
                    // Закрываем модальное окно и показываем сообщение об успешной регистрации или редиректим
                    modal.hide();
                    alert('Регистрация прошла успешно!');
                } else {
                    // Показ ошибок
                    for (var field in response.errors) {
                        $('#error_' + field).html(response.errors[field].join('<br>'));
                    }
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });

    $('#loginForm').submit(function(event) {
        event.preventDefault(); // предотвращение стандартного поведения формы
        var form = $(this);
        var url = form.attr('action');
        var data = form.serialize();

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function(response) {
                // Очищаем старые ошибки
                form.find('.error').html('');
                if (response.success) {
                    // Перенаправляем на главную страницу
                    window.location.href = response.redirect_url;
                } else {
                    // Показ ошибок
                    if (response.errors) {
                        $('#error_non_field_errors').html('Введены неверные данные');
                    }
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
});
