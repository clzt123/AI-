let currentPage = 1;
const pageSize = 10;
let deletedPage = 1;

document.addEventListener('DOMContentLoaded', () => {
    loadTeachers();
});

async function loadTeachers() {
    const name = document.getElementById('search_name').value;
    const gender = document.getElementById('search_gender').value;
    let url = `/teachers/check?page=${currentPage}&page_size=${pageSize}`;
    if (name) url += `&teacher_name=${name}`;
    if (gender) url += `&gender=${gender}`;
    try {
        const res = await apiRequest(url);
        const data = Array.isArray(res) ? res : (res.data || []);
        renderTeachers(data);
        renderPagination(res.page || 1, res.page_size || pageSize, res.total || 0, 'changePage');
    } catch (e) {
        console.error(e);
    }
}

function renderTeachers(data) {
    const tbody = document.getElementById('teacher_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(t => `
        <tr>
            <td>${t.teacher_id}</td>
            <td>${t.teacher_name}</td>
            <td>${t.gender || '-'}</td>
            <td>${t.phone || '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editTeacher(${t.teacher_id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteTeacher(${t.teacher_id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function changePage(page) {
    if (page < 1) return;
    currentPage = page;
    loadTeachers();
}

function searchTeachers() {
    currentPage = 1;
    loadTeachers();
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增老师';
    document.getElementById('teacher_id').value = '';
    document.getElementById('teacher_form').reset();
    openModal('teacher_modal');
}

async function editTeacher(id) {
    try {
        const res = await apiRequest(`/teachers/check/${id}`);
        document.getElementById('modal_title').textContent = '编辑老师';
        document.getElementById('teacher_id').value = res.teacher_id;
        document.getElementById('form_teacher_name').value = res.teacher_name;
        document.getElementById('form_gender').value = res.gender || '';
        document.getElementById('form_phone').value = res.phone || '';
        openModal('teacher_modal');
    } catch (e) {
        console.error(e);
    }
}

async function saveTeacher() {
    const id = document.getElementById('teacher_id').value;
    const data = {
        teacher_name: document.getElementById('form_teacher_name').value,
        gender: document.getElementById('form_gender').value || null,
        phone: document.getElementById('form_phone').value || null
    };
    try {
        if (id) {
            await apiRequest(`/teachers/update/${id}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/teachers/create', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('teacher_modal');
        loadTeachers();
    } catch (e) {
        console.error(e);
    }
}

async function deleteTeacher(id) {
    if (!confirm('确定要删除该老师吗？')) return;
    try {
        await apiRequest(`/teachers/delete/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadTeachers();
    } catch (e) {
        console.error(e);
    }
}

async function restoreTeacher(id) {
    try {
        await apiRequest(`/teachers/restore/${id}`, 'PUT');
        showToast('恢复成功', 'success');
        loadDeletedTeachers();
    } catch (e) {
        console.error(e);
    }
}

async function loadDeletedTeachers() {
    deletedPage = 1;
    fetchDeletedTeachers();
    openModal('deleted_modal');
}

async function fetchDeletedTeachers() {
    let url = `/teachers/deleted?page=${deletedPage}&page_size=${pageSize}`;
    try {
        const res = await apiRequest(url);
        renderDeletedTeachers(res.data || []);
        renderDeletedPagination(res.page || 1, res.page_size || pageSize, res.total || 0);
    } catch (e) {
        console.error(e);
    }
}

function renderDeletedTeachers(data) {
    const tbody = document.getElementById('deleted_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(t => `
        <tr>
            <td>${t.teacher_id}</td>
            <td>${t.teacher_name}</td>
            <td>${t.gender || '-'}</td>
            <td>${t.phone || '-'}</td>
            <td class="action-btns">
                <button class="btn btn-success" onclick="restoreTeacher(${t.teacher_id})">恢复</button>
            </td>
        </tr>
    `).join('');
}

function renderDeletedPagination(current, size, total) {
    const totalPages = Math.ceil(total / size);
    const el = document.getElementById('deleted_pagination');
    el.innerHTML = `
        <button onclick="changeDeletedPage(${current - 1})" ${current <= 1 ? 'disabled' : ''}>上一页</button>
        <span>第 ${current} 页 / 共 ${totalPages || 1} 页 (共 ${total} 条)</span>
        <button onclick="changeDeletedPage(${current + 1})" ${current >= totalPages ? 'disabled' : ''}>下一页</button>
    `;
}

function changeDeletedPage(page) {
    if (page < 1) return;
    deletedPage = page;
    fetchDeletedTeachers();
}

async function loadStats() {
    try {
        const res = await apiRequest('/teachers/stats');
        document.getElementById('stats_title').textContent = '老师性别统计';
        let html = '<div class="stat-cards">';
        html += `<div class="stat-card"><h4>总人数</h4><div class="value">${res.total}</div></div>`;
        html += `<div class="stat-card"><h4>男老师</h4><div class="value">${res.male_count}</div></div>`;
        html += `<div class="stat-card"><h4>女老师</h4><div class="value">${res.female_count}</div></div>`;
        html += '</div>';
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}
