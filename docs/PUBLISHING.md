# pboot 生态发布指南

## 当前状态

| 仓库 | Gitee | GitHub | PyPI | 版本 |
| --- | --- | --- | --- | --- |
| `pboot` | ✅ | ✅ | 待发布 | 3.2.0 |
| `pboot-pbatis` | ✅ | ✅ | 待发布 | 1.0.0 |
| `pboot-wtf` | ✅ | ✅ | 待发布 | 1.0.0 |
| `pboot-caching` | ✅ | ✅ | 待发布 | 1.0.0 |
| `pboot-talisman` | ✅ | ✅ | 待发布 | 1.0.0 |
| `pboot-mongoengine` | ✅ | ✅ | 待发布 | 1.0.0 |

GitHub 仓库统一位于 `pengdeyou/` 组织下，发布工作流统一为 `.github/workflows/publish.yaml`，
`environment: publish`，使用 `pypa/gh-action-pypi-publish`（Trusted Publishing / OIDC）。

## 发布前置条件（二选一）

### 方案 A：配置 Pending Trusted Publisher（推荐，无需 token）

PyPI 项目名在**首次发布时自动创建**，不需要单独"创建项目"。但 Trusted Publisher
需要在 PyPI 后台登记。

1. 登录 <https://pypi.org/account/login/>（账号 `corsak`）
2. 进入 **Manage → Publishing**（账号侧边栏的 "Publishing"，不是某个项目的）
3. 点击 **Add**，逐个添加 6 个 pending publisher，每个填：

   | 字段 | 值 |
   | --- | --- |
   | PyPI project name | `pboot` / `pboot-pbatis` / `pboot-wtf` / `pboot-caching` / `pboot-talisman` / `pboot-mongoengine` |
   | Provider | GitHub |
   | Owner | `pengdeyou` |
   | Repository name | 同上（与 PyPI project name 相同） |
   | Workflow name | `publish.yaml` |
   | Environment name | `publish` |

   > Environment name 留空也可以，但填 `publish` 与工作流保持一致更稳妥。

4. 在 GitHub 侧为对应仓库创建 `publish` environment：
   `https://github.com/pengdeyou/<repo>/settings/environments` → New environment → 命名 `publish`

5. 打 tag 触发发布：

   ```console
   $ git tag v3.2.0 && git push origin v3.2.0        # pboot
   $ git tag v1.0.0 && git push origin v1.0.0        # 各扩展
   ```

   GitHub Actions 会自动构建并上传到 PyPI，首次上传即创建项目。

### 方案 B：使用账号级 API Token

当前手上的 token 是**项目级 token**（载荷中 `*[3,"fb8f6023-..."]`），只对 `pbatis` 有效，
上传 `pboot` 会返回 `403 Forbidden`。PyPI 已废弃用户名密码上传，必须用 API token。

1. 登录 <https://pypi.org/manage/account/> → **API tokens** → **Add API token**
2. Token name 填 `pboot-publish`，Scope 选 **Entire account**
3. 得到 `pypi-...` 开头的 token 后：

   ```console
   $ export TWINE_USERNAME='__token__'
   $ export TWINE_PASSWORD='pypi-xxxxxxxxxxxxxxxx'
   $ bash tools/publish-pypi.sh          # 发布全部 6 个包
   $ bash tools/publish-pypi.sh --test   # 先发 TestPyPI 验证
   ```

   注意：发布顺序有依赖，`pboot` 必须先发布（扩展依赖 `pboot>=3.2.0`）。

## 本地构建

```console
$ python3 -m build          # 生成 dist/*.whl 与 dist/*.tar.gz
$ python3 -m twine check dist/*
```

## 已验证事项

- 6 个包的 wheel/sdist 构建均通过，元数据（Name / Version / Requires-Dist）已校验
- 现有 `pypi-...` token 上传 `pbatis` 成功（HTTP 200），确认 token 本身有效，仅权限受限
- 各扩展与上游基线的测试结果对照一致，详见各仓库的提交记录
