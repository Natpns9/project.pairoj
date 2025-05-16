
        document.getElementById('currentYear').textContent = new Date().getFullYear();

        const userAuthSection = document.getElementById('userAuthSection');
        const userProfileSection = document.getElementById('userProfileSection');
        const logoutLink = document.getElementById('logoutLink');

        // --- ฟังก์ชันจำลองการล็อกอิน/ล็อกเอาท์ (สำหรับสาธิต) ---
        // ในแอปพลิเคชันจริง ส่วนนี้จะถูกจัดการโดย server-side logic และ sessions

        function showLoggedInState() {
            if (userAuthSection) userAuthSection.style.display = 'none';
            if (userProfileSection) userProfileSection.style.display = 'flex'; // หรือ 'block' ขึ้นอยู่กับ CSS
            // อาจเก็บสถานะการล็อกอินใน localStorage เพื่อความต่อเนื่องง่ายๆ
            localStorage.setItem('isLoggedIn', 'true');
        }

        function showLoggedOutState() {
            if (userAuthSection) userAuthSection.style.display = 'flex'; // หรือ 'block'
            if (userProfileSection) userProfileSection.style.display = 'none';
            localStorage.removeItem('isLoggedIn');
            // alert('คุณออกจากระบบแล้ว'); // ยกเลิกการ alert อัตโนมัติเมื่อโหลดหน้า
        }

        if (logoutLink) {
            logoutLink.addEventListener('click', function(event) {
                event.preventDefault(); // ป้องกันการ redirect ของลิงก์ #
                // ทำการล็อกเอาท์ (เช่น ล้าง session, token)
                alert('คุณออกจากระบบแล้ว'); // แจ้งผู้ใช้
                showLoggedOutState();
                // สามารถ redirect ไปหน้า login ได้หากต้องการ
                // window.location.href = "login.html";
            });
        }

        // ตรวจสอบสถานะการล็อกอิน (จำลอง) เมื่อโหลดหน้า
        // ในการใช้งานจริง คุณควรตรวจสอบ session หรือ token จาก server
        if (localStorage.getItem('isLoggedIn') === 'true') {
            showLoggedInState();
        } else {
            showLoggedOutState(); // ตรวจสอบให้แน่ใจว่าแสดงสถานะ logout ถูกต้องเมื่อเริ่ม
        }

        // ---- สิ้นสุดส่วนจำลอง ----

        // คุณสามารถเรียก showLoggedInState() หลังจากผู้ใช้ล็อกอินสำเร็จจากหน้า login.html
        // ตัวอย่าง: ถ้า login.html redirect กลับมาที่ menu.html หลังล็อกอินสำเร็จ
        // คุณอาจจะตั้งค่า flag ใน localStorage จาก login.html แล้วตรวจสอบที่นี่
  

document.getElementById('currentYear').textContent = new Date().getFullYear();
        // Basic form submission handling (client-side only example)
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent actual form submission
            const username = document.getElementById('username').value;
            // In a real application, you would send this to a server for validation
            alert('Login attempt for: ' + username);
            // Example: Redirect to main page after "login"
            // window.location.href = "menu.html";
        });

