(function() {
    var token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login/';
    }
})();

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login/';
}

function getCurrentUser() {
    var userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch (e) {
            return null;
        }
    }
    return null;
}

function getToken() {
    return localStorage.getItem('token');
}

function getAuthHeaders() {
    var token = getToken();
    if (token) {
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        };
    }
    return {
        'Content-Type': 'application/json'
    };
}
