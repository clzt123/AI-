let currentPage = 1;
const pageSize = 10;
let deletedPage = 1;

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
});

async function loadStudents() {
    const name = document.getElementById('search_name').value;
    const classId = document.getElementById('search_class_id').value;
    let url = `/students/check?page=${currentPage}&page_size=${pageSize}`;
    if (name) url += `&student_name=${name}`;
    if (classId) url += `&class_id=${classId}`;
    try {
        const res = await apiRequest(url);
        if (res.code === 200) {
            renderStudents(res.data || []);
            renderPagination(res.page || 1, res.page_size || pageSize, res.total || 0, 'changePage');
        } else {
            showToast(res.msg || '加载失败', 'error');
        }
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
            <td>${formatDate(s.graduation_time)}</td>
            <td>${s.advisor_id || '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editStudent(${s.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteStudent(${s.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function changePage(page) {
    if (page < 1) return;
    currentPage = page;
    loadStudents();
}

function searchStudents() {
    currentPage = 1;
    loadStudents();
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增学生';
    document.getElementById('student_id').value = '';
    document.getElementById('student_form').reset();
    openModal('student_modal');
}

async function editStudent(id) {
    try {
        const res = await apiRequest(`/students/check/${id}`);
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
        document.getElementById('form_graduation_time').value = res.graduation_time ? formatDate(res.graduation_time) : '';
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
        gender: document.getElementById('form_gender').value,
        age: parseInt(document.getElementById('form_age').value),
        native_place: document.getElementById('form_native_place').value,
        graduate_school: document.getElementById('form_graduate_school').value,
        major: document.getElementById('form_major').value,
        education: document.getElementById('form_education').value,
        admission_time: document.getElementById('form_admission_time').value,
        graduation_time: document.getElementById('form_graduation_time').value,
        advisor_id: document.getElementById('form_advisor_id').value ? parseInt(document.getElementById('form_advisor_id').value) : null
    };
    try {
        if (id) {
            await apiRequest(`/students/update/${id}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/students/create', 'POST', data);
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
        await apiRequest(`/students/delete/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadStudents();
    } catch (e) {
        console.error(e);
    }
}

async function restoreStudent(id) {
    try {
        await apiRequest(`/students/restore/${id}`, 'PUT');
        showToast('恢复成功', 'success');
        loadDeletedStudents();
    } catch (e) {
        console.error(e);
    }
}

async function loadDeletedStudents() {
    deletedPage = 1;
    document.getElementById('deleted_search_name').value = '';
    fetchDeletedStudents();
    openModal('deleted_modal');
}

async function fetchDeletedStudents() {
    const name = document.getElementById('deleted_search_name').value;
    let url = `/students/check_is_deleted?page=${deletedPage}&page_size=${pageSize}`;
    if (name) url += `&student_name=${name}`;
    try {
        const res = await apiRequest(url);
        if (res.code === 200) {
            const data = res.data || [];
            renderDeletedStudents(data);
            renderDeletedPagination(res.page || deletedPage, res.page_size || pageSize, res.total || 0);
        } else {
            showToast(res.message || '加载失败', 'error');
        }
    } catch (e) {
        console.error(e);
    }
}

function renderDeletedStudents(data) {
    const tbody = document.getElementById('deleted_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">暂无数据</td></tr>';
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
            <td class="action-btns">
                <button class="btn btn-success" onclick="restoreStudent(${s.id})">恢复</button>
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
    fetchDeletedStudents();
}

function searchDeletedStudents() {
    deletedPage = 1;
    fetchDeletedStudents();
}

async function loadAgeStats() {
    try {
        const res = await apiRequest('/students/age_stats');
        document.getElementById('stats_title').textContent = '超过30岁的学员';
        let html = '<table><thead><tr><th>ID</th><th>学号</th><th>姓名</th><th>年龄</th><th>性别</th></tr></thead><tbody>';
        const data = Array.isArray(res) ? res : (res.data || []);
        if (!data || data.length === 0) {
            html += '<tr><td colspan="5" style="text-align:center;">暂无数据</td></tr>';
        } else {
            data.forEach(s => {
                html += `<tr><td>${s.id}</td><td>${s.student_no}</td><td>${s.student_name}</td><td>${s.age}</td><td>${s.gender || '-'}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}

async function loadGenderStats() {
    try {
        const res = await apiRequest('/students/gender_stats');
        document.getElementById('stats_title').textContent = '班级人数统计';
        let html = '<table><thead><tr><th>班级ID</th><th>总人数</th><th>男生人数</th><th>女生人数</th></tr></thead><tbody>';
        const data = Array.isArray(res) ? res : (res.data || []);
        if (!data || data.length === 0) {
            html += '<tr><td colspan="4" style="text-align:center;">暂无数据</td></tr>';
        } else {
            data.forEach(s => {
                const classId = s.class_id || s.班级 || s['班级'] || '-';
                const totalCount = s.total_count || s.班级总人数 || s['班级总人数'] || 0;
                const maleCount = s.male_count || s.男生人数 || s['男生人数'] || 0;
                const femaleCount = s.female_count || s.女生人数 || s['女生人数'] || 0;
                html += `<tr><td>${classId}</td><td>${totalCount}</td><td>${maleCount}</td><td>${femaleCount}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}
