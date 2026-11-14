#!/usr/bin/env python3
"""统计 JSONL 错误流水：类型分布、复发告警、近期记录摘要。

用法：
    python audit_errors.py --path errors.jsonl
    python audit_errors.py --path /abs/path/errors.jsonl --recent 10 --threshold 3
"""

import argparse
import collections
import json
import sys
from pathlib import Path


def load_rows(path):
    """逐行读取 JSONL，跳过空行，把坏行报出来但不中断统计。"""
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print("第 %d 行 JSON 非法：%s" % (lineno, exc), file=sys.stderr)
    return rows


def summarize(rows, threshold, recent):
    counter = collections.Counter(row.get("type", "UNLABELED") for row in rows)
    dates = sorted(row["date"] for row in rows if row.get("date"))

    print("总条数：%d" % len(rows))
    if dates:
        print("日期范围：%s 至 %s" % (dates[0], dates[-1]))
    print("")
    print("类型分布（降序）：")
    for label, count in counter.most_common():
        print("  %-12s %3d" % (label, count))

    escalated = [label for label, count in counter.items() if count >= threshold]
    print("")
    print("复发 >= %d 次，需升级为强制脚本：%s"
          % (threshold, ", ".join(sorted(escalated)) if escalated else "无"))

    print("")
    print("最近 %d 条：" % recent)
    for row in rows[-recent:]:
        claim = str(row.get("claim", "")).replace("\n", " ")[:90]
        print("  %s | %s | %s" % (row.get("date", "?"), row.get("id", "?"), claim))


def main():
    parser = argparse.ArgumentParser(description="统计错误流水的类型分布与复发次数")
    parser.add_argument("--path", default="errors.jsonl", help="JSONL 文件路径")
    parser.add_argument("--recent", type=int, default=5, help="列出最近 N 条")
    parser.add_argument("--threshold", type=int, default=3, help="复发告警阈值")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print("找不到文件：%s" % path, file=sys.stderr)
        return 1

    rows = load_rows(path)
    if not rows:
        print("文件内没有有效记录：%s" % path, file=sys.stderr)
        return 1

    summarize(rows, args.threshold, args.recent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
