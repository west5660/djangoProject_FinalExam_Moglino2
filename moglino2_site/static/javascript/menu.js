document.addEventListener('DOMContentLoaded', function () {
    var mobileMenuIcon = document.querySelector('.mobile-menu-icon');
    var desktopMenu = document.querySelector('.desktop-menu');

    mobileMenuIcon.addEventListener('click', function () {
        desktopMenu.classList.toggle('show');
    });

    // Закрываем меню при клике за его пределами на мобильных устройствах
    document.addEventListener('click', function (event) {
        if (!desktopMenu.contains(event.target) && event.target !== mobileMenuIcon) {
            desktopMenu.classList.remove('show');
        }
    });
});
