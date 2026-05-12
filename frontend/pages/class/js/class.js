document.addEventListener('DOMContentLoaded', () => {
    loadClasses();
});

async function loadClasses() {
    try {
        const res = await apiRequest('/classes/all');
        renderClasses(res || []);
    } catch (e) {
        console.error(e);
    }
}

function renderClasses(data) {
    const tbody = document.getElementById('class_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(c => `
        <tr>
            <td>${c.class_id}</td>
            <td>${c.class_name}</td>
            <td>${formatDate(c.start_time)}</td>
            <td>${c.head_teacher_id || '-'}</td>
            <td>${c.lecturer_id || '-'}</td>
            <td>${c.create_time ? new Date(c.create_time).toLocaleString() : '-'}</td>
            <td>${c.update_time ? new Date(c.update_time).toLocaleString() : '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editClass(${c.class_id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteClass(${c.class_id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增班级';
    document.getElementById('class_id').value = '';
    document.getElementById('class_form').reset();
    openModal('class_modal');
}

async function editClass(id) {
    try {
        const res = await apiRequest(`/classes/one/${id}`);
        document.getElementById('modal_title').textContent = '编辑班级';
        document.getElementById('class_id').value = res.class_id;
        document.getElementById('form_class_name').value = res.class_name;
        document.getElementById('form_start_time').value = res.start_time ? formatDate(res.start_time) : '';
        document.getElementById('form_head_teacher_id').value = res.head_teacher_id || '';
        document.getElementById('form_lecturer_id').value = res.lecturer_id || '';
        openModal('class_modal');
    } catch (e) {
        console.error(e);
    }
}

async function saveClass() {
    const id = document.getElementById('class_id').value;
    const data = {
        class_name: document.getElementById('form_class_name').value,
        start_time: document.getElementById('form_start_time').value || null,
        head_teacher_id: document.getElementById('form_head_teacher_id').value ? parseInt(document.getElementById('form_head_teacher_id').value) : null,
        lecturer_id: document.getElementById('form_lecturer_id').value ? parseInt(document.getElementById('form_lecturer_id').value) : null
    };
    try {
        if (id) {
            await apiRequest(`/classes/update/${id}`, 'PUT', data);
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/classes/create', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('class_modal');
        loadClasses();
    } catch (e) {
        console.error(e);
    }
}

async function deleteClass(id) {
    if (!confirm('确定要删除该班级吗？')) return;
    try {
        await apiRequest(`/classes/delete/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadClasses();
    } catch (e) {
        console.error(e);
    }
}

async function restoreClassById() {
    const classId = document.getElementById('restore_class_id').value;
    if (!classId) {
        showToast('请输入班级ID', 'error');
        return;
    }
    try {
        await apiRequest(`/classes/restore/${classId}`, 'POST');
        showToast('恢复成功', 'success');
        closeModal('restore_modal');
        document.getElementById('restore_class_id').value = '';
        loadClasses();
    } catch (e) {
        console.error(e);
    }
}

function openRestoreModal() {
    document.getElementById('restore_class_id').value = '';
    openModal('restore_modal');
}

function loadMonthStats() {
    document.getElementById('stats_month').value = '';
    document.getElementById('stats_title').textContent = '月度统计';
    document.getElementById('stats_content').innerHTML = '';
    openModal('stats_modal');
}

async function fetchMonthStats() {
    const month = document.getElementById('stats_month').value;
    try {
        let url = '/classes/count/month';
        if (month) {
            url += `?month=${month}`;
        }
        const res = await apiRequest(url);
        let html = '<table><thead><tr><th>月份</th><th>班级数</th></tr></thead><tbody>';
        if (!res || res.length === 0) {
            html += '<tr><td colspan="2" style="text-align:center;">暂无数据</td></tr>';
        } else {
            res.forEach(r => {
                html += `<tr><td>${r.month || r.月份 || '-'}</td><td>${r.count || r.班级数 || 0}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_content').innerHTML = html;
    } catch (e) {
        console.error(e);
    }
}

async function searchByLecturer() {
    const lecturerId = document.getElementById('search_lecturer_id').value;
    if (!lecturerId) {
        showToast('请输入授课老师ID', 'error');
        return;
    }
    try {
        const res = await apiRequest(`/classes/class_by_lecturer_id/${lecturerId}`);
        let html = '<table><thead><tr><th>班级ID</th><th>班级名称</th><th>开班时间</th></tr></thead><tbody>';
        if (!res || res.length === 0) {
            html += '<tr><td colspan="3" style="text-align:center;">暂无数据</td></tr>';
        } else {
            res.forEach(c => {
                html += `<tr><td>${c.class_id}</td><td>${c.class_name}</td><td>${formatDate(c.start_time)}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_title').textContent = `老师ID ${lecturerId} 的授课班级`;
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}
