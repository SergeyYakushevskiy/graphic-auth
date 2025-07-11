document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Отключаем стандартную отправку формы

    const identifier = document.getElementById("identifier").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ identifier, password }),
            credentials: "include" // важно: позволяет принимать HttpOnly куки
        });

        if (response.ok) {
            const data = await response.json();
            if (data["2fa_required"]) {
                window.location.href = data.redirect || "/two-factor";
            } else {
                alert("2FA не требуется — доступ предоставлен (что странно для этого проекта)");
            }
        } else if (response.status === 401) {
            const text = await response.text();
            alert("Ошибка авторизации: " + text);
        } else {
            alert("Неизвестная ошибка: " + response.status);
        }
    } catch (error) {
        console.error("Ошибка запроса:", error);
        alert("Ошибка подключения к серверу.");
    }
});