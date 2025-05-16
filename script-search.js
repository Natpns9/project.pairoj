document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('companySearchForm');
    const searchQueryInput = document.getElementById('searchQuery');
    const clearSearchBtn = document.getElementById('clearSearch');
    const resultsDisplaySection = document.getElementById('resultsDisplaySection');
    const resultsTitle = document.getElementById('resultsTitle'); // เพิ่มมา
    const resultsList = document.getElementById('resultsList');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const resultsCount = document.getElementById('resultsCount');
    const paginationControls = document.getElementById('paginationControls'); // ถ้ามี pagination

    // แสดงปีปัจจุบันใน Footer
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    // --- Mock Data (ข้อมูลตัวอย่าง) ---
    // ในระบบจริง ข้อมูลนี้จะมาจาก Backend API
    const allCompanies = [
        { id: "01055XXXXXX1", name: "บริษัท ตัวอย่าง เอ จำกัด (มหาชน)", taxId: "01055XXXXXX1" },
        { id: "01075XXXXXX2", name: "บริษัท ทดสอบ บี จำกัด", taxId: "01075XXXXXX2" },
        { id: "1234567890123", name: "ห้างหุ้นส่วนจำกัด ซี โปรแกรมมิ่ง", taxId: "1234567890123" },
        { id: "0105500000000", name: "บริษัท ไพโรจน์พัฒนาการบัญชี จำกัด", taxId: "0105500000000" },
        { id: "9876543210987", name: "ร้าน ดีอีเอฟ การค้า", taxId: "9876543210987" },
    ];

    // --- Event Listeners ---
    searchQueryInput.addEventListener('input', function() {
        if (searchQueryInput.value.length > 0) {
            clearSearchBtn.style.display = 'inline-block';
        } else {
            clearSearchBtn.style.display = 'none';
        }
    });

    clearSearchBtn.addEventListener('click', function() {
        searchQueryInput.value = '';
        clearSearchBtn.style.display = 'none';
        searchQueryInput.focus();
        hideResults(); // ซ่อนผลลัพธ์เมื่อล้างคำค้นหา
    });

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // ป้องกันการ submit form แบบปกติ
        performSearch();
    });

    // --- Functions ---
    function performSearch() {
        const query = searchQueryInput.value.toLowerCase().trim();

        if (!query) {
            // ถ้า query ว่างเปล่า อาจจะซ่อนผลลัพธ์ หรือแสดงข้อความบางอย่าง
            hideResults();
            // alert("กรุณาป้อนคำค้นหา");
            return;
        }

        // Simulate API call / filtering
        // กรองข้อมูลจากชื่อบริษัท หรือ เลขประจำตัวผู้เสียภาษี
        const filteredData = allCompanies.filter(company =>
            company.name.toLowerCase().includes(query) ||
            (company.taxId && company.taxId.toLowerCase().includes(query))
        );

        displayResults(filteredData, query);
    }

    function displayResults(data, query) {
        resultsList.innerHTML = ''; // เคลียร์รายการผลลัพธ์เก่า

        if (query) { // แสดงส่วนผลลัพธ์ต่อเมื่อมีการค้นหาจริง
            resultsDisplaySection.style.display = 'block';
            resultsTitle.textContent = `ผลการค้นหาสำหรับ "${searchQueryInput.value}"`; // แสดงคำค้นหาในหัวข้อ
        }


        if (data && data.length > 0) {
            resultsCount.textContent = `พบ ${data.length} รายการ`;
            noResultsMessage.style.display = 'none';
            resultsList.style.display = ''; // แสดง ul
            // paginationControls.style.display = ''; // แสดง pagination (ถ้ามี logic)

            data.forEach(company => {
                const listItem = document.createElement('li');
                listItem.className = 'result-item';
                listItem.innerHTML = `
                    <span class="company-name">${company.name}</span>
                    <a href="company-details.html?id=${company.id}" class="view-details-btn">ดูรายละเอียด</a>
                `;
                // อาจจะเพิ่มข้อมูล taxId ถ้าต้องการแสดงในรายการ
                // <p class="company-taxid">เลขผู้เสียภาษี: ${company.taxId}</p>
                resultsList.appendChild(listItem);
            });
        } else if (query) { // ถ้ามีการค้นหา (query ไม่ใช่ค่าว่าง) แต่ไม่พบข้อมูล
            resultsCount.textContent = 'พบ 0 รายการ';
            noResultsMessage.style.display = 'block';
            resultsList.style.display = 'none';
            // paginationControls.style.display = 'none';
        } else {
            hideResults();
        }
    }

    function hideResults() {
        resultsDisplaySection.style.display = 'none';
        resultsList.innerHTML = '';
        noResultsMessage.style.display = 'none';
        resultsCount.textContent = '';
        // paginationControls.style.display = 'none';
    }

    // เริ่มต้นซ่อนส่วนแสดงผลลัพธ์
    hideResults();

});