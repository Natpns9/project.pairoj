document.addEventListener('DOMContentLoaded', function() {
    // --- ตั้งค่าปีปัจจุบันใน Footer ---
    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }

    // --- ตรวจสอบสถานะการล็อกอิน ---
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const userName = localStorage.getItem('userName');
    
    const userAuthSection = document.getElementById('userAuthSection');
    const userProfileSection = document.getElementById('userProfileSection');
    const logoutLink = document.getElementById('logoutLink');
    const actionButtons = document.querySelectorAll('.action-buttons .btn');

    if (isLoggedIn && userName) {
        // --- กรณี: ล็อกอินแล้ว ---
        
        // 1. ซ่อนลิงก์ "เข้าสู่ระบบ / สมัครสมาชิก"
        if (userAuthSection) userAuthSection.style.display = 'none';
        
        // 2. แสดงส่วนโปรไฟล์และปุ่ม "ออกจากระบบ"
        if (userProfileSection) {
            userProfileSection.style.display = 'flex';
            // แสดงตัวอักษรแรกของชื่อผู้ใช้ในไอคอนโปรไฟล์
            userProfileSection.querySelector('.user-profile').textContent = userName.charAt(0).toUpperCase();
        }
        
        // 3. ตั้งค่าการทำงานให้ปุ่ม "ออกจากระบบ"
        if (logoutLink) {
            logoutLink.addEventListener('click', function(event) {
                event.preventDefault();
                // ล้างข้อมูลการล็อกอินทั้งหมด
                localStorage.removeItem('isLoggedIn');
                localStorage.removeItem('authToken');
                localStorage.removeItem('userName');
                localStorage.removeItem('userId');
                
                // แจ้งเตือนและกลับไปหน้าหลัก
                alert('ออกจากระบบสำเร็จ');
                window.location.href = 'menu.html';
            });
        }
        
        // 4. (ตรวจสอบ) ทำให้แน่ใจว่าปุ่มใช้งานได้
        actionButtons.forEach(button => {
            button.classList.remove('disabled');
            // ตรวจสอบว่ามี data-href เก็บไว้หรือไม่ ถ้ามีให้ใส่กลับเข้าไป
            if (button.dataset.href) {
                button.href = button.dataset.href;
            }
        });

    } else {
        // --- กรณี: ยังไม่ได้ล็อกอิน ---

        // 1. แสดงลิงก์ "เข้าสู่ระบบ / สมัครสมาชิก" (ตามค่าเริ่มต้น)
        if (userAuthSection) userAuthSection.style.display = 'flex';
        if (userProfileSection) userProfileSection.style.display = 'none';

        // 2. ปิดการใช้งานปุ่มระบบภาษีทั้งหมด
        actionButtons.forEach(button => {
            // เก็บ URL เดิมไว้ใน data attribute
            button.dataset.href = button.getAttribute('href');
            // ลบ URL ออกจากปุ่ม ทำให้คลิกไม่ได้
            button.removeAttribute('href');
            // เพิ่ม class 'disabled' เพื่อให้เราสามารถใส่สไตล์ให้มันดูเหมือนถูกปิดใช้งาน
            button.classList.add('disabled');
        });

        // 3. (ทางเลือก) เพิ่มข้อความแจ้งเตือน
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            const warningMessage = document.createElement('p');
            warningMessage.textContent = 'กรุณาเข้าสู่ระบบเพื่อใช้งานระบบยื่นภาษีออนไลน์';
            warningMessage.style.textAlign = 'center';
            warningMessage.style.color = '#d9534f';
            warningMessage.style.marginTop = '20px';
            warningMessage.style.fontWeight = 'bold';
            mainContent.appendChild(warningMessage);
        }
    }
});
