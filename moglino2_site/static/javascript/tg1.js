// document.addEventListener('DOMContentLoaded', function () {
//     const userInfo = document.getElementById('user-info');
//     const username = userInfo.dataset.username;
//     const orderButton = document.getElementById('orderButton');
//     let isCartCleared = false;
//
//     orderButton.addEventListener('click', function (event) {
//         event.preventDefault();
//
//         // Получаем данные о заказах пользователя
//         const ordersElements = document.querySelectorAll('.order');
//         const orders = [];
//
//         ordersElements.forEach(element => {
//             const serviceTitle = element.dataset.serviceTitle;
//             const quantity = parseInt(element.dataset.quantity);
//             const totalCost = parseFloat(element.dataset.totalCost);
//
//             const order = {
//                 service: { title: serviceTitle },
//                 quantity: quantity,
//                 total_cost: totalCost
//             };
//
//             orders.push(order);
//         });
//
//         // Генерируем текст сообщения для Телеграм
//         let messageText = `Новый заказ от пользователя ${username}:\n\n`;
//         for (const order of orders) {
//             messageText += `${order.service.title} (${order.quantity} шт.) - ${order.total_cost} руб.\n`;
//         }
//
//         // Вызываем функцию отправки сообщения в Телеграм
//         sendTelegramMessage(messageText, function () {
//             // Очищаем корзину
//             clearCart();
//
//             /// Редирект на главную страницу
//             window.location.href = '/home';
//         });
//     });
//
//     // Функция для отправки сообщения в Telegram (ваша реализация)
//     function sendTelegramMessage(message, callback) {
//         const botToken = '6148037034:AAGylTPYhWbrZce8J4aCULQF2x7Qns1zv5k';
//         const chatId = '825113753';
//         const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
//
//         const params = {
//             chat_id: chatId,
//             text: message,
//             parse_mode: 'HTML',
//         };
//
//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(params),
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log('Telegram API Response:', data);
//             alert('Ваш заказ оформлен и направлен в УК ОЭЗ Моглино');
//             // Редирект на главную страницу
//             window.location.href = '/home';
//         })
//         .catch(error => {
//             console.error('Error sending message to Telegram:', error);
//             alert('Произошла ошибка при обработки заказа.');
//         });
//     }
//         function clearCart() {
//     fetch('/clear_cart/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrf_token,  // Убедитесь, что у вас есть csrf_token (передайте его из Django шаблона)
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Cart cleared:', data);
//         // Дополнительные действия при успешной отчистке корзины
//         // Например, перенаправление на главную страницу
//         window.location.href = '/home';
//     })
//     .catch(error => {
//         console.error('Error clearing cart:', error);
//         alert('Произошла ошибка при отчистке корзины.');
//     });
// }
//     function clearCartOnServer() {
//     fetch('/clear_cart/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf_token,
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'success') {
//             console.log('Cart cleared on server:', data);
//             // Дополнительные действия при успешной отчистке корзины
//         } else {
//             console.error('Error clearing cart on server:', data.message);
//             // Обработка ошибки при отчистке корзины на сервере
//         }
//     })
//     .catch(error => {
//         console.error('Error clearing cart on server:', error);
//         // Обработка ошибки при отчистке корзины на сервере
//     });
// }
// });
//
//
//
//
// document.addEventListener('DOMContentLoaded', function () {
//         const orderButton = document.getElementById('orderButton');
//         const ordersElements = document.querySelectorAll('.order');
//
//         orderButton.addEventListener('click', function () {
//             // Скрыть кнопку заказа
//             orderButton.style.display = 'none';
//
//             // Скрыть элементы заказов
//             ordersElements.forEach(element => {
//                 element.style.display = 'none';
//                 // Сохраняем информацию о том, что элемент был скрыт в localStorage
//                 localStorage.setItem(`hidden_${element.dataset.serviceTitle}`, 'true');
//             });
//         });
//
//         // Проверяем localStorage на наличие информации о скрытых элементах при загрузке страницы
//         ordersElements.forEach(element => {
//             if (localStorage.getItem(`hidden_${element.dataset.serviceTitle}`) === 'true') {
//                 element.style.display = 'none';
//             }
//         });
//
//         // Добавляем обработчик кликов на каждую кнопку "Удалить"
//         ordersElements.forEach(element => {
//             const removeButton = element.querySelector('.removeButton');
//             removeButton.addEventListener('click', function () {
//                 // Сохраняем информацию о том, что элемент был скрыт в localStorage
//                 localStorage.setItem(`hidden_${element.dataset.serviceTitle}`, 'true');
//             });
//         });
//     });
document.addEventListener('DOMContentLoaded', function () {
    const orderButton = document.getElementById('orderButton');

    orderButton.addEventListener('click', function () {
        // Собираем информацию о заказах
        const orders = document.querySelectorAll('.order');
        let messageText = "Новый заказ:\n";

        orders.forEach(order => {
            const serviceTitle = order.getAttribute('data-service-title');
            const quantity = order.getAttribute('data-quantity');
            const totalCost = order.getAttribute('data-total-cost');

            messageText += `${serviceTitle} (${quantity} шт.) - ${totalCost} руб.\n`;
        });

        // Отправляем информацию на сервер Django для обработки
        sendOrderToDjango(messageText);
    });

    function sendOrderToDjango(messageText) {
        fetch('/process_order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({ message_text: messageText }), // Отправляем сообщение как JSON
        })
        .then(response => response.json())
        .then(data => {
            console.log('Order processed:', data);

            if (data.status === 'success') {
                // После успешной обработки заказа, отправляем заказ в Telegram
                sendTelegramMessage();
            } else {
                console.error('Error processing order:', data.message);
                alert('Произошла ошибка при обработке заказа.');
            }
        })
        .catch(error => {
            console.error('Error processing order:', error);
            alert('Произошла ошибка при обработке заказа.');
        });
    }

    function sendTelegramMessage() {
        // Ваш текущий код отправки сообщения в Telegram

        // После успешной отправки в Telegram, вызываем функцию для очистки корзины
        clearCart();
    }

    function clearCart() {
    fetch('/clear_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Cart cleared:', data);
            alert('Ваш заказ обработан и отправлен в УК ОЭЗ Моглино');

            // Обновляем страницу после успешной отчистки корзины
            location.reload();

            // Дополнительные действия при успешной отчистке корзины
        } else {
            console.error('Error clearing cart:', data.message);
            alert('Произошла ошибка при обработке заказа.');
        }
    })
    .catch(error => {
        console.error('Error clearing cart:', error);
        alert('Произошла ошибка при обработке заказа.');
    });
}
});





