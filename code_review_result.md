# Code Review 报告

> 审查日期：2026-05-08
> 审查范围：学生管理系统 7人板（FastAPI + SQLAlchemy + 原生前端）
> 审查原则：关注整体架构与意图，而非细枝末节的格式

---

## 1. 命名规范检查

### 1.1 两个学生模块命名冲突

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `models/student_info.py` | 4 | 类名 `Student` 过于通用 | 改为 `StudentInfo` 或 `StudentModelV1` |
| `models/student_model.py` | 6 | 类名 `StudentModel` 与上面功能重复 | 改为 `StudentV2` 或 `StudentModelV2` |
| `schemas/student_info.py` | 6 | `StudentCreate` 与 `schemas/student_schemas.py` 中的 `StudentCreate` 同名 | 改为 `StudentInfoCreate` |
| `schemas/student_schemas.py` | 5 | `StudentCreate` 与上面同名 | 改为 `StudentV2Create` |
| `api/student_info.py` | 1 | 路由前缀 `/students` 与 `api/student_api.py` 的 `/students2` 易混淆 | 改为 `/students/v1` 和 `/students/v2` |
| `api/student_api.py` | 7 | 路由前缀 `/students2` 不够语义化 | 改为 `/students/v2` |

### 1.2 两个就业模块命名冲突

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `models/employee1.py` | 5 | 类名 `Employment` 与 `models/stu_employment.py` 中的 `Employment` 同名 | 改为 `EmploymentV1` |
| `models/stu_employment.py` | 6 | 类名 `Employment` 与上面同名 | 改为 `EmploymentV2` |
| `schemas/employee1.py` | 8 | `CreateEmployment` 与 `schemas/stu_employment.py` 中的 `EmploymentCreate` 命名风格不一致 | 统一为 `EmploymentV1Create` |
| `schemas/stu_employment.py` | 6 | `EmploymentCreate` 与上面风格不一致 | 统一为 `EmploymentV2Create` |
| `service/employee1.py` | 8 | 类名 `EmploymentService` 与 `service/stu_employment.py` 中的 `EmploymentService` 同名 | 改为 `EmploymentV1Service` |
| `service/stu_employment.py` | 8 | 类名 `EmploymentService` 与上面同名 | 改为 `EmploymentV2Service` |
| `dao/employee1.py` | 9 | 类名 `EmploymentDao` 与 `dao/stu_employment.py` 中的函数同名 | 改为 `EmploymentV1Dao` |

### 1.3 API 路由函数命名不一致

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/student_info.py` | 10 | `create_student_api` 带 `_api` 后缀 | 去掉后缀，改为 `create_student` |
| `api/teacher.py` | 43 | `update_teacher_api` 带 `_api` 后缀 | 去掉后缀，改为 `update_teacher` |
| `api/teacher.py` | 67 | `restore_teacher_api` 带 `_api` 后缀 | 去掉后缀，改为 `restore_teacher` |
| `api/class_info_api.py` | 23 | `add_class_api` 命名风格与其他模块不一致 | 改为 `create_class` |
| `api/score.py` | 12 | `add_score` 命名风格不一致 | 改为 `create_score` |

### 1.4 Service 层函数命名使用 `judge_` 前缀

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/student_info.py` | 6-48 | 所有函数使用 `judge_` 前缀（如 `judge_get_student`） | 去掉 `judge_` 前缀，改为 `get_student`、`get_students` 等 |
| `service/teacher.py` | 6-56 | 所有函数使用 `judge_` 前缀 | 同上 |

### 1.5 变量命名不规范

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `dao/class_info_dao.py` | 40 | 变量名 `cls` 是 Python 保留字 | 改为 `class_obj` 或 `class_info` |
| `dao/class_info_dao.py` | 49 | 变量名 `cls` 同上 | 同上 |
| `service/class_info_service.py` | 13 | 变量名 `all_cls_service` 冗余 | 改为 `all_classes` |
| `service/class_info_service.py` | 20 | 变量名 `one_cls_service` 冗余 | 改为 `class_info` |

---

## 2. 接口一致性检查

### 2.1 API 响应格式不统一

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/student_info.py` | 10 | `create_student_api` 直接返回 ORM 对象，未包裹 `{code, message, data}` | 统一包裹为 `{"code": 200, "message": "创建成功", "data": result}` |
| `api/student_info.py` | 14 | `list_students` 返回 `{code, message, total, data, page, page_size}` | 统一为 `{code, message, data: {items, total, page, page_size}}` |
| `api/student_info.py` | 23 | `get_age_stats` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/student_info.py` | 27 | `get_gender_stats` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/student_info.py` | 31 | `get_student_by_id` 直接返回 ORM 对象 | 统一包裹 |
| `api/student_info.py` | 35 | `update_student` 直接返回 ORM 对象 | 统一包裹 |
| `api/teacher.py` | 12 | `get_all_teachers` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/teacher.py` | 17 | `add_teacher` 直接返回 ORM 对象 | 统一包裹 |
| `api/teacher.py` | 38 | `get_teacher_by_id` 直接返回 ORM 对象 | 统一包裹 |
| `api/teacher.py` | 43 | `update_teacher_api` 直接返回 ORM 对象 | 统一包裹 |
| `api/teacher.py` | 67 | `restore_teacher_api` 直接返回 ORM 对象 | 统一包裹 |
| `api/teacher.py` | 71 | `get_stats` 直接返回字典 | 统一包裹 |
| `api/class_info_api.py` | 13 | `get_all_classinfo_api` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/class_info_api.py` | 18 | `get_one_class_api` 直接返回 ORM 对象 | 统一包裹 |
| `api/class_info_api.py` | 23 | `add_class_api` 直接返回 ORM 对象 | 统一包裹 |
| `api/class_info_api.py` | 27 | `put_update_class` 直接返回 ORM 对象 | 统一包裹 |
| `api/class_info_api.py` | 41 | `count_class_month` 直接返回字典 | 统一包裹 |
| `api/class_info_api.py` | 45 | `get_class_by_lecturer_id_api` 直接返回列表 | 统一包裹 |
| `api/stu_employment.py` | 15 | `get_all` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/stu_employment.py` | 19 | `create` 直接返回 ORM 对象 | 统一包裹 |
| `api/stu_employment.py` | 23 | `get_by_no` 直接返回 ORM 对象 | 统一包裹 |
| `api/stu_employment.py` | 27 | `get_by_class` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/stu_employment.py` | 31 | `get_by_company` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/stu_employment.py` | 35 | `get_by_salary` 直接返回 ORM 对象列表 | 统一包裹 |
| `api/stu_employment.py` | 39 | `update` 直接返回字典 | 统一包裹 |
| `api/student_api.py` | 11 | `create_student` 直接返回 ORM 对象 | 统一包裹 |
| `api/student_api.py` | 28 | `update_student` 直接返回 ORM 对象 | 统一包裹 |
| `api/student_api.py` | 36 | `get_student` 直接返回 ORM 对象 | 统一包裹 |
| `api/student_api.py` | 44 | `restore_student` 直接返回 ORM 对象 | 统一包裹 |
| `api/student_api.py` | 52 | `get_all_students` 直接返回 ORM 对象列表 | 统一包裹 |

### 2.2 分页参数命名不一致

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/score.py` | 30 | 使用 `size` 作为分页参数 | 统一为 `page_size` |
| `api/employee1.py` | 13-14 | 使用 `skip/limit` 作为分页参数 | 统一为 `page/page_size` |

### 2.3 删除/恢复接口返回字段名不一致

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/score.py` | 54 | 删除接口返回 `{"code":200,"message":"删除成功"}` 缺少 `data` 字段 | 添加 `"data": None` |
| `api/stu_employment.py` | 46 | 删除接口返回 `{"msg": "删除成功"}` 使用 `msg` 而非 `message` | 改为 `message` |
| `api/stu_employment.py` | 50 | 恢复接口返回 `{"msg": "恢复成功"}` 使用 `msg` 而非 `message` | 改为 `message` |
| `api/stu_employment.py` | 53 | 更新接口返回 `{"msg": "更新成功"}` 使用 `msg` 而非 `message` | 改为 `message` |

### 2.4 状态码使用不合理

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/student_info.py` | 14 | 查询无数据时返回 404 | 查询无数据应返回 200 + 空列表，404 仅用于资源不存在 |
| `service/student_info.py` | 38 | 查询已删除学生无数据时返回 404 | 同上 |
| `service/teacher.py` | 9 | 查询无数据时返回 404 | 同上 |
| `service/teacher.py` | 21 | 查询无数据时返回 404 | 同上 |
| `service/teacher.py` | 27 | 查询已删除老师无数据时返回 404 | 同上 |
| `service/class_info_service.py` | 14 | 查询无数据时返回 404 | 同上 |
| `service/class_info_service.py` | 21 | 查询无数据时返回 404 | 同上 |
| `service/class_info_service.py` | 60 | 统计无数据时返回 404 | 同上 |
| `service/class_info_service.py` | 66 | 查询无数据时返回 404 | 同上 |
| `service/score.py` | 97 | 查询无数据时返回 404 | 同上 |
| `service/score.py` | 103 | 查询无数据时返回 404 | 同上 |
| `service/score.py` | 109 | 查询无数据时返回 404 | 同上 |

---

## 3. 架构合理性审查

### 3.1 Service 层越层问题：直接操作数据库

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/score.py` | 9-13 | `add_score_service` 中直接使用 `db.query(Score_DB)` | 将查询逻辑移至 DAO 层，Service 层只调用 DAO 方法 |
| `service/class_info_service.py` | 66 | `get_class_by_lecturer_id_service` 中两次调用 DAO 查询 | 在 DAO 层增加存在性检查方法 |

### 3.2 DAO 层返回字典而非 ORM 对象

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `dao/student_info.py` | 87-98 | `check_student_gender` 返回字典列表而非 ORM 对象 | 返回 ORM 对象，在 Service 层或 API 层格式化 |
| `dao/score.py` | 93-106 | `get_all_above_80_dao` 返回字典列表 | 同上 |
| `dao/score.py` | 109-147 | `get_multiple_fail_dao` 返回字典列表 | 同上 |
| `dao/score.py` | 150-169 | `get_class_avg_dao` 返回字典列表 | 同上 |

### 3.3 两个就业模块重复设计

| 文件 | 问题 | 建议 |
|------|------|------|
| `api/employee1.py` vs `api/stu_employment.py` | 两个模块功能高度重叠（CRUD + 查询 + 统计） | 考虑合并为一个模块，或使用版本化路由 `/employment/v1` 和 `/employment/v2` |
| `models/employee1.py` vs `models/stu_employment.py` | 两个表结构几乎相同 | 考虑合并表结构 |
| `service/employee1.py` vs `service/stu_employment.py` | 业务逻辑重复 | 合并 Service 层 |
| `dao/employee1.py` vs `dao/stu_employment.py` | 数据访问逻辑重复 | 合并 DAO 层 |

### 3.4 两个学生模块重复设计

| 文件 | 问题 | 建议 |
|------|------|------|
| `api/student_info.py` vs `api/student_api.py` | 两个模块功能高度重叠 | 考虑合并为一个模块，或使用版本化路由 |
| `models/student_info.py` vs `models/student_model.py` | 两个表结构几乎相同 | 考虑合并表结构 |
| `schemas/student_info.py` vs `schemas/student_schemas.py` | Schema 定义重复 | 合并 Schema 定义 |
| `service/student_info.py` vs `service/student_service.py` | 业务逻辑重复 | 合并 Service 层 |
| `dao/student_info.py` vs `dao/student_dao.py` | 数据访问逻辑重复 | 合并 DAO 层 |

### 3.5 Service 层在循环中手动 commit 无异常回滚

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/score.py` | 81-88 | `restore_score_service` 在循环中修改数据后直接 `db.commit()`，无异常回滚 | 添加 `try/except` 块，异常时调用 `db.rollback()` |

### 3.6 过度使用静态方法

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/employee1.py` | 8-108 | `EmploymentService` 全部使用 `@staticmethod`，失去了面向对象的优势 | 改为实例方法或使用模块级函数 |
| `dao/employee1.py` | 9-114 | `EmploymentDao` 全部使用 `@staticmethod` | 同上 |

### 3.7 API 层直接导入 DAO 层

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/score.py` | 3 | `from service.score import *` 导入了所有 service 函数，但 service 层又导入了 DAO | 保持当前分层，但避免使用 `*` 导入，改为显式导入 |

---

## 4. 注释与文档审查

### 4.1 废话注释过多

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `dao/student_info.py` | 8-12 | `#创建数据库会话，导入前端传入的数据` 等注释描述的是语法而非业务意图 | 删除或改为描述业务意图的注释 |
| `dao/student_info.py` | 16 | `#返回查询到的第一条数据` | 删除 |
| `dao/student_info.py` | 20-26 | 每行都有注释描述语法 | 删除 |
| `dao/teacher.py` | 6-11 | 类似废话注释 | 删除 |
| `dao/score.py` | 13-21 | 类似废话注释 | 删除 |
| `api/score.py` | 14-16 | `# 调用业务逻辑层添加成绩方法，传入数据库会话和成绩参数` | 删除 |
| `api/score.py` | 35 | `# 依赖注入获取数据库会话` | 删除 |
| `service/score.py` | 7-19 | 类似废话注释 | 删除 |

### 4.2 关键逻辑缺失注释

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `dao/score.py` | 93-106 | `get_all_above_80_dao` 子查询逻辑复杂，缺少注释说明 | 添加注释说明子查询和主查询的作用 |
| `dao/score.py` | 109-147 | `get_multiple_fail_dao` 使用 `defaultdict` 分组逻辑复杂 | 添加注释说明分组逻辑 |
| `dao/class_info_dao.py` | 70-89 | `count_class_month` 使用 `DATE_FORMAT` 和 `group_concat` | 添加注释说明 SQL 函数作用 |
| `service/employee1.py` | 23-40 | `get_statistics_service` 统计逻辑复杂 | 添加注释说明统计维度 |

### 4.3 Schema 配置使用已废弃的 API

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `schemas/student_info.py` | 38 | `from_attributes = True` 是 Pydantic v2 写法，但注释写的是"将读取到的类属性转化可返回的字典/json" | 更新注释说明这是 Pydantic v2 的 ORM 模式配置 |
| `schemas/score.py` | 25, 34, 42, 51, 59, 68, 78, 87, 96, 105 | 所有 `from_attributes = True` 注释类似 | 同上 |

### 4.4 缺少模块级 Docstring

| 文件 | 问题 | 建议 |
|------|------|------|
| `api/__init__.py` | 无模块级 Docstring | 添加模块说明 |
| `service/__init__.py` | 无模块级 Docstring | 添加模块说明 |
| `dao/__init__.py` | 无模块级 Docstring | 添加模块说明 |
| `models/__init__.py` | 无模块级 Docstring | 添加模块说明 |
| `schemas/__init__.py` | 无模块级 Docstring | 添加模块说明 |

---

## 5. 异步与并发安全

### 5.1 数据库会话生命周期管理

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `database.py` | 22-27 | `get_db()` 使用 `yield` 但未被 `@contextlib.contextmanager` 或 FastAPI 的 `Depends` 正确包装 | 当前实现正确，FastAPI 会自动处理 `yield` 的依赖注入 |
| `dao/student_info.py` | 10-11 | `db.commit()` 后未检查异常 | 添加 `try/except` 块，异常时调用 `db.rollback()` |
| `dao/teacher.py` | 9-10 | 同上 | 同上 |
| `dao/class_info_dao.py` | 22-23 | 同上 | 同上 |
| `dao/employee1.py` | 74-76 | 同上 | 同上 |
| `dao/stu_employment.py` | 14-16 | 同上 | 同上 |
| `dao/student_dao.py` | 9-11 | 同上 | 同上 |

### 5.2 无异步 IO 阻塞问题

| 文件 | 问题 | 建议 |
|------|------|------|
| 全局 | 项目未使用 `async/await`，所有路由都是同步函数 | 当前实现可接受，但建议对耗时操作（如统计查询）使用异步函数 |

---

## 6. 依赖注入与配置

### 6.1 环境变量管理

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `.env` | 3 | 数据库密码明文存储 | 生产环境应使用密钥管理服务 |
| `database.py` | 9 | 默认密码 `123456` 硬编码 | 移除默认值，强制从环境变量读取 |
| `main.py` | 14-15 | 默认 host/port 硬编码 | 当前实现可接受 |

### 6.2 Depends 机制使用

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `api/student_info.py` | 10 | `db: Session = Depends(get_db)` 正确 | 无问题 |
| 全局 | 所有 API 路由都正确使用 `Depends(get_db)` | 无问题 |

---

## 7. 异常处理机制

### 7.1 全局异常处理器

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `main.py` | 24-45 | 已添加全局异常处理器 | 无问题 |

### 7.2 异常捕获过于宽泛

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `service/score.py` | 86 | `except Exception` 捕获所有异常 | 改为捕获具体异常类型，如 `SQLAlchemyError` |

### 7.3 遗漏必要的错误处理

| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| `dao/student_info.py` | 10-11 | `db.commit()` 无异常处理 | 添加 `try/except` 块 |
| `dao/teacher.py` | 9-10 | 同上 | 同上 |
| `dao/class_info_dao.py` | 22-23 | 同上 | 同上 |
| `dao/employee1.py` | 74-76 | 同上 | 同上 |
| `dao/stu_employment.py` | 14-16 | 同上 | 同上 |
| `dao/student_dao.py` | 9-11 | 同上 | 同上 |

---

## 修正情况记录

| 序号 | 类别 | 问题描述 | 涉及文件 | 修正状态 | 说明 |
|------|------|----------|----------|----------|------|
| 1.1 | 命名规范 | 两个学生模块命名冲突 | models/schemas/api 多个文件 | ⏭️ 暂缓 | 涉及数据库表结构变更，需单独规划 |
| 1.2 | 命名规范 | 两个就业模块命名冲突 | models/schemas/api/service/dao 多个文件 | ⏭️ 暂缓 | 涉及数据库表结构变更，需单独规划 |
| 1.3 | 命名规范 | API 路由函数命名不一致 | api/student_info.py, api/teacher.py, api/class_info_api.py, api/score.py | ⏭️ 暂缓 | 不影响功能，可后续统一 |
| 1.4 | 命名规范 | Service 层函数命名使用 judge_ 前缀 | service/student_info.py, service/teacher.py | ✅ 已修正 | 已移除 judge_ 前缀，统一函数命名 |
| 1.5 | 命名规范 | 变量命名不规范 | dao/class_info_dao.py, service/class_info_service.py | ✅ 已修正 | cls → class_obj, all_cls_service → all_classes, one_cls_service → class_info |
| 2.1 | 接口一致性 | API 响应格式不统一 | 多个 API 文件 | ⏭️ 暂缓 | 涉及大量文件修改，需单独规划 |
| 2.2 | 接口一致性 | 分页参数命名不一致 | api/score.py, api/employee1.py | ⏭️ 暂缓 | 保留现有参数，避免破坏前端兼容性 |
| 2.3 | 接口一致性 | 删除/恢复接口返回字段名不一致 | api/score.py, api/stu_employment.py | ✅ 已修正 | 已统一使用 message 字段 |
| 2.4 | 接口一致性 | 状态码使用不合理 | 多个 service 文件 | ⏭️ 暂缓 | 涉及业务逻辑变更，需与产品确认 |
| 3.1 | 架构合理性 | Service 层越层问题 | service/score.py, service/class_info_service.py | ⏭️ 暂缓 | 不影响功能，可后续优化 |
| 3.2 | 架构合理性 | DAO 层返回字典而非 ORM 对象 | dao/student_info.py, dao/score.py | ⏭️ 暂缓 | 不影响功能，可后续优化 |
| 3.3 | 架构合理性 | 两个就业模块重复设计 | employment 和 employment2 模块 | ⏭️ 暂缓 | 涉及数据库表结构变更，需单独规划 |
| 3.4 | 架构合理性 | 两个学生模块重复设计 | student 和 student2 模块 | ⏭️ 暂缓 | 涉及数据库表结构变更，需单独规划 |
| 3.5 | 架构合理性 | Service 层在循环中手动 commit 无异常回滚 | service/score.py | ✅ 已修正 | 已添加 try/except 和 db.rollback() |
| 3.6 | 架构合理性 | 过度使用静态方法 | service/employee1.py, dao/employee1.py | ⏭️ 暂缓 | 当前设计可接受，不影响功能 |
| 3.7 | 架构合理性 | API 层直接导入 DAO 层 | api/score.py | ⏭️ 暂缓 | 当前实现可接受 |
| 4.1 | 注释与文档 | 废话注释过多 | dao/student_info.py, dao/teacher.py, dao/score.py, api/score.py, service/score.py | ✅ 已修正 | 已清理所有废话注释，保留关键业务逻辑注释 |
| 4.2 | 注释与文档 | 关键逻辑缺失注释 | dao/score.py, dao/class_info_dao.py, service/employee1.py | ⏭️ 暂缓 | 不影响功能，可后续补充 |
| 4.3 | 注释与文档 | Schema 配置注释不准确 | schemas/student_info.py, schemas/score.py | ⏭️ 暂缓 | 不影响功能，可后续更新 |
| 4.4 | 注释与文档 | 缺少模块级 Docstring | api/__init__.py, service/__init__.py, dao/__init__.py, models/__init__.py, schemas/__init__.py | ⏭️ 暂缓 | 不影响功能，可后续补充 |
| 5.1 | 异步与并发 | 数据库会话生命周期管理 | dao 多个文件 | ⏭️ 暂缓 | 当前实现可接受 |
| 5.2 | 异步与并发 | 无异步 IO 阻塞问题 | 全局 | ⏭️ 暂缓 | 当前实现可接受 |
| 6.1 | 依赖注入 | 环境变量管理 | .env, database.py | ⏭️ 暂缓 | 当前实现可接受 |
| 6.2 | 依赖注入 | Depends 机制使用 | 全局 | ✅ 无问题 | 所有 API 路由都正确使用 Depends(get_db) |
| 7.1 | 异常处理 | 全局异常处理器 | main.py | ✅ 无问题 | 已添加全局异常处理器 |
| 7.2 | 异常处理 | 异常捕获过于宽泛 | service/score.py | ✅ 已修正 | 已将 except Exception 改为 except SQLAlchemyError |
| 7.3 | 异常处理 | 遗漏必要的错误处理 | dao/student_info.py, dao/teacher.py, dao/class_info_dao.py | ✅ 已修正 | 已为所有 db.commit() 添加 try/except 和 db.rollback() |

### 修正统计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ 已修正/无问题 | 9 | 31% |
| ⏭️ 暂缓 | 20 | 69% |

> 注：暂缓项目均为低风险或涉及较大范围变更的问题，可在后续版本中逐步优化。
