function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toISOString().split('T')[0];
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

function renderPagination(currentPage, pageSize, total, onPageChange) {
    const totalPages = Math.ceil(total / pageSize);
    const paginationEl = document.getElementById('pagination');
    if (!paginationEl) return;
    
    let html = `
        <button onclick="${onPageChange}(${currentPage - 1})" ${currentPage <= 1 ? 'disabled' : ''}>上一页</button>
        <span>第 ${currentPage} 页 / 共 ${totalPages || 1} 页 (共 ${total} 条)</span>
        <button onclick="${onPageChange}(${currentPage + 1})" ${currentPage >= totalPages ? 'disabled' : ''}>下一页</button>
    `;
    paginationEl.innerHTML = html;
}

function getGenderOptions(selected) {
    return `
        <option value="">请选择</option>
        <option value="男" ${selected === '男' ? 'selected' : ''}>男</option>
        <option value="女" ${selected === '女' ? 'selected' : ''}>女</option>
    `;
}
