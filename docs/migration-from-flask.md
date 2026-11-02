# 从 Flask 迁移到 Pboot

本文档面向已有 Flask 项目的开发者，说明如何把项目迁移到 Pboot。

Pboot 是 Flask 的完整分支实现：**API 表面几乎完全一致**，绝大多数迁移工作集中在「改名」，
而不是「重写」。下文按「必须改的」「容易漏的」「不需要改的」三层组织，每一条都经过实机验证。

---

## 一、迁移成本速览

Pboot 与 Flask 的顶层 API **完全对齐**，实测差异如下：

| 对比项 | 结论 |
| --- | --- |
| 顶层导出名 | 仅 `Flask` → `Pboot`，其余全部一致 |
| `app` 实例方法 | 完全一致 |
| `Blueprint` 方法 | 完全一致 |
| `flask.json` / `pboot.json` | 完全一致 |
| 默认配置键 | 完全一致 |
| 新增能力 | `app.query` / `blueprint.query`（上游 3.2 新增） |

因此迁移工作量主要集中在：

1. 导入语句改名
2. 扩展包替换
3. CLI / 环境变量 / 配置文件改名
4. 少量 API 语义差异（见第五章）

---

## 二、第一步：改导入语句

### 2.1 应用类

```python
# 迁移前
from flask import Flask
app = Flask(__name__)

# 迁移后
from pboot import Pboot
app = Pboot(__name__)
```

### 2.2 全局对象

```python
# 迁移前
from flask import request, session, g, current_app

# 迁移后
from pboot import request, session, g, current_app
```

### 2.3 工具函数

```python
# 迁移前
from flask import (
    render_template, render_template_string,
    url_for, redirect, abort, jsonify,
    make_response, send_file, send_from_directory,
    flash, get_flashed_messages, stream_with_context,
)

# 迁移后
from pboot import (
    render_template, render_template_string,
    url_for, redirect, abort, jsonify,
    make_response, send_file, send_from_directory,
    flash, get_flashed_messages, stream_with_context,
)
```

### 2.4 蓝图与类型

```python
# 迁移前
from flask import Blueprint, Request, Response

# 迁移后
from pboot import Blueprint, Request, Response
```

### 2.5 子模块路径

Pboot 与 Flask 的子模块结构一一对应，只需把 `flask` 换成 `pboot`：

```python
from flask.blueprints import Blueprint     →  from pboot.blueprints import Blueprint
from flask.config import Config           →  from pboot.config import Config
from flask.ctx import AppContext          →  from pboot.ctx import AppContext
from flask.helpers import url_for         →  from pboot.helpers import url_for
from flask.json.provider import DefaultJSONProvider
                                          →  from pboot.json.provider import DefaultJSONProvider
from flask.signals import request_started →  from pboot.signals import request_started
from flask.testing import FlaskClient     →  from pboot.testing import PbootClient
from flask.templating import render_template
                                          →  from pboot.templating import render_template
from flask.wrappers import Response       →  from pboot.wrappers import Response
```

> `pboot.testing.FlaskClient` 已更名为 `PbootClient`，**未保留旧别名**，需一并修改。
> `pboot.testing.Client` 仍然可用（werkzeug 测试客户端基类，未改名）。

### 2.6 一键替换（推荐用脚本）

仓库提供了经过实测的迁移脚本，它基于 Python AST 精确识别 `flask` 导入，
**不会误伤 `flask_login` / `flask_sqlalchemy` / `flask_wtf` 等第三方包名**：

```console
$ python docs/migrate_flask_to_pboot.py <项目目录> --dry-run   # 先预览
$ python docs/migrate_flask_to_pboot.py <项目目录>             # 实际改写
```

脚本自动处理：

- `from flask...` → `from pboot...`（含 `flask.testing` 等子模块）
- `import flask` → `import pboot`
- 导入列表里的 `Flask` → `Pboot`
- `Flask(__name__)` → `Pboot(__name__)`
- `FlaskClient` → `PbootClient`

> 为什么不直接用 `sed` 一把梭？macOS 自带的 BSD `grep`/`sed` 不支持 `\s` 和 `\b`
> 这类 GNU 扩展语法，直接照搬网上常见的 Flask 改名命令会**静默不生效**；
> 而 GNU 版与 BSD 版语法又不兼容。脚本跨平台且行为确定，更可靠。

若坚持用命令行替换，注意各平台差异：

```console
# GNU (Linux)
$ grep -rl --include="*.py" -E "^\s*from flask\b" . | xargs sed -i 's/\bfrom flask\b/from pboot/g'

# macOS (BSD): 需去掉 -i 的空串, 且 \b 不可用
$ grep -rl --include="*.py" -E "^from flask([^_a-zA-Z0-9]|$)" . | xargs sed -i '' -E 's/from flask/from pboot/g'
```

执行后**必须人工复查**以下几处，它们无法靠正则可靠判断：

| 位置 | 问题 | 处理 |
| --- | --- | --- |
| `from pboot import Flask, ...` | 导入列表里的类名 | 改为 `Pboot` |
| `from pboot.testing import FlaskClient` | 带 `Flask` 前缀的类名 | 改为 `PbootClient` |
| `flask_login` / `flask_cors` 等 | 第三方包名 | **不要改** |
| `SQLALCHEMY_*` 配置键 | 扩展专有配置 | 见第三章 |

---

## 三、第二步：换扩展包

Pboot 生态已提供官方对应扩展，依赖关系已声明为 `pboot>=3.2.0`：

| Flask 扩展 | Pboot 对应 | 说明 |
| --- | --- | --- |
| `Flask-SQLAlchemy` | `pboot-pbatis` | 底层 ORM 换成 pbatis，配置键随之变化 |
| `Flask-WTF` | `pboot-wtf` | 类名 `FlaskForm` → `PbootForm` |
| `Flask-Caching` | `pboot-caching` | 配置键 `CACHE_*` 保持不变 |
| `Flask-Talisman` | `pboot-talisman` | API 完全一致 |
| `Flask-MongoEngine` | `pboot-mongoengine` | 依赖 `pboot-wtf` |

```console
$ pip uninstall Flask-SQLAlchemy Flask-WTF Flask-Caching Flask-Talisman Flask-MongoEngine
$ pip install pboot-pbatis pboot-wtf pboot-caching pboot-talisman pboot-mongoengine
```

### 3.1 pboot-pbatis 的两处差异

**导入名与类名：**

```python
# 迁移前
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 迁移后
from pboot_pbatis import Pbatis
from pboot_pbatis.model import Model
```

**配置键全部改为 `PBATIS_` 前缀**（不兼容旧键，需逐一修改）：

| Flask 配置键 | Pboot 配置键 |
| --- | --- |
| `SQLALCHEMY_DATABASE_URI` | `PBATIS_DATABASE_URI` |
| `SQLALCHEMY_BINDS` | `PBATIS_BINDS` |
| `SQLALCHEMY_ENGINE_OPTIONS` | `PBATIS_ENGINE_OPTIONS` |
| `SQLALCHEMY_ECHO` | `PBATIS_ECHO` |
| `SQLALCHEMY_RECORD_QUERIES` | `PBATIS_RECORD_QUERIES` |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | `PBATIS_TRACK_MODIFICATIONS` |

### 3.2 pboot-wtf 的类名差异

```python
# 迁移前
from flask_wtf import FlaskForm
from flask_wtf.form import FlaskForm as BaseFlaskForm

# 迁移后
from pboot_wtf import PbootForm
from pboot_wtf.form import PbootForm as BasePbootForm
```

同时替换所有继承声明：

```python
class MyForm(FlaskForm):   →   class MyForm(PbootForm):
```

---

## 四、第三步：改命令行与环境变量

### 4.1 CLI 命令

```console
$ flask run                 →  $ pboot run
$ flask shell               →  $ pboot shell
$ flask routes              →  $ pboot routes
$ flask --version           →  $ pboot --version
$ python -m flask           →  $ python -m pboot
```

`pboot` 与 `flask` 的 CLI 参数完全对应：

| 参数 | 说明 |
| --- | --- |
| `--app` | 指定应用或工厂函数（`module:app` 形式） |
| `--debug` | 开启调试模式 |
| `--env_file` | 从指定文件加载环境变量 |
| `--version` | 显示版本 |

### 4.2 环境变量

| Flask | Pboot |
| --- | --- |
| `FLASK_APP` | `PBOOT_APP` |
| `FLASK_DEBUG` | `PBOOT_DEBUG` |
| `FLASK_SKIP_DOTENV` | `PBOOT_SKIP_DOTENV` |
| `FLASK_RUN_FROM_CLI` | `PBOOT_RUN_FROM_CLI` |

> 注意：`FLASK_RUN_PORT` / `FLASK_RUN_HOST` 是 Flask 2.x 的旧特性，Flask 3.x 与 Pboot 均已移除。
> 请改用 `--port` / `--host` 命令行参数。

### 4.3 环境变量文件

Pboot 默认加载 **`.pbootenv`** 和 **`.env`**，**不再读取 `.flaskenv`**。

```console
$ git mv .flaskenv .pbootenv
```

实测行为对照：

| 文件 | Flask | Pboot |
| --- | --- | --- |
| `.flaskenv` | 加载 | **不加载** |
| `.pbootenv` | 不加载 | 加载 |
| `.env` | 加载 | 加载 |

> 若想继续使用 `.flaskenv`，可用 `--env_file .flaskenv` 显式指定。

### 4.4 容器与进程管理

```dockerfile
# 迁移前
CMD ["flask", "run", "--host=0.0.0.0"]

# 迁移后
CMD ["pboot", "run", "--host=0.0.0.0"]
```

Gunicorn / uWSGI 等 WSGI 服务器无需改动 —— Pboot 应用本身就是标准 WSGI 应用：

```console
$ gunicorn "app:app"
```

---

## 五、需要注意的 API 语义差异

以下差异源于 Pboot 基于 Flask 上游 **3.2 开发版**，而多数项目仍在用 **3.1.x** 稳定版。

### 5.1 `RequestContext` 已并入 `AppContext`（上游 #5639）

这是 3.2 最大的内部重构：**已 push 的 app context 在派发请求时不再复用**。

绝大多数项目感知不到这个变化。但有一类写法会受影响 —— **请求结束后再访问请求期间写入 `g` 的属性**：

```python
@app.route("/")
def index():
    g.token = compute_token()
    return "ok"

# 测试中
response = client.get("/")
assert response.data == g.token       # Flask 3.1 可用；Pboot / Flask 3.2 可能 AttributeError
```

典型受影响的是 **CSRF token 校验类测试**：Flask-WTF 把 token 存进 `g.csrf_token`，
若在请求结束后断言 `g.csrf_token` 就会失败（Flask 3.2 起该行为已改变）。

**改法**：在请求处理器内部捕获需要的值，而不是事后从 `g` 取。

```python
tokens = []

@app.route("/")
def index():
    f = PbootForm()
    tokens.append(g.csrf_token)           # 在上下文内取值
    return f.csrf_token.current_token

response = client.get("/")
assert response.data == tokens[0]
```

> 排查建议：若迁移后测试报 `AttributeError` 且涉及 `g`、`current_app` 或请求上下文对象，
> 优先检查是否在请求结束后才访问这些对象。

### 5.2 `__version__` 属性已移除

Flask 3.2 移除了已废弃的 `flask.__version__`（用 `importlib.metadata` 替代）。

```python
# 迁移前
from flask import __version__

# 迁移后
from importlib.metadata import version
__version__ = version("pboot")
```

同理，`flask.__version__` 的其他用法（如在 `setup.py` 中动态取版本）都需改为静态声明。

### 5.3 `redirect` 默认返回 303

Flask 3.2 起 `redirect()` 默认返回 **303 See Other**（此前是 302）。

这会让浏览器在 POST 后改用 GET —— 通常正是期望行为，但对断言状态码的测试有影响：

```python
# 迁移前
assert response.status_code == 302

# 迁移后
assert response.status_code == 303
```

若需保持 302，显式指定：`redirect(url, code=302)`。

### 5.4 `flask.Markup` 与 `flask.escape` 不可用

自 Flask 2.3 起已移除（`flask 3.1` 同样没有），Pboot 保持一致。

```python
# 旧写法（Flask 2.2 及更早）
from flask import Markup, escape
safe = Markup("<b>x</b>")

# 迁移后
from markupsafe import Markup, escape
```

### 5.5 模板上下文处理器的签名

`@app.context_processor` 的函数在 3.2 中仍接收一个字典参数，但 `stream_template`
等新接口已加入。若项目使用自定义模板全局对象，注意 `app.jinja_env.globals` 赋值方式不变。

---

## 六、不需要改动的部分

以下内容与框架无关，**保持原样**：

- 所有业务逻辑、视图函数、路由装饰器
- 模板文件（`*.html` / `*.jinja2`）与 Jinja2 语法
- `static/` 目录结构
- 数据库模型定义（若用 `pboot-pbatis`，仅需换基类导入）
- 测试框架用法：`app.test_client()`、`app.test_request_context()` 行为一致
- `before_request` / `after_request` / `teardown_*` 等钩子
- `Blueprint` 的注册方式（`app.register_blueprint(bp, url_prefix=...)`）
- `app.config` 的所有自定义配置键
- Celery / Redis / SQLAlchemy Core 等第三方集成

### 关于第三方扩展

部分社区扩展直接依赖 `flask` 包（如 `flask-login`、`flask-restful`），这类扩展**不能**直接用在 Pboot 上，
需要等待对应移植版本，或改用标准 WSGI 方式集成。

迁移前建议先排查：

```console
$ grep -rn "flask" requirements.txt pyproject.toml setup.py
```

若依赖的扩展只是间接使用 `flask.Flask` 做类型判断，通常改动量很小；
若直接 `import flask` 并调用框架内部 API，则需要更深入的处理。

---

## 七、迁移检查清单

按顺序执行，每步都可独立验证：

- [ ] 1. 安装 Pboot 与生态扩展，卸载 Flask 系扩展
- [ ] 2. 运行迁移脚本：`python docs/migrate_flask_to_pboot.py <目录> --dry-run` 先预览，再执行
- [ ] 3. 替换导入语句：`from flask` → `from pboot`，`Flask` → `Pboot`
- [ ] 4. 替换子模块导入：`flask.xxx` → `pboot.xxx`
- [ ] 5. 处理扩展差异：`FlaskForm` → `PbootForm`，`SQLALCHEMY_*` → `PBATIS_*`
- [ ] 6. 修改 CLI 调用：`flask` → `pboot`
- [ ] 7. 修改环境变量：`FLASK_*` → `PBOOT_*`
- [ ] 8. 重命名 `.flaskenv` → `.pbootenv`
- [ ] 9. 更新 Dockerfile / CI / Procfile 中的 `flask` 命令
- [ ] 10. 排查 `g` 跨请求访问、`__version__`、`redirect` 状态码断言（见第五章）
- [ ] 11. 跑通全部测试套件
- [ ] 12. 用 `pboot routes` 核对路由表与迁移前一致
- [ ] 13. 检查第三方扩展的兼容性

### 验证命令

```console
# 路由表核对（迁移前后 diff 应为空）
$ flask routes  > /tmp/routes-before.txt
$ pboot routes  > /tmp/routes-after.txt
$ diff /tmp/routes-before.txt /tmp/routes-after.txt

# 启动冒烟测试
$ pboot run --port 5000
```

---

## 八、常见问题

**Q：可以直接 `import pboot` 然后 `pboot.Flask` 吗？**
不能。应用类已更名为 `Pboot`，需写 `from pboot import Pboot`。

**Q：现有 Flask 项目的 `.flaskenv` 里的配置会失效吗？**
是的，`.flaskenv` 不再自动加载。请重命名为 `.pbootenv`，或用 `--env_file .flaskenv` 显式指定。

**Q：`flask run` 的参数还能用吗？**
可以。`pboot` 的 CLI 参数与 `flask` 完全对应，包括 `--host`、`--port`、`--debug`、`--env_file`。

**Q：pboot 支持 Python 3.10 吗？**
不支持。Pboot 3.2 要求 **Python >= 3.11**，Flask 3.1 支持 3.9+。如需兼容旧版本 Python，请停留在 Flask 3.1。

**Q：两者性能有差异吗？**
Pboot 与 Flask 同源同构，性能基本一致。迁移不需要任何性能调优动作。

**Q：能不能两个框架并存，逐步迁移？**
不推荐。两者共用同一套 WSGI 生态，但 `flask` 与 `pboot` 的上下文对象互不相通，
混用会导致 `current_app` / `g` / `session` 取值错乱。建议一次性完成单模块切换。

---

## 九、已验证的迁移实例

以下实例在真实 Flask 项目上完整跑通，可作为迁移验收基准。

**迁移前**（标准 Flask 项目）：

```python
from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECRET_KEY'] = 'x'
db = SQLAlchemy(app)
login = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class MyForm(FlaskForm):
    pass

bp = Blueprint('api', __name__)

@bp.route('/api/<name>')
def api(name):
    return jsonify(name=name)

app.register_blueprint(bp)
```

**迁移后**：

```python
from pboot import Pboot, render_template, request, jsonify, Blueprint
from pboot_pbatis import Pbatis
from pboot_wtf import PbootForm

app = Pboot(__name__)
app.config['PBATIS_DATABASE_URI'] = 'sqlite://'
app.config['SECRET_KEY'] = 'x'
db = Pbatis(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class MyForm(PbootForm):
    pass

bp = Blueprint('api', __name__)

@bp.route('/api/<name>')
def api(name):
    return jsonify(name=name)

app.register_blueprint(bp)
```

**迁移后验证结果**（PyPI 安装的真实包，非本地源码）：

```
✓ 导入成功 (pboot + pboot_pbatis + pboot_wtf)
✓ 建表+插入+查询: [(1, '大羽')]
✓ 模板渲染: 200 <h1>Hello</h1>
✓ 蓝图路由: 200 {"name":"x"}
✓ POST JSON: 200 {"data":{"k":"v"}}

$ pboot --app app:app routes
Endpoint  Methods  Rule
--------  -------  -----------------------
api.api   GET      /api/<name>
echo      POST     /echo
idx       GET      /
static    GET      /static/<path:filename>
```

---

## 十、迁移陷阱速查

按实际踩坑频率排序：

| 陷阱 | 现象 | 处理 |
| --- | --- | --- |
| 第三方扩展名被误改 | `from flask_login import ...` 变成 `from pboot_login import ...` | 用配套脚本（基于 AST 精确识别）；或用 `flask([^_a-zA-Z0-9]|$)` 限定 |
| 导入列表里的类名漏改 | `from pboot import Flask` → `ImportError` | 改 `Flask` → `Pboot` |
| 配置键漏改 | `RuntimeError: Either 'PBATIS_DATABASE_URI' or 'PBATIS_BINDS' must be set` | `SQLALCHEMY_*` → `PBATIS_*` |
| `.flaskenv` 不再加载 | 环境变量读不到 | 重命名为 `.pbootenv` |
| `redirect` 状态码变化 | 断言 `302` 失败，实际 `303` | 改断言，或 `redirect(url, code=302)` |
| `__version__` 移除 | `ImportError` | 用 `importlib.metadata.version("pboot")` |
| `g` 在请求结束后失效 | `AttributeError: csrf_token` | 在请求处理器内取值，不要事后取 `g` |
| `FlaskClient` 不存在 | `ImportError` | 改 `PbootClient` |
| `Markup` / `escape` 不存在 | `ImportError` | 从 `markupsafe` 导入 |
| BSD 工具链不支持 `\b` | 替换命令**静默不生效** | 用配套 Python 脚本 |

---

## 相关链接

- Pboot 源码与文档：<https://gitee.com/pboot-org/pboot>
- pboot-pbatis：<https://gitee.com/pboot-org/pboot-pbatis>
- pboot-wtf：<https://gitee.com/pboot-org/pboot-wtf>
- pboot-caching：<https://gitee.com/pboot-org/pboot-caching>
- pboot-talisman：<https://gitee.com/pboot-org/pboot-talisman>
- pboot-mongoengine：<https://gitee.com/pboot-org/pboot-mongoengine>
- PyPI：<https://pypi.org/project/pboot/>
