// js/auth-login.js
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessageElement = document.getElementById('loginErrorMessage');
    const submitButton = loginForm.querySelector('button[type="submit"]');

    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        setLoading(true);

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        if (!username || !password) {
            displayError('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน');
            setLoading(false);
            return;
        }

        const loginApiUrl = `${API_BASE_URL}/auth/login`;

        try {
            const response = await fetch(loginApiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.message || `เกิดข้อผิดพลาด: ${response.status}`);
            }

            console.log('Login successful:', responseData);
            localStorage.setItem('authToken', responseData.token);
            localStorage.setItem('userId', responseData.userId);
            localStorage.setItem('userName', responseData.username);
            localStorage.setItem('isLoggedIn', 'true');

            alert('เข้าสู่ระบบสำเร็จ!');
            window.location.href = 'menu.html';

        } catch (error) {
            console.error('Login error:', error);
            const userFriendlyError = error.message.includes("Failed to fetch")
                ? 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาตรวจสอบและลองอีกครั้ง'
                : error.message;
            displayError(userFriendlyError);
        } finally {
            setLoading(false);
        }
    });

    function displayError(message) {
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = 'block';
    }

    function clearError() {
        errorMessageElement.textContent = '';
        errorMessageElement.style.display = 'none';
    }

    function setLoading(isLoading) {
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'กำลังเข้าสู่ระบบ...';
            clearError();
        } else {
            submitButton.disabled = false;
            submitButton.textContent = 'เข้าสู่ระบบ';
        }
    }
});