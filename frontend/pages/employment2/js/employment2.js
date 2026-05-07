let currentData = [];

document.addEventListener('DOMContentLoaded', () => {
    loadEmployments();
});

async function loadEmployments() {
    const studentNo = document.getElementById('search_student_no').value;
    const classId = document.getElementById('search_class_id').value;
    const company = document.getElementById('search_company').value;
    const salaryMin = document.getElementById('search_salary_min').value;
    const salaryMax = document.getElementById('search_salary_max').value;
    
    try {
        let data = [];
        if (studentNo) {
            const res = await apiRequest(`/employment2/check/${studentNo}`);
            data = res ? [res] : [];
        } else if (classId) {
            const res = await apiRequest(`/employment2/class/${classId}`);
            data = res || [];
        } else if (company) {
            const res = await apiRequest(`/employment2/company/${company}`);
            data = res || [];
        } else if (salaryMin && salaryMax) {
            const res = await apiRequest(`/employment2/salary/${salaryMin}/${salaryMax}`);
            data = res || [];
        } else {
            const res = await apiRequest('/employment2/all');
            data = res || [];
        }
        currentData = data;
        renderEmployments(data);
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
            <td>${e.student_name}</td>
            <td>${e.class_id}</td>
            <td>${e.job_open_time ? new Date(e.job_open_time).toLocaleString() : '-'}</td>
            <td>${e.offer_send_time ? new Date(e.offer_send_time).toLocaleString() : '-'}</td>
            <td>${e.company_name || '-'}</td>
            <td>${e.salary !== null && e.salary !== undefined ? e.salary : '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editEmployment('${e.student_no}')">编辑</button>
                <button class="btn btn-danger" onclick="deleteEmployment('${e.student_no}')">删除</button>
            </td>
        </tr>
    `).join('');
}

function searchEmployments() {
    loadEmployments();
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增就业信息';
    document.getElementById('edit_student_no').value = '';
    document.getElementById('employment_form').reset();
    document.getElementById('form_student_no').disabled = false;
    openModal('employment_modal');
}

async function editEmployment(studentNo) {
    try {
        const res = await apiRequest(`/employment2/check/${studentNo}`);
        document.getElementById('modal_title').textContent = '编辑就业信息';
        document.getElementById('edit_student_no').value = res.student_no;
        document.getElementById('form_student_no').value = res.student_no;
        document.getElementById('form_student_no').disabled = true;
        document.getElementById('form_student_name').value = res.student_name;
        document.getElementById('form_class_id').value = res.class_id;
        document.getElementById('form_job_open_time').value = res.job_open_time ? new Date(res.job_open_time).toISOString().slice(0, 16) : '';
        document.getElementById('form_offer_send_time').value = res.offer_send_time ? new Date(res.offer_send_time).toISOString().slice(0, 16) : '';
        document.getElementById('form_company_name').value = res.company_name || '';
        document.getElementById('form_salary').value = res.salary !== null && res.salary !== undefined ? res.salary : '';
        openModal('employment_modal');
    } catch (e) {
        console.error(e);
    }
}

async function saveEmployment() {
    const editStudentNo = document.getElementById('edit_student_no').value;
    const data = {
        student_no: document.getElementById('form_student_no').value,
        student_name: document.getElementById('form_student_name').value,
        class_id: parseInt(document.getElementById('form_class_id').value),
        job_open_time: document.getElementById('form_job_open_time').value || null,
        offer_send_time: document.getElementById('form_offer_send_time').value || null,
        company_name: document.getElementById('form_company_name').value || null,
        salary: document.getElementById('form_salary').value ? parseInt(document.getElementById('form_salary').value) : null
    };
    try {
        if (editStudentNo) {
            await apiRequest(`/employment2/update/${editStudentNo}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/employment2/add', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('employment_modal');
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

async function deleteEmployment(studentNo) {
    if (!confirm('确定要删除该就业信息吗？')) return;
    try {
        await apiRequest(`/employment2/delete/${studentNo}`, 'DELETE');
        showToast('删除成功', 'success');
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

async function recoverEmploymentById() {
    const studentNo = document.getElementById('restore_student_no').value;
    if (!studentNo) {
        showToast('请输入学号', 'error');
        return;
    }
    try {
        await apiRequest(`/employment2/recover/${studentNo}`, 'POST');
        showToast('恢复成功', 'success');
        closeModal('restore_modal');
        document.getElementById('restore_student_no').value = '';
        loadEmployments();
    } catch (e) {
        console.error(e);
    }
}

function openRestoreModal() {
    document.getElementById('restore_student_no').value = '';
    openModal('restore_modal');
}
