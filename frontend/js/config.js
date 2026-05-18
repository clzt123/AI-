
// Dify智能体配置
const AGENT_CONFIG = {
    // 客服智能体
    customer: {
        appId: 'G3Tsuspuu40ayj52',
        baseUrl: 'http://192.168.110.49:80',
        name: '客服智能体',
        title: '在线客服'
    },
    // 企业智能体
    employee: {
        appId: '7looxs6HP9YBSnK8',
        baseUrl: 'http://192.168.110.60:80',
        name: '企业智能体',
        title: '企业助手'
    },
    // 学生智能体
    student: {
        appId: 'EE4fkzwDP1FPz5ux',
        baseUrl: 'http://192.168.110.48:80',
        name: '学生智能体',
        title: '学生助手'
    }
};

// 后端API地址（修改为8080端口）
const API_BASE_URL = 'http://localhost:8080/api';

// 存储用户信息的key
const USER_INFO_KEY = 'dify_user_info';
