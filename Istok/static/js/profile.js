$(document).ready(function() {
    $('.side-url a').click(function(e) {
        e.preventDefault();
        console.log('Clicked link'); // Для отладки
        var target = $(this).data('target');
        var url = $(this).data('url');
        console.log('Target:', target); // Для отладки
        console.log('URL:', url); 
        $('.section').hide();
        $('#' + target).show();

        // Добавляем активный класс к нажатому элементу и удаляем у других
        console.log('Removing active class from all .side-url elements'); // Логирование
        $('.side-url').removeClass('active');
        console.log('Current classes after removal:', $('.side-url').attr('class')); // Логирование
        console.log('Adding active class to the clicked element'); // Логирование
        $(this).closest('.side-url').addClass('active');
        console.log('Active class added to:', $(this).closest('.side-url')); // Логирование
        console.log('Current classes of clicked element:', $(this).closest('.side-url').attr('class')); // Логирование

        if (target === 'order-history-section' || target === 'favorites-section' || target === 'bonus-program-section') {
            loadContent(url, '#' + target);
        }
    });

    function loadContent(url, target) {
        console.log('Loading content from:', url); 
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                console.log('Content loaded:', data); 
                $(target).html(data);
            }
        });
    }
});
