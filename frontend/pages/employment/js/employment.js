let currentPage = 0;
const pageSize = 10;

document.addEventListener('DOMContentLoaded', () => {
    loadEmployments();
});

async function loadEmployments() {
    const studentName = document.getElementById('search_student_name').value;
    const companyName = document.getElementById('search_company_name').value;
    const classId = document.getElementById('search_class_id').value;
    let url = `/employment/?skip=${currentPage}&limit=${pageSize}`;
    if (studentName) url += `&student_name=${studentName}`;
    if (companyName) url += `&company_name=${companyName}`;
    if (classId) url += `&class_id=${classId}`;
    try {
        const res = await apiRequest(url);
        const data = Array.isArray(res) ? res : (res.data || []);
        renderEmployments(data);
        renderPagination((currentPage / pageSize) + 1, pageSize, data.length, 'changePage');
    } catch (e) {
        console.error(e);
    }
}

function renderEmployments(data) {
    const tbody = document.getElementById('employment_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(e => `
        <tr>
            <td>${e.employment_id}</td>
            <td>${e.student_no}</td>
            <td>${e.student_name || '-'}</td>
            <td>${e.class_id || '-'}</td>
            <td>${formatDate(e.job_open_time)}</td>
            <td>${formatDate(e.offer_send_time)}</td>
            <td>${e.company_name || '-'}</td>
            <td>${e.salary !== null && e.salary !== undefined ? e.salary : '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editEmployment(${e.employment_id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteEmployment(${e.employment_id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function changePage(page) {
    if (page < 1) return;
    currentPage = (page - 1) * pageSize;
    loadEmployments();
}

function searchEmployments() {
    currentPage = 0;
    loadEmployments();
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增就业信息';
    document.getElementById('employment_id').value = '';
    document.getElementById('employment_form').reset();
    openModal('employment_modal');
}

async function editEmployment(id) {
    try {
        const res = await apiRequest(`/employment/?skip=0&limit=100`);
        const data = Array.isArray(res) ? res : (res.data || []);
        const emp = data.find(e => e.employment_id === id);
        if (emp) {
            document.getElementById('modal_title').textContent = '编辑就业信息';
            document.getElementById('employment_id').value = emp.employment_id;
            document.getElementById('form_student_no').value = emp.student_no;
            document.getElementById('form_student_name').value = emp.student_name || '';
            document.getElementById('form_class_id').value = emp.class_id || '';
            document.getElementById('form_job_open_time').value = emp.job_open_time ? formatDate(emp.job_open_time) : '';
            document.getElementById('form_offer_send_time').value = emp.offer_send_time ? formatDate(emp.offer_send_time) : '';
            document.getElementById('form_company_name').value = emp.company_name || '';
            document.getElementById('form_salary').value = emp.salary !== null && emp.salary !== undefined ? emp.salary : '';
            openModal('employment_modal');
        }
    } catch (e) {
        console.error(e);
    }
}

async function saveEmployment() {
    const id = document.getElementById('employment_id').value;
    const data = {
        student_no: document.getElementById('form_student_no').value,
        student_name: document.getElementById('form_student_name').value || null,
        class_id: document.getElementById('form_class_id').value ? parseInt(document.getElementById('form_class_id').value) : null,
        job_open_time: document.getElementById('form_job_open_time').value || null,
        offer_send_time: document.getElementById('form_offer_send_time').value || null,
        company_name: document.getElementById('form_company_name').value || null,
        salary: document.getElementById('form_salary').value ? parseInt(document.getElementById('form_salary').value) : null
    };
    try {
        if (id) {
            await apiRequest(`/employment/${id}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/employment/', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('employment_modal');
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

async function deleteEmployment(id) {
    if (!confirm('确定要删除该就业信息吗？')) return;
    try {
        await apiRequest(`/employment/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

async function restoreEmploymentById() {
    const employmentId = document.getElementById('restore_employment_id').value;
    if (!employmentId) {
        showToast('请输入就业ID', 'error');
        return;
    }
    try {
        await apiRequest(`/employment/restore/${employmentId}`, 'PUT');
        showToast('恢复成功', 'success');
        closeModal('restore_modal');
        document.getElementById('restore_employment_id').value = '';
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

function openRestoreModal() {
    document.getElementById('restore_employment_id').value = '';
    openModal('restore_modal');
}

function openSalaryRangeModal() {
    document.getElementById('salary_min').value = '';
    document.getElementById('salary_max').value = '';
    openModal('salary_range_modal');
}

async function searchBySalary() {
    const min = document.getElementById('salary_min').value;
    const max = document.getElementById('salary_max').value;
    if (!min || !max) {
        showToast('请输入最低和最高薪资', 'error');
        return;
    }
    try {
        const res = await apiRequest(`/employment/salary/range?salary_min=${min}&salary_max=${max}`);
        closeModal('salary_range_modal');
        const data = Array.isArray(res) ? res : (res.data || []);
        renderEmployments(data);
    } catch (e) {
        console.error(e);
    }
}

async function loadStatistics() {
    try {
        const res = await apiRequest('/employment/statistics');
        const data = res.data || res;
        document.getElementById('stats_title').textContent = '就业统计';
        let html = '';
        if (data) {
            for (const key in data) {
                const value = data[key];
                html += `<h4 style="margin:10px 0 5px;">${key}</h4>`;
                if (Array.isArray(value)) {
                    html += '<table style="margin-bottom:10px;"><thead><tr>';
                    if (value.length > 0) {
                        const keys = Object.keys(value[0]);
                        keys.forEach(k => { html += `<th>${k}</th>`; });
                    }
                    html += '</tr></thead><tbody>';
                    value.forEach(item => {
                        html += '<tr>';
                        Object.values(item).forEach(v => {
                            html += `<td>${v !== null && v !== undefined ? v : '-'}</td>`;
                        });
                        html += '</tr>';
                    });
                    html += '</tbody></table>';
                } else if (typeof value === 'object') {
                    html += `<table style="margin-bottom:10px;"><tbody>`;
                    for (const k in value) {
                        html += `<tr><td>${k}</td><td>${value[k]}</td></tr>`;
                    }
                    html += '</tbody></table>';
                } else {
                    html += `<p>${value}</p>`;
                }
            }
        }
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}
