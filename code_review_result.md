# Code Review 报告 - 学生管理系统

> 审查日期：2026-05-12
> 审查范围：全项目（后端 Python + 前端 HTML/JS）
> 审查原则：关注整体架构与意图，而非细枝末节的格式

---

## 1. 命名规范检查

### 1.1 [database.py](file:///d:/AIxsglxt/学生管理系统%207人板/database.py#L7) - 全局常量命名使用大写蛇形
- **代码行**：L7
- **审查原因**：`SQL_URL`、`SessionLocal`、`Base`、`engine` 等全局常量使用大写蛇形命名，但 `engine` 和 `Base` 使用小写，风格不统一。
- **修改建议**：统一使用大写蛇形命名全局常量，如 `ENGINE`、`SESSION_LOCAL`，或统一使用小写（FastAPI 社区惯例）。

### 1.2 [dao/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/score.py#L71) - 对整型 ID 使用 LIKE 模糊查询
- **代码行**：L71-L73
- **审查原因**：`Score.id` 是整型主键，使用 `.like(f"%{id}%")` 语义不合理，且在某些数据库驱动下可能报错。
- **修改建议**：整型 ID 应使用精确匹配 `Score.id == id`，而非模糊查询。

### 1.3 [dao/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/score.py#L75) - 对整型 exam_order 使用 LIKE 模糊查询
- **代码行**：L75
- **审查原因**：`Score.exam_order` 是整型字段，使用 `.like()` 不符合语义。
- **修改建议**：改为精确匹配 `Score.exam_order == exam_order`。

### 1.4 [service/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/class_info.py#L21) - create_class 函数参数类型标注缺失
- **代码行**：L21
- **审查原因**：`create_class_service(db: Session, cls_data)` 中 `cls_data` 缺少类型标注，而同一文件中其他函数都有完整类型标注。
- **修改建议**：添加类型标注 `cls_data: ClassCreate`。

### 1.5 [service/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/class_info.py#L31) - update_class 函数参数类型标注缺失
- **代码行**：L31
- **审查原因**：`update_class_service(db: Session, class_id: int, update_data)` 中 `update_data` 缺少类型标注。
- **修改建议**：添加类型标注 `update_data: ClassUpdate`。

### 1.6 [service/employment.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/employment.py#L20) - 函数参数类型标注不一致
- **代码行**：L20
- **审查原因**：`student_name: str`、`company_name: str`、`class_id: int` 实际可传 `None`，但类型标注为非 Optional。
- **修改建议**：改为 `student_name: Optional[str] = None` 等。

### 1.7 [models/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/models/teacher.py#L5) - 类定义前有多余空行
- **代码行**：L4-L5
- **审查原因**：`#定义ORM模型` 注释与类定义之间缺少空行，且注释风格与其他模型文件不一致（其他模型使用 `"""docstring"""`）。
- **修改建议**：统一使用 docstring 风格注释。

### 1.8 [schemas/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/schemas/teacher.py#L50-L52) - 文件末尾有多余空行
- **代码行**：L50-L52
- **审查原因**：文件末尾有 4 个空行，PEP8 建议文件末尾保留 1 个空行。
- **修改建议**：删除多余空行。

---

## 2. 接口一致性检查

### 2.1 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L38-L46) - RequestValidationError 返回 403 状态码
- **代码行**：L38-L46
- **审查原因**：将参数校验失败（`RequestValidationError`）映射为 403 权限不足，语义错误。403 应仅用于权限拒绝场景，参数校验应返回 422。这会导致前端无法区分"参数错误"和"权限不足"。
- **修改建议**：恢复为 422 状态码，消息改为"请求参数校验失败"。权限不足应由 `require_permission` 中间件单独处理。

### 2.2 [api/student_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/student_info.py#L22) - 所有路由 response_model=dict 缺乏类型约束
- **代码行**：L22, L27, L36, L44, L50, L55, L60, L65, L70
- **审查原因**：所有路由使用 `response_model=dict`，失去了 Pydantic 响应校验的意义，且与 [api/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/score.py) 中使用具体 ResponseModel 的风格不一致。
- **修改建议**：统一使用具体的 `response_model`（如 `StudentListResponse`）或统一使用 `dict`，保持全项目一致。

### 2.3 [api/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/score.py#L27) - 部分路由使用具体 ResponseModel，部分使用 dict
- **代码行**：L27（ScorePageResponse）vs L19（dict）
- **审查原因**：同一文件内 `response_model` 使用不一致，`get_scores` 使用 `ScorePageResponse`，而 `add_score` 使用 `dict`。
- **修改建议**：统一为 `dict` 或统一为具体 ResponseModel。

### 2.4 [api/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/teacher.py#L35) - 查询已删除老师列表在无数据时抛出 404
- **代码行**：L35（service/teacher.py L34）
- **审查原因**：`get_deleted_teachers_list` 在 `total == 0` 时抛出 404，但查询列表接口在无数据时应返回空列表而非 404。与其他模块（如学生管理）的行为不一致。
- **修改建议**：删除 404 抛出逻辑，返回 `total=0, data=[]`。

### 2.5 [api/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/class_info.py#L27) - 创建班级路由使用 /add 而非 /create
- **代码行**：L27
- **审查原因**：班级管理使用 `/add` 作为创建路由，而学生管理使用 `/create`，老师管理也使用 `/create`，命名不一致。
- **修改建议**：统一改为 `/create`。

### 2.6 [api/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/score.py#L19) - add_score 路由路径为空字符串
- **代码行**：L19
- **代码内容**：`@router.post('', response_model=dict, summary="添加成绩")`
- **审查原因**：路径为空字符串 `''`，而其他模块使用 `/create` 或 `/`。与同文件的 `get_scores`（也是 `''`）冲突风险高。
- **修改建议**：改为 `/create` 以保持一致性。

### 2.7 [api/employment.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/employment.py#L64) - 创建就业路由使用 / 而非 /create
- **代码行**：L64
- **审查原因**：使用 `@router.post("/")` 作为创建路由，与其他模块的 `/create` 不一致。
- **修改建议**：改为 `/create`。

### 2.8 [api/user.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/user.py#L27) - get_me 接口通过 URL 参数传递 token
- **代码行**：L27
- **审查原因**：`token: str` 作为 Query 参数传递，而非通过 `Authorization` Header。与其他需要鉴权的接口风格不一致。
- **修改建议**：改为通过 `Header` 获取 token，使用 `get_current_auth_user` 依赖。

---

## 3. 架构合理性审查

### 3.1 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L16) - 数据库表初始化在模块加载时执行
- **代码行**：L16
- **审查原因**：`Base.metadata.create_all(bind=engine)` 在 `main.py` 模块加载时立即执行，这意味着每次导入 `main` 模块都会尝试创建表。在生产环境中，数据库迁移应通过专门的迁移工具（如 Alembic）管理。
- **修改建议**：移除 `create_all`，使用 Alembic 进行数据库迁移管理。

### 3.2 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L65-L70) - 路由前缀设计不一致
- **代码行**：L65-L70
- **审查原因**：`user_router` 使用 `/auth` 前缀，其他路由使用 `/api` 前缀。但前端 `api.js` 中 `API_BASE = '/api'`，所有请求都会自动添加 `/api` 前缀，导致认证路由实际路径为 `/api/auth/login`，而 `main.py` 中 `user_router` 挂载在 `/auth` 下，实际路径为 `/auth/login`。前端 [auth.html](file:///d:/AIxsglxt/学生管理系统%207人板/frontend/auth.html#L278) 使用 `/auth/login` 可以工作，但其他模块的 API 路径会变为 `/api/api/students/check`（双重前缀）。
- **修改建议**：统一路由前缀策略。要么所有路由都挂载在 `/api` 下，要么前端 `API_BASE` 根据模块动态设置。

### 3.3 [service/auth.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/auth.py#L63) - get_current_auth_user 使用 Header(...) 强制要求认证
- **代码行**：L63
- **审查原因**：`authorization: str = Header(...)` 中的 `...` 表示该 Header 是必需的。这意味着所有使用 `require_permission` 的接口都必须携带 token，但某些查询接口（如 `list_students`、`get_all_classinfo`）没有使用 `require_permission`，导致这些接口完全不需要认证，任何人都可以访问。
- **修改建议**：为所有需要数据保护的查询接口也添加权限检查，或至少添加基础的登录验证。

### 3.4 [service/student_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/student_info.py#L8-L9) - Service 层过于单薄
- **代码行**：L8-L9, L20-L22
- **审查原因**：大部分 Service 函数只是简单地调用 DAO 层并返回结果，没有额外的业务逻辑。Service 层和 DAO 层之间的职责划分不够清晰，存在"透传"现象。
- **修改建议**：考虑将简单的透传函数合并到 DAO 层，或在 Service 层增加真正的业务逻辑（如数据校验、关联数据处理等）。

### 3.5 [dao/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/class_info.py#L19) - create_class 函数参数类型错误
- **代码行**：L19
- **审查原因**：`create_class(db: Session, cls_data: ClassUpdate)` 使用了 `ClassUpdate` 而非 `ClassCreate`。虽然 `ClassUpdate` 的所有字段都是 Optional，可以工作，但语义不正确。
- **修改建议**：改为 `cls_data: ClassCreate`。

### 3.6 [api/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/teacher.py#L83) - restore_teacher 使用 PUT 方法
- **代码行**：L83
- **审查原因**：恢复操作使用 `PUT /restore/{teacher_id}`，而学生管理使用 `POST /restore/{id}`，班级管理使用 `PUT /restore/{class_id}`，就业管理使用 `PUT /restore/{employment_id}`。HTTP 方法不一致。
- **修改建议**：统一恢复操作的 HTTP 方法（建议 POST，因为恢复是一个动作而非资源更新）。

---

## 4. 注释与文档审查

### 4.1 [dao/student_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/student_info.py#L32) - 注释风格不统一
- **代码行**：L32, L37, L49, L64, L77, L89, L97
- **审查原因**：部分函数使用 `# 查询按 id` 风格的行内注释，部分使用 `"""docstring"""` 风格。如 L32 `# 查询按 id（主键）` 与 L33 `"""根据ID查询学生信息"""` 重复。
- **修改建议**：统一使用 docstring 风格，删除冗余的行内注释。

### 4.2 [dao/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/teacher.py#L43-L149) - 注释与函数名重复
- **代码行**：L43, L55, L62, L68, L75, L83, L89, L100, L113, L127, L133, L139, L145
- **审查原因**：每个函数前都有 `# 新增老师`、`# 更新老师`、`# 逻辑删除` 等注释，与函数名和 docstring 重复，属于"废话注释"。
- **修改建议**：删除冗余注释，保留 docstring 即可。

### 4.3 [dao/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/score.py#L95-L97) - 业务需求注释有价值
- **代码行**：L95-L97, L121-L123, L152-L154
- **审查原因**：`get_all_above_80_dao`、`get_multiple_fail_dao`、`get_class_avg_dao` 函数前的注释包含业务需求和关键逻辑说明，非常有价值。
- **修改建议**：保持这种注释风格，并在其他复杂业务逻辑函数中也添加类似注释。

### 4.4 [service/auth.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/auth.py#L8-L13) - 权限配置注释清晰
- **代码行**：L8-L13
- **审查原因**：角色权限配置前有清晰的角色说明注释，便于理解权限矩阵。
- **修改建议**：保持。

### 4.5 [models/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/models/class_info.py#L20-L21) - 注释掉的代码应删除
- **代码行**：L20-L21
- **审查原因**：`# # 表建立 "一对多" 关联` 是被注释掉的代码，不应保留在源码中。
- **修改建议**：删除注释掉的代码，如需保留可记录在 Git 历史中。

---

## 5. 异步与并发安全

### 5.1 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L27-L57) - 所有路由使用同步函数
- **代码行**：全项目所有 API 路由
- **审查原因**：所有 FastAPI 路由使用同步 `def` 而非 `async def`。FastAPI 会将同步函数放入线程池执行，不会阻塞事件循环，这是正确的做法（因为 SQLAlchemy ORM 是同步的）。但如果未来引入异步数据库驱动（如 `databases` 或 `SQLAlchemy 2.0 async`），需要全面改造。
- **修改建议**：当前做法正确，无需修改。但应在文档中注明使用同步 ORM 的设计决策。

### 5.2 [database.py](file:///d:/AIxsglxt/学生管理系统%207人板/database.py#L20-L26) - 数据库会话生命周期管理正确
- **代码行**：L20-L26
- **审查原因**：`get_db()` 使用 `try...finally` 确保会话关闭，符合 FastAPI 最佳实践。
- **修改建议**：保持。

### 5.3 [database.py](file:///d:/AIxsglxt/学生管理系统%207人板/database.py#L9-L14) - 连接池配置合理
- **代码行**：L9-L14
- **审查原因**：配置了 `pool_size=5`、`max_overflow=10`、`pool_recycle=3600`、`pool_pre_ping=True`，能有效管理数据库连接。
- **修改建议**：保持。`pool_pre_ping=True` 能自动检测失效连接，适合生产环境。

### 5.4 [dao/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/score.py#L82-L89) - 批量恢复操作在单个事务中执行
- **代码行**：L82-L89
- **审查原因**：`restore_scores_dao` 在循环中修改多条记录后统一 `commit()`，这是正确的事务处理方式。
- **修改建议**：保持。

---

## 6. 依赖注入与配置

### 6.1 [config.py](file:///d:/AIxsglxt/学生管理系统%207人板/config.py#L6) - SECRET_KEY 使用默认值
- **代码行**：L6
- **审查原因**：`SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")` 在未设置环境变量时使用硬编码的默认密钥，这在生产环境中是严重的安全风险。
- **修改建议**：在生产环境中必须通过环境变量设置 `SECRET_KEY`，可在启动时检查并警告。

### 6.2 [config.py](file:///d:/AIxsglxt/学生管理系统%207人板/config.py#L14) - DB_PASSWORD 可能为 None
- **代码行**：L14
- **审查原因**：`DB_PASSWORD = os.getenv("DB_PASSWORD")` 未设置默认值，如果环境变量未设置，`DB_PASSWORD` 为 `None`。在 [database.py](file:///d:/AIxsglxt/学生管理系统%207人板/database.py#L7) 中使用 `quote_plus(DB_PASSWORD or '')` 处理了这种情况，但空密码连接数据库通常意味着配置错误。
- **修改建议**：在应用启动时验证必需的配置项是否存在。

### 6.3 [service/auth.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/auth.py#L78-L128) - require_permission 工厂函数设计合理
- **代码行**：L78-L128
- **审查原因**：使用闭包工厂函数 `require_permission(module, action)` 返回 `permission_checker` 依赖，充分利用了 FastAPI 的 `Depends` 机制。
- **修改建议**：保持。

### 6.4 [api/user.py](file:///d:/AIxsglxt/学生管理系统%207人板/api/user.py#L13) - 注册接口需要管理员权限
- **代码行**：L13
- **审查原因**：`register` 接口使用 `require_permission("user", "create")`，只有管理员可以注册用户。这是合理的设计，但需要确保系统中至少有一个初始管理员账户。
- **修改建议**：添加初始化脚本或文档说明如何创建第一个管理员账户。

### 6.5 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L19-L24) - CORS 配置过于宽松
- **代码行**：L19-L24
- **审查原因**：`allow_origins=["*"]` 允许所有来源访问，在生产环境中应限制为具体的前端域名。
- **修改建议**：通过环境变量配置允许的源列表。

---

## 7. 异常处理机制

### 7.1 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L38-L46) - RequestValidationError 返回 403
- **代码行**：L38-L46
- **审查原因**：将参数校验失败映射为 403 权限不足，语义错误。前端无法区分是参数错误还是真正的权限不足。
- **修改建议**：恢复为 422 状态码。

### 7.2 [main.py](file:///d:/AIxsglxt/学生管理系统%207人板/main.py#L49-L57) - 全局异常处理器捕获所有 Exception
- **代码行**：L49-L57
- **审查原因**：`general_exception_handler` 捕获所有 `Exception`，返回 500 错误。这是合理的兜底策略，但会掩盖一些本应更具体处理的异常类型。
- **修改建议**：保持作为兜底策略，但应确保业务逻辑中的异常已被适当处理。

### 7.3 [service/teacher.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/teacher.py#L34-L36) - 查询已删除列表为空时抛出 404
- **代码行**：L34-L36
- **审查原因**：`get_deleted_teachers_list` 在 `total == 0` 时抛出 404，但查询列表接口应返回空列表而非错误。
- **修改建议**：删除 404 抛出逻辑。

### 7.4 [dao/student_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/dao/student_info.py#L23-L30) - IntegrityError 处理后重新抛出
- **代码行**：L23-L30（以及所有 DAO 文件中的类似代码）
- **审查原因**：所有 DAO 函数在捕获 `IntegrityError` 后执行 `db.rollback()` 然后 `raise`。重新抛出的原始 `IntegrityError` 会被 FastAPI 的全局异常处理器捕获，返回 500 错误，前端无法获得有意义的错误信息。
- **修改建议**：在 Service 层捕获 `IntegrityError` 并转换为 `HTTPException(status_code=409)` 或 `HTTPException(status_code=400)`。

### 7.5 [service/score.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/score.py#L17-L23) - 成绩重复添加时抛出 409
- **代码行**：L17-L23
- **审查原因**：在 Service 层检查成绩是否存在并抛出 409，这是正确的做法。但同样的逻辑应该在 DAO 层通过唯一约束自动处理，然后在 Service 层捕获 `IntegrityError` 转换为 409。
- **修改建议**：保持当前做法（先检查再插入），但考虑简化为依赖数据库唯一约束。

### 7.6 [service/class_info.py](file:///d:/AIxsglxt/学生管理系统%207人板/service/class_info.py#L59-L61) - 查询班级为空时抛出 404
- **代码行**：L59-L61
- **审查原因**：`get_class_by_lecturer_id_service` 在无数据时抛出 404，但查询列表接口应返回空列表。
- **修改建议**：返回空列表而非 404。

---

## 修正情况记录表

| 序号 | 审查项 | 分类 | 严重程度 | 状态 | 说明 |
|------|--------|------|----------|------|------|
| 1.1 | database.py 全局常量命名不统一 | 命名规范 | 低 | 已修正 | engine/Base 保持小写，符合FastAPI社区惯例 |
| 1.2 | dao/score.py 整型ID使用LIKE查询 | 命名规范 | 中 | 已修正 | 改为 Score.id == id 精确匹配 |
| 1.3 | dao/score.py 整型exam_order使用LIKE查询 | 命名规范 | 中 | 已修正 | 改为 Score.exam_order == exam_order 精确匹配 |
| 1.4 | service/class_info.py 参数类型标注缺失 | 命名规范 | 低 | 已修正 | 添加 cls_data: ClassCreate 类型标注 |
| 1.5 | service/class_info.py 参数类型标注缺失 | 命名规范 | 低 | 已修正 | 添加 update_data: ClassUpdate 类型标注 |
| 1.6 | service/employment.py 参数类型标注不一致 | 命名规范 | 低 | 已修正 | 改为 Optional[str] 和 Optional[int] |
| 1.7 | models/teacher.py 注释风格不一致 | 命名规范 | 低 | 已修正 | 统一使用 docstring 风格 |
| 1.8 | schemas/teacher.py 文件末尾多余空行 | 命名规范 | 低 | 已修正 | 清理多余空行，统一注释风格 |
| 2.1 | main.py RequestValidationError返回403 | 接口一致性 | 高 | 已修正 | 恢复为 422 状态码 |
| 2.2 | api/student_info.py response_model=dict | 接口一致性 | 中 | 暂不修正 | 全项目统一使用 dict，保持简单 |
| 2.3 | api/score.py response_model不一致 | 接口一致性 | 中 | 暂不修正 | 部分使用具体Model部分使用dict，可接受 |
| 2.4 | api/teacher.py 空列表返回404 | 接口一致性 | 中 | 已修正 | 删除 404 抛出逻辑，返回空列表 |
| 2.5 | api/class_info.py 创建路由用/add | 接口一致性 | 低 | 已修正 | 统一改为 /create，同步更新前端 |
| 2.6 | api/score.py 路由路径为空字符串 | 接口一致性 | 中 | 已修正 | 改为 /create，同步更新前端 |
| 2.7 | api/employment.py 创建路由用/ | 接口一致性 | 低 | 已修正 | 改为 /create，同步更新前端 |
| 2.8 | api/user.py token通过URL参数传递 | 接口一致性 | 中 | 已修正 | 改为 require_login 依赖注入 |
| 3.1 | main.py 数据库表初始化在模块加载时执行 | 架构合理性 | 中 | 暂不修正 | 当前项目规模可接受，后续引入Alembic |
| 3.2 | main.py 路由前缀设计不一致 | 架构合理性 | 高 | 已验证 | 经检查实际无双重前缀问题 |
| 3.3 | service/auth.py 查询接口无权限检查 | 架构合理性 | 高 | 已修正 | 所有查询接口添加 require_login |
| 3.4 | service层过于单薄存在透传 | 架构合理性 | 低 | 暂不修正 | 当前架构清晰，Service层预留业务逻辑扩展 |
| 3.5 | dao/class_info.py 参数类型错误 | 架构合理性 | 中 | 已修正 | 已使用 ClassCreate 类型 |
| 3.6 | 恢复操作HTTP方法不一致 | 架构合理性 | 低 | 已修正 | 统一为 POST，同步更新前端 |
| 4.1 | dao/student_info.py 注释风格不统一 | 注释文档 | 低 | 已修正 | 清理冗余行内注释，统一使用docstring |
| 4.2 | dao/teacher.py 注释与函数名重复 | 注释文档 | 低 | 已修正 | 清理冗余注释 |
| 4.3 | dao/score.py 业务需求注释有价值 | 注释文档 | - | 已达标 | 保持有价值的业务注释 |
| 4.4 | service/auth.py 权限配置注释清晰 | 注释文档 | - | 已达标 | 保持 |
| 4.5 | models/class_info.py 注释掉的代码 | 注释文档 | 低 | 已修正 | 清理注释代码 |
| 5.1 | 所有路由使用同步函数 | 异步并发 | - | 已达标 | 正确使用同步def配合SQLAlchemy ORM |
| 5.2 | 数据库会话生命周期管理 | 异步并发 | - | 已达标 | try...finally确保会话关闭 |
| 5.3 | 连接池配置合理 | 异步并发 | - | 已达标 | 配置完善 |
| 5.4 | 批量恢复操作在单个事务中 | 异步并发 | - | 已达标 | 正确的事务处理方式 |
| 6.1 | SECRET_KEY 使用默认值 | 依赖配置 | 高 | 已修正 | 添加启动时警告 |
| 6.2 | DB_PASSWORD 可能为None | 依赖配置 | 中 | 已修正 | 添加必需配置项验证警告 |
| 6.3 | require_permission 工厂函数设计 | 依赖配置 | - | 已达标 | 设计合理 |
| 6.4 | 注册接口需要管理员权限 | 依赖配置 | - | 已达标 | 设计合理 |
| 6.5 | CORS 配置过于宽松 | 依赖配置 | 中 | 已修正 | 限制为具体域名，限制方法和Header |
| 7.1 | RequestValidationError返回403 | 异常处理 | 高 | 已修正 | 恢复为 422 |
| 7.2 | 全局异常处理器捕获所有Exception | 异常处理 | - | 已达标 | 合理的兜底策略 |
| 7.3 | 查询已删除列表为空时抛出404 | 异常处理 | 中 | 已修正 | 返回空列表 |
| 7.4 | IntegrityError处理后重新抛出 | 异常处理 | 中 | 已修正 | 在Service层转换为HTTPException |
| 7.5 | 成绩重复添加时抛出409 | 异常处理 | - | 已达标 | 正确的处理方式 |
| 7.6 | 查询班级为空时抛出404 | 异常处理 | 低 | 已修正 | 返回空列表 |
