#!/usr/bin/env python3
"""Flask -> Pboot 批量改名脚本。

跨平台可用（不依赖 GNU grep / BSD sed 的扩展语法），只处理 Python 源文件。

用法:
    python migrate_flask_to_pboot.py <目录>            # 原地改写
    python migrate_flask_to_pboot.py <目录> --dry-run  # 只预览

处理规则:
    from flask...      -> from pboot...
    import flask...     -> import pboot...
    Flask(...)         -> Pboot(...)
    FlaskClient        -> PbootClient
    flask_<子模块>      -> pboot_<子模块>   (如 flask.testing -> pboot.testing)

不会改动:
    第三方包名 (flask_login / flask_sqlalchemy / flask_wtf / flask_cors ...)
    字符串字面量与注释里的 flask 字样
"""
import argparse
import ast
import pathlib
import re
import sys

# 真正的框架子模块: flask.xxx 且 xxx 不是第三方包名
# 第三方包: flask_login, flask_sqlalchemy, flask_wtf, flask_cors, flask_restful ...
THIRD_PARTY = {
    "flask_login", "flask_sqlalchemy", "flask_wtf", "flask_cors",
    "flask_restful", "flask_restx", "flask_migrate", "flask_admin",
    "flask_caching", "flask_talisman", "flask_mongoengine", "flask_jwt",
    "flask_socketio", "flask_limiter", "flask_mail", "flask_bcrypt",
    "flask_cors", "flask_paginate", "flask_debugtoolbar", "flask_whooshee",
}


def collect_flask_modules(tree):
    """收集源码中真正属于框架的 flask 子模块名。"""
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                if root == "flask":
                    mods.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] == "flask":
                mods.add(node.module)
    return mods


def transform(text, modules):
    out = text

    # 1) import 语句: from flask... / import flask...
    for mod in sorted(modules, key=len, reverse=True):
        pboot_mod = "pboot" + mod[len("flask"):]
        out = re.sub(rf"(^|\n)(\s*)from\s+{re.escape(mod)}\b",
                     rf"\1\2from {pboot_mod}", out)
        out = re.sub(rf"(^|\n)(\s*)import\s+{re.escape(mod)}\b",
                     rf"\1\2import {pboot_mod}", out)

    # 2) 类名
    out = re.sub(r"\bFlask\(", "Pboot(", out)
    out = re.sub(r"\bFlaskClient\b", "PbootClient", out)

    # 3) 导入列表中的 Flask 类名: from pboot import Flask, xxx -> from pboot import Pboot, xxx
    #    只处理确实改写过 from flask 的行, 避免误伤第三方包
    out = re.sub(r"(^from\s+pboot\s+import\s+[^\n]*?)\bFlask\b",
                 r"\1Pboot", out, flags=re.M)

    return out


def main():
    ap = argparse.ArgumentParser(description="Flask -> Pboot 批量改名")
    ap.add_argument("path", help="要处理的目录")
    ap.add_argument("--dry-run", action="store_true", help="只预览不写入")
    args = ap.parse_args()

    root = pathlib.Path(args.path)
    changed = []

    for py in sorted(root.rglob("*.py")):
        if any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"}
               for part in py.parts):
            continue
        try:
            text = py.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (SyntaxError, UnicodeDecodeError):
            continue

        mods = collect_flask_modules(tree)
        if not mods:
            continue

        new_text = transform(text, mods)
        if new_text != text:
            changed.append((py, mods))
            if not args.dry_run:
                py.write_text(new_text, encoding="utf-8")
                print(f"  [改写] {py}  ({', '.join(sorted(mods))})")
            else:
                print(f"  [预览] {py}  ({', '.join(sorted(mods))})")

    if not changed:
        print("未发现需要改写的文件。")
    else:
        print(f"\n共 {len(changed)} 个文件{'已改写' if not args.dry_run else '待改写'}。")
    print("\n请人工复查以下项目（脚本无法自动判断）：")
    print("  1. 导入列表中的 Flask 类名是否已改为 Pboot")
    print("  2. SQLALCHEMY_* 配置键是否已改为 PBATIS_*")
    print("  3. FlaskForm 是否已改为 PbootForm")
    print("  4. 字符串中的 'flask' 字样（如配置项、模板变量名）")


if __name__ == "__main__":
    sys.exit(main())
