#!/usr/bin/env bash
# pboot 生态 PyPI 发布脚本
#
# 用法:
#   export TWINE_USERNAME='__token__'
#   export TWINE_PASSWORD='pypi-xxxxxxxxxxxxxxxx'
#   ./tools/publish-pypi.sh            # 上传到正式 PyPI
#   ./tools/publish-pypi.sh --test     # 上传到 TestPyPI
#
# 需要的包(按依赖顺序, pboot 必须先发布):
#   pboot, pboot-pbatis, pboot-wtf, pboot-caching, pboot-talisman, pboot-mongoengine
set -euo pipefail

REPO="https://pypi.org/legacy/"
if [[ "${1:-}" == "--test" ]]; then
  REPO="https://test.pypi.org/legacy/"
  echo ">>> 目标: TestPyPI"
else
  echo ">>> 目标: PyPI (正式)"
fi

if [[ -z "${TWINE_PASSWORD:-}" ]]; then
  echo "!! 未设置 TWINE_PASSWORD。请先执行:"
  echo "   export TWINE_USERNAME='__token__'"
  echo "   export TWINE_PASSWORD='pypi-xxxxxxxxxxxxxxxxxxxx'"
  exit 1
fi

# 构建目录: 主包在仓库内, 扩展在 /tmp/extwork
BUILD_ROOT="${PBOOT_BUILD_ROOT:-/tmp/extwork}"
declare -a PACKAGES=(
  "pboot:${PWD}"
  "pboot-pbatis:${BUILD_ROOT}/pboot-pbatis"
  "pboot-wtf:${BUILD_ROOT}/pboot-wtf"
  "pboot-caching:${BUILD_ROOT}/pboot-caching"
  "pboot-talisman:${BUILD_ROOT}/pboot-talisman"
  "pboot-mongoengine:${BUILD_ROOT}/pboot-mongoengine"
)

echo ">>> 检查 twine"
python3 -m pip install --quiet --upgrade twine build

for entry in "${PACKAGES[@]}"; do
  name="${entry%%:*}"
  dir="${entry#*:}"

  if [[ ! -d "$dir" ]]; then
    echo "!! 跳过 $name: 目录不存在 $dir"
    continue
  fi

  echo ""
  echo ">>> 构建 $name"
  ( cd "$dir" && rm -rf dist build && python3 -m build >/dev/null )

  echo ">>> 校验 $name"
  python3 -m twine check "$dir"/dist/*

  echo ">>> 上传 $name"
  python3 -m twine upload --non-interactive \
    --repository-url "$REPO" "$dir"/dist/*
done

echo ""
echo ">>> 全部完成。已发布:"
for entry in "${PACKAGES[@]}"; do
  echo "  - ${entry%%:*}"
done
