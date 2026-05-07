const API_BASE = '/api';

function parseErrorMessage(errorData) {
    if (!errorData) return '请求失败';
    
    // FastAPI 验证错误格式：{detail: [{loc, msg, type}, ...]}
    if (Array.isArray(errorData.detail)) {
        return errorData.detail.map(e => e.msg || JSON.stringify(e)).join('; ');
    }
    
    // FastAPI 普通错误格式：{detail: "错误信息"}
    if (typeof errorData.detail === 'string') {
        return errorData.detail;
    }
    
    // 其他对象格式
    if (typeof errorData.detail === 'object' && errorData.detail !== null) {
        return JSON.stringify(errorData.detail);
    }
    
    // 自定义格式
    if (errorData.msg) return errorData.msg;
    if (errorData.message) return errorData.message;
    
    return '请求失败';
}

async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    try {
        const response = await fetch(API_BASE + url, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            const errorMsg = parseErrorMessage(errorData) || `请求失败: ${response.status}`;
            throw new Error(errorMsg);
        }
        const result = await response.json();
        // 自动解包 {code: 200, message: "...", data: ...} 格式
        if (result && result.code !== undefined && result.data !== undefined) {
            // 如果是标准格式，返回 data，但保留 total/page/size 等分页信息
            const unwrapped = result.data;
            if (result.total !== undefined) unwrapped.total = result.total;
            if (result.page !== undefined) unwrapped.page = result.page;
            if (result.size !== undefined) unwrapped.size = result.size;
            if (result.page_size !== undefined) unwrapped.page_size = result.page_size;
            return unwrapped;
        }
        // 如果是 {total: ..., data: [...], page: ..., page_size: ...} 格式，直接返回
        if (result && result.total !== undefined && result.data !== undefined) {
            return result;
        }
        // 其他格式直接返回
        return result;
    } catch (error) {
        // 确保传递给 showToast 的是字符串
        const msg = typeof error === 'string' ? error : (error.message || '未知错误');
        showToast(msg, 'error');
        throw error;
    }
}
