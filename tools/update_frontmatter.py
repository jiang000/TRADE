#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给仓库根目录下的所有 .md 文章补齐博客所需的 YAML front matter。
幂等：已存在的字段不会重复添加。

新增字段：
  title   —— 取自文件名（去掉 .md）
  layout  —— default（套用博客布局）
  pubdate —— 复制自已有 date 字段（YYYY.MM.DD 字符串，用于排序/展示）

原有 author / date 等字段保持不动。

用法：在仓库根目录执行  python tools/update_frontmatter.py
"""
import glob
import os


def yaml_quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def has_key(lines, key):
    return any(l == key or l.startswith(key + ':') for l in lines)


def process(path):
    with open(path, 'rb') as f:
        raw_bytes = f.read()
    bom = raw_bytes.startswith(b'\xef\xbb\xbf')
    text = raw_bytes.decode('utf-8-sig')
    nl = '\r\n' if '\r\n' in text else '\n'
    norm = text.replace('\r\n', '\n')
    lines = norm.split('\n')

    if not lines or lines[0].strip() != '---':
        print('SKIP (no front matter):', path)
        return False

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        print('SKIP (unclosed front matter):', path)
        return False

    fm = lines[1:end]
    body = lines[end + 1:]

    title = os.path.splitext(os.path.basename(path))[0]

    pubdate = None
    for l in fm:
        if l.startswith('date:'):
            pubdate = l.split(':', 1)[1].strip()
            if len(pubdate) >= 2 and pubdate[0] == pubdate[-1] and pubdate[0] in ('"', "'"):
                pubdate = pubdate[1:-1]
            break

    new_fm = []
    if not has_key(fm, 'title'):
        new_fm.append('title: ' + yaml_quote(title))
    if not has_key(fm, 'layout'):
        new_fm.append('layout: default')

    combined = new_fm + fm
    if pubdate and not has_key(fm, 'pubdate'):
        combined.append('pubdate: ' + yaml_quote(pubdate))

    new_norm = '---\n' + '\n'.join(combined) + '\n---\n' + '\n'.join(body)
    if nl == '\r\n':
        new_text = new_norm.replace('\n', '\r\n')
    else:
        new_text = new_norm
    new_bytes = (b'\xef\xbb\xbf' if bom else b'') + new_text.encode('utf-8')

    with open(path, 'wb') as f:
        f.write(new_bytes)
    return True


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    files = sorted(glob.glob('*.md'))
    written = 0
    for path in files:
        if process(path):
            written += 1
    print('scanned files:', len(files), '| written:', written)


if __name__ == '__main__':
    main()
