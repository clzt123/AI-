# 学生管理系统

基于 FastAPI + SQLAlchemy + MySQL 的学生管理系统，包含学生管理、成绩管理、就业管理、老师管理、班级管理等多个模块，前端使用原生 HTML/CSS/JavaScript 构建。

## 技术栈

- **后端**: Python 3.x, FastAPI, SQLAlchemy, PyMySQL
- **数据库**: MySQL
- **前端**: HTML5, CSS3, Vanilla JavaScript (无框架)
- **服务器**: Uvicorn (ASGI)

## 项目结构

```
学生管理系统 7人板/
├── api/                    # API 路由层
│   ├── student_info.py     # 学生管理接口
│   ├── student_api.py      # 学生管理2接口
│   ├── score.py            # 成绩管理接口
│   ├── teacher.py          # 老师管理接口
│   ├── class_info_api.py   # 班级管理接口
│   ├── stu_employment.py   # 学生就业管理接口
│   ── employee1.py        # 就业模块接口
├── service/                # 业务逻辑层
├── dao/                    # 数据访问层
├── models/                 # 数据库模型层
├── schemas/                # Pydantic 数据校验模型
├── frontend/               # 前端页面
│   ├── index.html          # 首页
│   ├── css/common.css      # 公共样式
│   ├── js/                 # 公共JS
│   │   ├── api.js          # API请求封装
│   │   └── common.js       # 公共工具函数
│   └── pages/              # 各模块页面
│       ├── student/        # 学生管理
│       ├── student2/       # 学生管理2
│       ├── score/          # 成绩管理
│       ├── teacher/        # 老师管理
│       ├── class/          # 班级管理
│       ├── employment/     # 就业模块
│       └── employment2/    # 学生就业管理
├── database.py             # 数据库连接配置
├── main.py                 # FastAPI 应用入口
├── .env                    # 环境变量配置（需自行创建）
└── .gitignore              # Git 忽略文件
```

## 架构设计

项目采用经典的三层架构：

- **API层** (`api/`): 负责路由定义、请求参数校验、响应格式化
- **Service层** (`service/`): 负责业务逻辑处理、数据校验
- **DAO层** (`dao/`): 负责数据库 CRUD 操作

## 功能模块

| 模块 | 功能 |
|------|------|
| 学生管理 | 学生信息的增删改查、分页查询、逻辑删除与恢复、年龄统计、性别统计 |
| 学生管理2 | 学生信息的增删改查、批量查询 |
| 成绩管理 | 成绩的增删改查、综合查询、80分以上统计、不及格统计、班级平均分统计 |
| 老师管理 | 老师信息的增删改查、分页查询、逻辑删除与恢复、性别统计 |
| 班级管理 | 班级信息的增删改查、逻辑删除与恢复、月度统计、按讲师查询 |
| 就业模块 | 就业信息的增删改查、分页查询、逻辑删除与恢复、就业统计 |
| 学生就业管理 | 学生就业信息的增删改查、按学号/班级/公司/薪资查询 |

## 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- pip

### 2. 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv pydantic
```

### 3. 配置环境变量

复制 `.env` 文件并修改数据库连接信息：

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=student
DB_POOL_SIZE=5

APP_HOST=0.0.0.0
APP_PORT=8000
```

### 4. 创建数据库

```sql
CREATE DATABASE student CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

### 6. 访问前端

打开浏览器访问 `http://localhost:8000/`

## API 文档

启动服务后，访问以下地址查看自动生成的 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 注意事项

- `.env` 文件包含敏感信息，已加入 `.gitignore`，请勿提交到版本控制系统
- 首次运行会自动创建数据库表结构
- 所有删除操作均为逻辑删除，数据可通过恢复功能找回
