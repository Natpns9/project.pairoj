// js/auth-signup.js
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const errorMessagesContainer = document.getElementById('error-messages');
    const submitButton = signupForm.querySelector('button[type="submit"]');

    if (!signupForm) return;

    signupForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        setLoading(true);

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const terms = document.getElementById('terms').checked;

        let errors = [];
        if (username.length < 5) errors.push('ชื่อผู้ใช้ต้องมีความยาวอย่างน้อย 5 ตัวอักษร');
        if (!/^\S+@\S+\.\S+$/.test(email)) errors.push('รูปแบบอีเมลไม่ถูกต้อง');
        if (password.length < 8) errors.push('รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร');
        if (password !== confirmPassword) errors.push('รหัสผ่านและการยืนยันรหัสผ่านไม่ตรงกัน');
        if (!terms) errors.push('โปรดยอมรับข้อตกลงและเงื่อนไขการใช้งาน');

        if (errors.length > 0) {
            displayErrors(errors);
            setLoading(false);
            return;
        }

        const signupApiUrl = `${API_BASE_URL}/auth/signup`;

        try {
            const response = await fetch(signupApiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.message || `เกิดข้อผิดพลาด: ${response.status}`);
            }

            alert('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบเพื่อใช้งาน');
            window.location.href = 'login.html';

        } catch (error) {
            console.error('Signup error:', error);
            const userFriendlyError = error.message.includes("Failed to fetch")
                ? 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาตรวจสอบและลองอีกครั้ง'
                : error.message;
            displayErrors([userFriendlyError]);
        } finally {
            setLoading(false);
        }
    });

    function displayErrors(errorMessages) {
        errorMessagesContainer.style.display = 'block';
        let errorList = '<ul>' + errorMessages.map(e => `<li>${e}</li>`).join('') + '</ul>';
        errorMessagesContainer.innerHTML = errorList;
    }

    function clearErrors() {
        errorMessagesContainer.innerHTML = '';
        errorMessagesContainer.style.display = 'none';
    }

    function setLoading(isLoading) {
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'กำลังสมัครสมาชิก...';
            clearErrors();
        } else {
            submitButton.disabled = false;
            submitButton.textContent = 'สมัครสมาชิก';
        }
    }
});