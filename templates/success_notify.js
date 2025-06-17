// ==UserScript==
// @name         success_notify
// @namespace    http://tampermonkey.net/
// @version      2025-02-08
// @description  try to take over the world!
// @author       You
// @match        https://belarus.blsspainglobal.com/Global/payment/PaymentResponse*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Конфигурация Telegram
    const TELEGRAM_BOT_TOKEN = '7901901530:AAE29WGTOS3s7TBVUmShUEYBkXXPq7Ew1UA'; // Замените на ваш токен бота
    const TELEGRAM_CHAT_ID = '{{ TELEGRAM_CHAT_ID }}'; // Замените на ID чата

    // Флаг для отслеживания отправки сообщения
    let messageWasSent = false;

    // Функция для отправки сообщения в Telegram
    async function sendTelegramMessage(message) {
        if (messageWasSent) return; // Проверяем, было ли уже отправлено сообщение

        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chat_id: TELEGRAM_CHAT_ID,
                    text: message,
                    parse_mode: 'HTML'
                })
            });
            const data = await response.json();
            console.log('Сообщение отправлено в Telegram:', data);
            messageWasSent = true; // Устанавливаем флаг, что сообщение отправлено
        } catch (error) {
            console.error('Ошибка отправки в Telegram:', error);
        }
    }

    // Функция для проверки загрузки элемента
    function waitForElement(selector) {
        return new Promise(resolve => {
            if (document.querySelector(selector)) {
                return resolve(document.querySelector(selector));
            }

            const observer = new MutationObserver(mutations => {
                if (document.querySelector(selector)) {
                    observer.disconnect();
                    resolve(document.querySelector(selector));
                }
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
    }

    // Функция для извлечения данных и отправки в Telegram
    async function extractAndSendData() {
        try {
            console.log('Ожидание загрузки элемента...');

            // Ждем появления нужного элемента
            const cardDiv = await waitForElement('.card.card-body.bg-light.p-4');

            // Дополнительная задержка для гарантии загрузки содержимого
            await new Promise(resolve => setTimeout(resolve, 1000));

            console.log('Элемент найден, начинаем извлечение данных');

            // Извлекаем текст
            const items = cardDiv.querySelectorAll('.list-group-item');
            let data = "<b>Appointment Summary</b>\n\n";

            items.forEach((item) => {
                const label = item.querySelector('span:nth-child(1)');
                const value = item.querySelector('span:nth-child(2)');
                if (label && value) {
                    data += `<b>${label.textContent.trim()}</b>: ${value.textContent.trim()}\n`;
                }
            });

            // Отправляем данные в Telegram
            await sendTelegramMessage(data);
            console.log('Данные отправлены в Telegram');

        } catch (error) {
            console.error('Ошибка при извлечении данных:', error);
        }
    }

    // Функция инициализации с проверкой готовности DOM
    function initialize() {
        return new Promise(resolve => {
            if (document.readyState === 'complete') {
                console.log('DOM уже загружен');
                resolve();
            } else {
                console.log('Ожидание загрузки DOM...');
                window.addEventListener('load', () => {
                    console.log('DOM загружен');
                    resolve();
                });
            }
        });
    }

    // Запускаем скрипт
    (async function main() {
        try {
            console.log('Начало выполнения скрипта');
            await initialize();
            console.log('Страница полностью загружена, начинаем извлечение данных');
            await extractAndSendData();
        } catch (error) {
            console.error('Ошибка при выполнении скрипта:', error);
        }
    })();

})();
