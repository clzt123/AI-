# Dify HTTP Request Service

用于对接 Dify 的 Python 后端服务，提供数据库 CRUD 操作和动态 SQL 查询功能。

## 技术栈

- **Web 框架**: FastAPI
- **ORM**: SQLAlchemy 2.0+
- **数据库**: MySQL (pymysql/mysqlclient)
- **数据校验**: Pydantic V2
- **配置管理**: python-dotenv / pydantic-settings

## 项目结构

```
.
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── .env.example            # 环境变量模板
├── api/                    # 路由接口层
│   └── routes.py           # API 路由定义
├── core/                   # 核心配置层
│   ├── config.py           # 配置读取
│   └── database.py         # 数据库连接与会话管理
├── dao/                    # 数据访问层
│   └── base_dao.py         # 通用 DAO 逻辑
├── model/                  # 业务逻辑层
│   └── base_service.py     # 服务层封装
├── schema/                 # 数据模型层
│   ├── models.py           # SQLAlchemy 表定义
│   └── schemas.py          # Pydantic 校验模型
└── utils/                  # 工具类
    └── sql_validator.py    # SQL 安全校验
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并修改数据库配置：

```env
DATABASE_URL=mysql+mysqldb://username:password@localhost:3306/database_name
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false
```

### 3. 启动服务

```bash
python main.py
```

服务启动后访问 `http://localhost:8000/docs` 查看 Swagger API 文档。

## API 接口

### 通用 CRUD

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/osa/{table_name}/create` | 创建记录（仅插入非空字段） |
| PATCH | `/api/v1/osa/{table_name}/{id}` | 更新记录（仅更新非空字段） |
| DELETE | `/api/v1/osa/{table_name}/{id}` | 删除记录 |
| GET | `/api/v1/osa/{table_name}/{id}` | 根据ID查询记录 |

### 动态 SQL 查询（核心功能）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/osa/query` | 执行动态 SQL 查询 |

**请求示例**：
```json
{
    "sql": "SELECT * FROM student_psych_profile WHERE emotion_score > 80"
}
```

**响应示例**：
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "student_id": 1001,
            "latest_emotion_tag": "开心",
            "emotion_score": 95,
            "last_interaction_time": "2024-01-15T10:30:00",
            "emotion_history": "开心,愉悦,平静",
            "update_time": "2024-01-15T10:30:00"
        }
    ]
}
```

### SQL 安全校验

为防止 Dify 生成危险 SQL 语句，系统会自动校验：

- SQL 语句必须以 `SELECT` 开头
- 禁止包含危险关键字：`DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, `CREATE` 等

校验失败时返回 400 错误：

```json
{
    "detail": "SQL 语句包含危险操作关键字: DROP"
}
```

## 数据库模型

### 1. student_admin_service（学生行政服务表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学生ID |
| service_type | VARCHAR(100) | 服务类型 |
| start_time | DATETIME | 开始时间 |
| end_time | DATETIME | 结束时间 |
| reason | VARCHAR(100) | 原因 |
| status | VARCHAR(100) | 状态（默认'待审批'） |
| approver_id | INTEGER | 审批人ID |
| related_academic_id | INTEGER | 关联学业ID |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### 2. student_psych_profile（学生心理画像表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学生ID（唯一） |
| latest_emotion_tag | VARCHAR(100) | 最新情绪标签 |
| emotion_score | INTEGER | 情绪评分 |
| last_interaction_time | DATETIME | 最近互动时间 |
| emotion_history | VARCHAR(100) | 情绪历史 |
| update_time | DATETIME | 更新时间 |

### 3. student_psych_alert（学生心理预警表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学生ID |
| trigger_reason | VARCHAR(100) | 触发原因 |
| risk_level | VARCHAR(100) | 风险等级 |
| status | VARCHAR(100) | 状态（默认'未处理'） |
| teacher_id | INTEGER | 负责教师ID |
| create_time | DATETIME | 创建时间 |

### 4. student_feedback_ticket（学生反馈工单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学生ID |
| content | VARCHAR(100) | 内容 |
| detail | VARCHAR(100) | 详情 |
| status | VARCHAR(100) | 状态（默认'待处理'） |
| solution | VARCHAR(100) | 解决方案 |
| is_notified | INTEGER | 是否已通知（默认0） |
| create_time | DATETIME | 创建时间 |
| update_time | DATETIME | 更新时间 |

### 5. study_abroad_progress（留学申请进度追踪表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| student_id | INTEGER | 学生ID |
| service_stage | VARCHAR(50) | 服务阶段（文书/申请/签证） |
| current_status | VARCHAR(100) | 当前具体状态（如：初稿撰写中） |
| detail_info | TEXT | 详细备注（如：文案老师正在润色PS第二段） |
| last_update_time | DATETIME | 最后更新时间 |
| update_by | INTEGER | 最后更新人（顾问ID） |

## 使用示例

### 创建记录

```bash
curl -X POST "http://localhost:8000/api/v1/osa/student_psych_profile/create" \
     -H "Content-Type: application/json" \
     -d '{"student_id": 1001, "latest_emotion_tag": "开心", "emotion_score": 85}'
```

### 更新记录

```bash
curl -X PATCH "http://localhost:8000/api/v1/osa/student_psych_profile/1" \
     -H "Content-Type: application/json" \
     -d '{"emotion_score": 90}'
```

### 删除记录

```bash
curl -X DELETE "http://localhost:8000/api/v1/osa/student_psych_profile/1"
```

### 执行动态 SQL

```bash
curl -X POST "http://localhost:8000/api/v1/osa/query" \
     -H "Content-Type: application/json" \
     -d '{"sql": "SELECT * FROM student_psych_profile WHERE emotion_score > 80"}'
```

## 开发说明

### Clean Architecture 分层

```
api/routes.py      → 路由接口层（接收请求、调用服务、返回响应）
model/             → 业务逻辑层（复杂事务处理）
dao/               → 数据访问层（直接操作数据库）
schema/            → 数据模型层（SQLAlchemy ORM & Pydantic）
```

### 代码规范

- 遵循 PEP 8
- 使用 Type Hints
- Pydantic V2 配置：`model_config = ConfigDict(from_attributes=True)`
