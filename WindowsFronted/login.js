// login.js (สำหรับใช้ใน menu.html และหน้าที่ต้องการแสดงสถานะ login/logout UI)

document.addEventListener('DOMContentLoaded', function() {
    // แสดงปีปัจจุบันใน Footer (ถ้ามี element #currentYear ในหน้านั้น)
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // ส่วนจัดการการแสดงผล User Auth/Profile
    const userAuthSection = document.getElementById('userAuthSection');
    const userProfileSection = document.getElementById('userProfileSection');
    const logoutLink = document.getElementById('logoutLink');
    // หา .user-profile ที่อยู่ภายใน userProfileSection เพื่อแสดงชื่อย่อ
    const userProfileDiv = userProfileSection ? userProfileSection.querySelector('.user-profile') : null;

    function updateLoginStateUI() {
        // ในระบบจริง: ควรมีการเรียก API เพื่อตรวจสอบสถานะ session/token ที่ถูกต้อง
        // หรือตรวจสอบความ valid ของ token ที่เก็บไว้
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        const userName = localStorage.getItem('userName'); // ดึงชื่อผู้ใช้ที่อาจเก็บไว้ตอน login

        if (isLoggedIn) {
            if (userAuthSection) {
                userAuthSection.style.display = 'none';
            }
            if (userProfileSection) {
                userProfileSection.style.display = 'flex'; // หรือ 'block' หรือตาม CSS ที่คุณใช้
            }
            if (userProfileDiv && userName) {
                // แสดงอักษรตัวแรกของชื่อผู้ใช้เป็นตัวพิมพ์ใหญ่
                userProfileDiv.textContent = userName.charAt(0).toUpperCase();
            } else if (userProfileDiv) {
                userProfileDiv.textContent = 'U'; // Default placeholder
            }
        } else {
            if (userAuthSection) {
                userAuthSection.style.display = 'flex'; // หรือ 'block'
            }
            if (userProfileSection) {
                userProfileSection.style.display = 'none';
            }
        }
    }

    if (logoutLink) {
        logoutLink.addEventListener('click', async function(event) {
            event.preventDefault();

            // --- ส่วนนี้จะต้องเรียก API Logout ที่คุณจะสร้างใน server.js ---
            // Endpoint นี้เป็นตัวอย่าง คุณต้องสร้างมันใน server.js
            const logoutApiUrl = 'http://localhost:3001/api/auth/logout';

            try {
                console.log(`Attempting to logout via API: ${logoutApiUrl}`);
                // const authToken = localStorage.getItem('authToken'); // ถ้ามีการใช้ token
                // const response = await fetch(logoutApiUrl, {
                //     method: 'POST',
                //     headers: {
                //         'Content-Type': 'application/json',
                //         // 'Authorization': `Bearer ${authToken}` // ถ้า API ต้องการ token
                //     }
                // });

                // if (!response.ok) {
                //     const errorData = await response.json().catch(() => ({}));
                //     throw new Error(errorData.message || `Logout failed with status: ${response.status}`);
                // }

                // console.log('Logout API call successful'); // เมื่อ API ตอบกลับมาว่าสำเร็จ

            } catch (error) {
                console.error('Logout API error:', error);
                // อาจจะแจ้งผู้ใช้หรือไม่ก็ได้ เพราะยังไงก็จะเคลียร์ฝั่ง client อยู่ดี
            }

            // เคลียร์ข้อมูลการล็อกอินฝั่ง Client เสมอ ไม่ว่า API call จะสำเร็จหรือไม่
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('userName');
            // localStorage.removeItem('authToken'); // ถ้ามีการใช้ token

            alert('คุณออกจากระบบแล้ว');
            updateLoginStateUI(); // อัปเดต UI ทันที

            // (ทางเลือก) Redirect ไปหน้า login หรือหน้าหลัก
            // window.location.href = 'login.html';
        });
    }

    // เรียกเพื่ออัปเดต UI เมื่อหน้าโหลดครั้งแรก
    updateLoginStateUI();

    // (ทางเลือก) เพิ่ม event listener เพื่อตรวจจับการเปลี่ยนแปลงใน localStorage จาก tab อื่น
    // เพื่อให้ UI อัปเดตตรงกัน (ถ้ามีการล็อกอิน/ล็อกเอาท์จาก tab อื่น)
    window.addEventListener('storage', function(event) {
        if (event.key === 'isLoggedIn' || event.key === 'userName') {
            console.log('Storage event detected, updating UI.');
            updateLoginStateUI();
        }
    });
});
