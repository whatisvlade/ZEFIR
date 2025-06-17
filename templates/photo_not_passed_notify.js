// ==UserScript==
// @name         ФОТО НЕ ПРОШЛО (Improved)
// @namespace    http://tampermonkey.net/
// @version      2025-06-03
// @description  Логирование запросов, UI-оповещения и отправка статусов в Telegram
// @author       You
// @match        https://belarus.blsspainglobal.com/Global/Appointment/ApplicantSelection*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=blsspainrussia.ru
// @grant        GM_xmlhttpRequest
// @connect      api.telegram.org
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    // Имя для Telegram-сообщений
    const USER_NAME = "{{ USER_NAME }}"; // Измени на нужное

    // Конфигурация Telegram бота
    const TELEGRAM_BOT_TOKEN = '7901901530:AAE29WGTOS3s7TBVUmShUEYBkXXPq7Ew1UA'; // Замените на ваш токен бота
    const TELEGRAM_CHAT_ID = "{{ TELEGRAM_CHAT_ID }}"; // Замените на ваш Chat ID

    // Функция для отправки сообщения в Telegram
    function sendTelegramMessage(message) {
        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat_id: TELEGRAM_CHAT_ID,
                text: message,
                parse_mode: 'HTML'
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Telegram message sent:', data);
            if (!data.ok) {
                console.error('Ошибка Telegram API:', data);
            }
        })
        .catch(error => console.error('Error sending Telegram message:', error));
    }

    // Функция для отображения сообщения на странице
    function showMessage(message, color) {
        const existingMessage = document.getElementById("status-message");
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageDiv = document.createElement("div");
        messageDiv.id = "status-message";
        messageDiv.style.position = "fixed";
        messageDiv.style.top = "0";
        messageDiv.style.left = "0";
        messageDiv.style.width = "100%";
        messageDiv.style.zIndex = "9999";
        messageDiv.style.backgroundColor = color || "red";
        messageDiv.style.color = "white";
        messageDiv.style.textAlign = "center";
        messageDiv.style.padding = "10px";
        messageDiv.style.fontSize = "18px";
        messageDiv.style.fontWeight = "bold";
        messageDiv.style.fontFamily = "Arial, sans-serif";
        messageDiv.textContent = message;

        document.body.appendChild(messageDiv);

        // Автоматическое скрытие через 5 секунд
        setTimeout(() => messageDiv.remove(), 5000);
    }

    // Функция для обработки статуса
    function handleStatus(method, url, status) {
        console.log(`Запрос: ${method} ${url} -> Статус: ${status}`);

        if (url.includes("/Global/appointment/UploadApplicantPhoto")) {
            let message = '';
            let telegramMessage = '';

            if (status === 200) {
                message = "ФОТО ЗАГРУЖЕНО УСПЕШНО.";
                showMessage(message, "green");

            } else if (status === 429) {
                message = "УПС. АЙПИ ЗАБЛОКИРОВАН. ПЕРЕХОД НА СТРАНИЦУ ВХОДА.";
                showMessage(message, "red");
                setTimeout(() => {
                    window.location.href = "https://belarus.blsspainglobal.com/Global/account/Login?returnUrl=%2FGlobal%2Fappointment%2Fnewappointment&err=K7LYPi%2FpJtiLxj0JgYMBPVTdQ5hDdq9IVd7ALDT6sMo%3D";
                }, 2000);
            } else {
                message = "УПС. ПРОБУЕМ ДРУГОЕ ФОТО, СТРАНИЦА САМА ОБНОВИТСЯ.";
                telegramMessage = `⚠️${USER_NAME} ФОТО НЕ ЗАГРУЗИЛОСЬ`;
                showMessage(message, "orange");
                sendTelegramMessage(telegramMessage);
                setTimeout(() => {
                    location.reload();
                }, 3000);
            }
        }
    }

    // Перехват XMLHttpRequest-запросов
    (function () {
        const originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function (method, url, ...rest) {
            this._requestMethod = method;
            this._requestUrl = url;
            console.log(`Перехвачен запрос: ${method} ${url}`);
            originalOpen.apply(this, [method, url, ...rest]);
        };

        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function (...args) {
            this.addEventListener("load", function () {
                try {
                    handleStatus(this._requestMethod, this._requestUrl, this.status);
                } catch (error) {
                    console.error("Ошибка при обработке статуса:", error);
                }
            });
            originalSend.apply(this, args);
        };
    })();

    console.log("Скрипт запущен и готов к работе.");
})();
