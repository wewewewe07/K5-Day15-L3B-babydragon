"""Script tái lập toàn bộ số liệu đào data từ data/preclass/ cho Track A3.
Chạy lệnh:
    python evidence/count.py --data-dir ../data/preclass
Người khác chạy lại trên bộ data/preclass/ của BTC sẽ ra chính xác cùng con số x/N và %.
"""
import argparse
import sys
import csv
import json
import os
from collections import Counter, defaultdict


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=os.path.join("..", "data", "preclass"),
                        help="Đường dẫn tới thư mục data/preclass của BTC")
    args = parser.parse_args()
    d = args.data_dir
    if not os.path.isdir(d):
        print("Không tìm thấy thư mục %s. Hãy truyền --data-dir trỏ tới data/preclass/" % d)
        return 1

    # 1. Đếm agent_replied: missing_context và moc_trich_dan
    ar_total = 0
    mc_known = 0
    mc_true = 0
    mtd_known = 0
    mtd_empty = 0
    seek_total = 0
    seek_users = set()

    with open(os.path.join(d, "events.csv"), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = row.get("type", "")
            if t == "video_seeked":
                seek_total += 1
                seek_users.add(row.get("hv", ""))
            elif t == "agent_replied":
                ar_total += 1
                raw = row.get("data", "") or "{}"
                try:
                    payload = json.loads(raw)
                except ValueError:
                    payload = {}
                if "missing_context" in payload and payload["missing_context"] is not None:
                    mc_known += 1
                    if payload["missing_context"] is True:
                        mc_true += 1
                if "moc_trich_dan" in payload and payload["moc_trich_dan"] is not None:
                    mtd_known += 1
                    val = payload["moc_trich_dan"]
                    if (isinstance(val, list) and len(val) == 0) or not val:
                        mtd_empty += 1

    # 2. Đếm answers.csv: tỷ lệ sai lần đầu (lan_thu == 1) ở bài kiểm tra pre_post_post theo kc_code
    pp_first_total = 0
    pp_first_wrong = 0
    kc_total = Counter()
    kc_wrong = Counter()

    with open(os.path.join(d, "answers.csv"), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("nguon") == "pre_post_post" and str(row.get("lan_thu", "")).strip() == "1":
                wc = str(row.get("was_correct", "")).strip()
                if wc in ("True", "False"):
                    pp_first_total += 1
                    kc = row.get("kc_code", "") or "(trống)"
                    kc_total[kc] += 1
                    if wc == "False":
                        pp_first_wrong += 1
                        kc_wrong[kc] += 1

    print("=== KẾT QUẢ ĐÀO DỮ LIỆU PRE-CLASS CHO TRACK A3 ===")
    print("1. Lượt trả lời thiếu ngữ cảnh trong bài giảng (missing_context = True): %d / %d (%.1f%%)"
          % (mc_true, mc_known, mc_true * 100.0 / mc_known if mc_known else 0))
    print("2. Lượt trả lời không dẫn được mốc trích dẫn bài giảng (moc_trich_dan = []): %d / %d (%.1f%%)"
          % (mtd_empty, mtd_known, mtd_empty * 100.0 / mtd_known if mtd_known else 0))
    print("3. Lượt học viên phải tua video (video_seeked): %d lượt trên %d/436 học viên có hoạt động (%.1f%%)"
          % (seek_total, len(seek_users), len(seek_users) * 100.0 / 436.0))
    print("4. Lượt trả lời sai ngay lần đầu (lan_thu=1) ở câu hỏi ôn tập pre_post_post: %d / %d (%.1f%%)"
          % (pp_first_wrong, pp_first_total, pp_first_wrong * 100.0 / pp_first_total if pp_first_total else 0))
    print("5. Top 5 ý kiến thức (kc_code, N >= 15) có tỷ lệ học viên trả lời sai lần đầu cao nhất:")
    ranked = sorted([k for k, v in kc_total.items() if v >= 15],
                    key=lambda k: kc_wrong[k] * 1.0 / kc_total[k], reverse=True)
    for k in ranked[:5]:
        print("   - %s: %d / %d sai lần đầu (%.1f%%)"
              % (k, kc_wrong[k], kc_total[k], kc_wrong[k] * 100.0 / kc_total[k]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
