// ==UserScript==
// @name         ТРЕВЕЛ ДАТА И ОТП ДЛЯ ОДНОГО (Имя, почта, пароль и дата вынесены)
// @namespace    http://tampermonkey.net/
// @version      2025-06-03
// @description  Автоматизация заполнения даты и отправки уведомления в Telegram
// @author       You
// @match        https://belarus.blsspainglobal.com/Global/Appointment/ApplicantSelection*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=blsspainrussia.ru
// @grant        none
// ==/UserScript==

(async function () {
    // === НАСТРОЙКИ ===
    const TELEGRAM_BOT_TOKEN = '7901901530:AAE29WGTOS3s7TBVUmShUEYBkXXPq7Ew1UA';
    const TELEGRAM_CHAT_ID = "{{ TELEGRAM_CHAT_ID }}";
    const USER_NAME = "{{ USER_NAME }}";                // Имя пользователя
    const EMAIL = "{{ EMAIL }}"; // Почта
    const EMAILPASSWORD = '{{ EMAILPASSWORD }}';                  // Пароль
    const TRAVEL_DATE = "{{ TRAVEL_DATE }}"           // Дата путешествия

    let messageWasSent = false;

    async function sendTelegramMessage() {
        if (messageWasSent) return;

        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
        const text = `❗️${USER_NAME} нужен КОД ОТП\n\nпочта: ${EMAIL}\nпароль: ${EMAILPASSWORD}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: TELEGRAM_CHAT_ID,
                    text: text,
                    parse_mode: 'HTML'
                })
            });
            const data = await response.json();
            console.log('Сообщение отправлено в Telegram:', data);
            messageWasSent = true;
        } catch (error) {
            console.error('Ошибка отправки в Telegram:', error);
        }
    }

    async function autoClickAgreeButton() {
        const modal = document.getElementById('termsmodal');
        const agreeButton = modal?.querySelector('.btn.btn-primary');

        if (modal && modal.style.display === 'block' && agreeButton) {
            agreeButton.click();
            console.log('Кнопка согласия в termsmodal нажата.');

            if (!messageWasSent) {
                await sendTelegramMessage();
            }

            await waitForTravelDateInput();
        }
    }

    async function waitForTravelDateInput() {
        const interval = setInterval(() => {
            const travelDateInput = document.querySelector('#TravelDate');
            if (travelDateInput && travelDateInput.offsetParent !== null) {
                travelDateInput.value = TRAVEL_DATE;
                travelDateInput.dispatchEvent(new Event('input', { bubbles: true }));
                travelDateInput.dispatchEvent(new Event('change', { bubbles: true }));

                const kendoDatePicker = $(travelDateInput).data('kendoDatePicker');
                if (kendoDatePicker) {
                    kendoDatePicker.value(TRAVEL_DATE);
                    kendoDatePicker.trigger('change');
                }

                console.log('Дата установлена:', TRAVEL_DATE);
                clearInterval(interval);
            }
        }, 100);
    }

    function changeAlertText() {
        const alertDivs = document.querySelectorAll('.alert.alert-warning.text-center');
        alertDivs.forEach((div) => {
            if (div.textContent.includes('An OTP has been sent to your registered email')) {
                div.innerHTML = '!! ЗАПРОСИТЕ У МЕНЕДЖЕРА КОД ОТП, СОСТОЯЩИЙ ИЗ 6 ЦИФР !!! <span class="required">*</span>';
                console.log('Текст в alert изменен.');
            }
        });
    }

    changeAlertText();

    const textCheckInterval = setInterval(() => {
        if (document.querySelector('.alert.alert-warning.text-center')) {
            changeAlertText();
            clearInterval(textCheckInterval);
        }
    }, 500);

    autoClickAgreeButton();
    setInterval(autoClickAgreeButton, 2000);
    waitForTravelDateInput();
})();

(function () {
    let isAgreeButtonClicked = false;

    async function autoClickAgreeButtonInPhotoUploadModal() {
        const modal = document.getElementById('photoUploadModal');
        const agreeButton = modal?.querySelector('.btn.btn-primary');

        if (modal && modal.style.display === 'block' && agreeButton) {
            agreeButton.click();
            isAgreeButtonClicked = true;
            console.log('Кнопка согласия в photoUploadModal нажата.');
        }
    }

    setInterval(autoClickAgreeButtonInPhotoUploadModal, 500);

    async function executeActionsSequentially() {
        try {
            while (!isAgreeButtonClicked) {
                await new Promise(resolve => setTimeout(resolve, 500));
            }

            console.log('Начинаем действия после подтверждения в фото модальном окне');

            await new Promise(resolve => setTimeout(resolve, 2000));
            const radioButton = document.querySelector('.rdo-applicant');
            if (radioButton && radioButton.offsetParent !== null) {
                radioButton.click();
                console.log('Радиокнопка нажата.');
            } else {
                console.warn('Радиокнопка не найдена.');
                return;
            }

            await new Promise(resolve => setTimeout(resolve, 500));
            const submitButton = document.getElementById('btnSubmit');
            if (submitButton && submitButton.offsetParent !== null) {
                submitButton.click();
                console.log('Кнопка Submit нажата.');
            } else {
                console.warn('Кнопка Submit не найдена.');
            }
        } catch (error) {
            console.error('Ошибка выполнения действий:', error);
        }
    }

    executeActionsSequentially();
})();
