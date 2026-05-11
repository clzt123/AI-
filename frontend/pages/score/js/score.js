let currentPage = 1;
const pageSize = 10;

document.addEventListener('DOMContentLoaded', () => {
    loadScores();
});

async function loadScores() {
    const id = document.getElementById('search_id').value;
    const studentNo = document.getElementById('search_student_no').value;
    const examOrder = document.getElementById('search_exam_order').value;
    let url = `/scores?page=${currentPage}&page_size=${pageSize}`;
    if (id) url += `&id=${id}`;
    if (studentNo) url += `&student_no=${studentNo}`;
    if (examOrder) url += `&exam_order=${examOrder}`;
    try {
        const res = await apiRequest(url);
        const items = Array.isArray(res) ? res : (res.data || []);
        const total = res.total || 0;
        const page = res.page || currentPage;
        const page_size = res.page_size || pageSize;
        renderScores(items);
        renderPagination(page, page_size, total, 'changePage');
    } catch (e) {
        console.error(e);
    }
}

function renderScores(data) {
    const tbody = document.getElementById('score_tbody');
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">暂无数据</td></tr>';
        return;
    }
    tbody.innerHTML = data.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.student_no}</td>
            <td>${s.exam_order}</td>
            <td>${s.score !== null && s.score !== undefined ? s.score : '-'}</td>
            <td class="action-btns">
                <button class="btn btn-warning" onclick="editScore(${s.id})">编辑</button>
                <button class="btn btn-danger" onclick="deleteScore(${s.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function changePage(page) {
    if (page < 1) return;
    currentPage = page;
    loadScores();
}

function searchScores() {
    currentPage = 1;
    loadScores();
}

function openAddModal() {
    document.getElementById('modal_title').textContent = '新增成绩';
    document.getElementById('score_id').value = '';
    document.getElementById('score_form').reset();
    openModal('score_modal');
}

async function editScore(id) {
    try {
        const res = await apiRequest(`/scores?id=${id}&page=1&page_size=1`);
        const items = Array.isArray(res) ? res : (res.data || []);
        if (items && items.length > 0) {
            const s = items[0];
            document.getElementById('modal_title').textContent = '编辑成绩';
            document.getElementById('score_id').value = s.id;
            document.getElementById('form_student_no').value = s.student_no;
            document.getElementById('form_exam_order').value = s.exam_order;
            document.getElementById('form_score').value = s.score !== null && s.score !== undefined ? s.score : '';
            openModal('score_modal');
        }
    } catch (e) {
        console.error(e);
    }
}

async function saveScore() {
    const id = document.getElementById('score_id').value;
    const data = {
        student_no: document.getElementById('form_student_no').value,
        exam_order: parseInt(document.getElementById('form_exam_order').value),
        score: document.getElementById('form_score').value ? parseFloat(document.getElementById('form_score').value) : null
    };
    try {
        if (id) {
            await apiRequest(`/scores/${id}`, 'PUT', { score: data.score });
            showToast('修改成功', 'success');
        } else {
            await apiRequest('/scores', 'POST', data);
            showToast('新增成功', 'success');
        }
        closeModal('score_modal');
        loadScores();
    } catch (e) {
        console.error(e);
    }
}

async function deleteScore(id) {
    if (!confirm('确定要删除该成绩吗？')) return;
    try {
        await apiRequest(`/scores/${id}`, 'DELETE');
        showToast('删除成功', 'success');
        loadScores();
    } catch (e) {
        console.error(e);
    }
}

async function restoreScores() {
    const id = document.getElementById('restore_id').value;
    const studentNo = document.getElementById('restore_student_no').value;
    const examOrder = document.getElementById('restore_exam_order').value;
    let url = `/scores/delete/restore`;
    const params = [];
    if (id) params.push(`id=${id}`);
    if (studentNo) params.push(`student_no=${studentNo}`);
    if (examOrder) params.push(`exam_order=${examOrder}`);
    if (params.length > 0) url += `?${params.join('&')}`;
    try {
        await apiRequest(url, 'PUT');
        showToast('恢复成功', 'success');
        closeModal('restore_modal');
        document.getElementById('restore_id').value = '';
        document.getElementById('restore_student_no').value = '';
        document.getElementById('restore_exam_order').value = '';
        loadScores();
    } catch (e) {
        console.error(e);
    }
}

function openRestoreModal() {
    document.getElementById('restore_id').value = '';
    document.getElementById('restore_student_no').value = '';
    document.getElementById('restore_exam_order').value = '';
    openModal('restore_modal');
}

async function loadAbove80() {
    try {
        const res = await apiRequest('/scores/all-above-80');
        document.getElementById('stats_title').textContent = '所有科目80分以上的学生';
        let html = '<table><thead><tr><th>学号</th><th>姓名</th><th>最低分</th></tr></thead><tbody>';
        const data = Array.isArray(res) ? res : (res.data || []);
        if (!data || data.length === 0) {
            html += '<tr><td colspan="3" style="text-align:center;">暂无数据</td></tr>';
        } else {
            data.forEach(s => {
                html += `<tr><td>${s.student_no}</td><td>${s.student_name}</td><td>${s.score !== null && s.score !== undefined ? s.score : '-'}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}

async function loadMultipleFail() {
    try {
        const res = await apiRequest('/scores/multiple-fail');
        document.getElementById('stats_title').textContent = '不及格次数超过2次的学生';
        let html = '';
        const data = Array.isArray(res) ? res : (res.data || []);
        if (!data || data.length === 0) {
            html = '<p style="text-align:center;">暂无数据</p>';
        } else {
            data.forEach(s => {
                html += `<h4>${s.student_no} - ${s.student_name}</h4>`;
                html += '<table><thead><tr><th>考试序号</th><th>分数</th></tr></thead><tbody>';
                s.fail_records.forEach(r => {
                    html += `<tr><td>${r.exam_order}</td><td>${r.score}</td></tr>`;
                });
                html += '</tbody></table><br>';
            });
        }
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}

async function loadClassAvg() {
    try {
        const res = await apiRequest('/scores/class-avg');
        document.getElementById('stats_title').textContent = '各班级各次考试平均分';
        let html = '<table><thead><tr><th>班级ID</th><th>考试序号</th><th>平均分</th></tr></thead><tbody>';
        const data = Array.isArray(res) ? res : (res.data || []);
        if (!data || data.length === 0) {
            html += '<tr><td colspan="3" style="text-align:center;">暂无数据</td></tr>';
        } else {
            data.forEach(s => {
                html += `<tr><td>${s.class_id}</td><td>${s.exam_order}</td><td>${s.avg_score !== null && s.avg_score !== undefined ? s.avg_score.toFixed(2) : '-'}</td></tr>`;
            });
        }
        html += '</tbody></table>';
        document.getElementById('stats_content').innerHTML = html;
        openModal('stats_modal');
    } catch (e) {
        console.error(e);
    }
}
