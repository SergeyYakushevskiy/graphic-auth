document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // отменяем обычную отправку формы

    // Собираем данные из формы
    const formData = {
        login: document.getElementById('login').value,
        password: document.getElementById('password').value,
        mail: document.getElementById('mail').value,
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        birthDate: document.getElementById('birthDate').value
    };

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Регистрация прошла успешно!');
            // Например, редирект на страницу логина
            window.location.href = '/login';
        } else {
            const error = await response.text();
            alert('Ошибка регистрации: ' + error);
        }
    } catch (err) {
        alert('Ошибка сети или сервера: ' + err.message);
    }
});