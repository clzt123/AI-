let currentStudents = [];

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
});

async function loadStudents() {
    try {
        const res = await apiRequest('/students2/all');
        currentStudents = res || [];
        renderStudents(currentStudents);
    } catch (e) {
        console.error(e);
    }
}

function renderStudents(data) {
    const tbody = document.getElementById('student_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.student_no}</td>
            <td>${s.student_name}</td>
            <td>${s.gender || '-'}</td>
            <td>${s.age || '-'}</td>
            <td>${s.class_id}</td>
            <td>${s.native_place || '-'}</td>
            <td>${s.graduate_school || '-'}</td>
            <td>${s.major || '-'}</td>
            <td>${s.education || '-'}</td>
            <td>${formatDate(s.admission_time)}</td>
            <td>${formatDate(s.graduate_time)}</td>
            <td>${s.advisor_id || '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editStudent(${s.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteStudent(${s.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

async function searchStudent() {
    const id = document.getElementById('search_student_id').value;
    if (!id) {
        showToast('请输入学生ID', 'error');
        return;
    }
    try {
        const res = await apiRequest(`/students2/student_get/${id}`);
        renderStudents([res]);
    } catch (e) {
        console.error(e);
    }
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增学生';
    document.getElementById('student_id').value = '';
    document.getElementById('student_form').reset();
    openModal('student_modal');
}

async function editStudent(id) {
    try {
        const res = await apiRequest(`/students2/student_get/${id}`);
        document.getElementById('modal_title').textContent = '编辑学生';
        document.getElementById('student_id').value = res.id;
        document.getElementById('form_student_no').value = res.student_no;
        document.getElementById('form_class_id').value = res.class_id;
        document.getElementById('form_student_name').value = res.student_name;
        document.getElementById('form_gender').value = res.gender || '';
        document.getElementById('form_age').value = res.age || '';
        document.getElementById('form_native_place').value = res.native_place || '';
        document.getElementById('form_graduate_school').value = res.graduate_school || '';
        document.getElementById('form_major').value = res.major || '';
        document.getElementById('form_education').value = res.education || '';
        document.getElementById('form_admission_time').value = res.admission_time ? formatDate(res.admission_time) : '';
        document.getElementById('form_graduate_time').value = res.graduate_time ? formatDate(res.graduate_time) : '';
        document.getElementById('form_advisor_id').value = res.advisor_id || '';
        openModal('student_modal');
    } catch (e) {
        console.error(e);
    }
}

async function saveStudent() {
    const id = document.getElementById('student_id').value;
    const data = {
        student_no: document.getElementById('form_student_no').value,
        class_id: parseInt(document.getElementById('form_class_id').value),
        student_name: document.getElementById('form_student_name').value,
        gender: document.getElementById('form_gender').value || null,
        age: document.getElementById('form_age').value ? parseInt(document.getElementById('form_age').value) : null,
        native_place: document.getElementById('form_native_place').value || null,
        graduate_school: document.getElementById('form_graduate_school').value || null,
        major: document.getElementById('form_major').value || null,
        education: document.getElementById('form_education').value || null,
        admission_time: document.getElementById('form_admission_time').value || null,
        graduate_time: document.getElementById('form_graduate_time').value || null,
        advisor_id: document.getElementById('form_advisor_id').value ? parseInt(document.getElementById('form_advisor_id').value) : null
    };
    try {
        if (id) {
            await apiRequest(`/students2/student_update/${id}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/students2/student_create/', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('student_modal');
        loadStudents();
    } catch (e) {
        console.error(e);
    }
}

async function deleteStudent(id) {
    if (!confirm('确定要删除该学生吗？')) return;
    try {
        await apiRequest(`/students2/student_delete/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadStudents();
    } catch (e) {
        console.error(e);
    }
}

async function restoreStudentById() {
    const studentId = document.getElementById('restore_student_id').value;
    if (!studentId) {
        showToast('请输入学生ID', 'error');
        return;
    }
    try {
        await apiRequest(`/students2/student_restore/${studentId}`, 'PUT');
        showToast('恢复成功', 'success');
        closeModal('restore_modal');
        document.getElementById('restore_student_id').value = '';
        loadStudents();
    } catch (e) {
        console.error(e);
    }
}

function openRestoreModal() {
    document.getElementById('restore_student_id').value = '';
    openModal('restore_modal');
}
