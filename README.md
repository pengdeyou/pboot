<div align="center">
  <img src="docs/_static/pboot-logo.svg" alt="Pboot" height="140">
</div>

# Pboot

**Pboot** 是一个轻量级的 [WSGI] Web 应用框架，目标是让项目启动足够快，同时又能平滑扩展到复杂应用。

```python
from pboot import Pboot

app = Pboot(__name__)


@app.route("/")
def hello():
    return "Hello, Pboot!"
```

```console
$ pboot run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## 特性

- **轻量**：核心只依赖 [Werkzeug]、[Jinja]、[Click]、[ItsDangerous]、[MarkupSafe] 与 [Blinker]
- **灵活**：Pboot 只提供建议，不强制依赖或项目结构，开发者可以自由选择工具链
- **可扩展**：通过统一的扩展接口，ORM、缓存、CSRF、HTTP 安全头等能力按需接入
- **完备**：内置路由、模板、会话、蓝图、信号、测试客户端与 CLI

## 安装

```console
$ pip install pboot
```

## 生态

| 扩展 | 说明 |
| --- | --- |
| [pboot-pbatis](https://gitee.com/pboot-org/pboot-pbatis) | 基于 [pbatis](https://gitee.com/pboot-org/pbatis) ORM 的数据库支持 |
| [pboot-wtf](https://gitee.com/pboot-org/pboot-wtf) | 表单渲染、校验、CSRF 防护与文件上传 |
| [pboot-caching](https://gitee.com/pboot-org/pboot-caching) | 多后端缓存支持 |
| [pboot-talisman](https://gitee.com/pboot-org/pboot-talisman) | HTTP 安全响应头 |
| [pboot-mongoengine](https://gitee.com/pboot-org/pboot-mongoengine) | MongoEngine 集成 |

## 核心概念

### 应用与路由

```python
from pboot import Pboot

app = Pboot(__name__)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    return f"User {user_id}"


@app.post("/users")
def create_user():
    return "created", 201
```

### 蓝图

```python
from pboot import Blueprint

bp = Blueprint("api", __name__)


@bp.route("/ping")
def ping():
    return "pong"
```

### 模板

```python
from pboot import render_template


@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)
```

### 配置

配置来自多种来源，按优先级从高到低依次为：

1. 直接传给 `Pboot(...)` 的构造参数
2. 环境变量
3. 配置文件
4. 默认值

```python
app.config["SECRET_KEY"] = "your-secret"
```

## 命令行

```console
$ pboot --help
$ pboot run --port 8080
$ pboot routes
$ pboot shell
```

## 测试

Pboot 提供测试客户端与独立的测试运行器：

```python
from pboot import Pboot

app = Pboot(__name__)


@app.route("/")
def index():
    return "ok"


def test_index():
    client = app.test_client()
    assert client.get("/").data == b"ok"
```

## 环境变量

| 变量 | 说明 |
| --- | --- |
| `PBOOT_APP` | 指定要加载的应用或工厂函数 |
| `PBOOT_DEBUG` | 开启调试模式 |
| `PBOOT_RUN_PORT` | 指定开发服务器端口 |
| `PBOOT_SKIP_DOTENV` | 跳过 `.pbootenv` / `.env` 加载 |

## 参与贡献

问题反馈、功能建议与代码贡献都欢迎通过
[pboot-org/pboot](https://gitee.com/pboot-org/pboot/issues) 提交。

## 许可证

BSD-3-Clause，详见 [LICENSE.txt](LICENSE.txt)。

[WSGI]: https://wsgi.readthedocs.io/
[Werkzeug]: https://werkzeug.palletsprojects.com/
[Jinja]: https://jinja.palletsprojects.com/
[Click]: https://click.palletsprojects.com/
[ItsDangerous]: https://itsdangerous.palletsprojects.com/
[MarkupSafe]: https://markupsafe.palletsprojects.com/
[Blinker]: https://blinker.readthedocs.io/
