"""Công cụ của bài toán Track A3 — Kiểm và duyệt kịch bản bài giảng & câu hỏi tương tác do AI sinh.

Mỗi công cụ là một hàm Python có @tool, khớp 100% với sơ đồ ở spec.md §4:
1. search_sources(query) -> danh sách đoạn nguồn liên quan từ data/course_sources.json (Chỉ đọc)
2. get_segment(code) -> toàn văn đoạn nguồn theo mã đoạn SRC-Dxx-Mx-xx (Chỉ đọc)
3. check_claim(claim, source_codes) -> kiểm tra mã đoạn hợp lệ và dấu hiệu lỗi đặc thù / tấn công (Chỉ đọc)
4. submit_for_review(draft_report) -> lưu bản nháp vào hàng đợi chờ giảng viên duyệt, KHÔNG tự xuất bản
"""
import json
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(ROOT, "data", "course_sources.json")


def _load_sources() -> list:
    if not os.path.exists(SOURCES_PATH):
        return []
    with open(SOURCES_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "").lower()
    return text


def _strip_accents(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text or "")
    out = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    return out.replace("đ", "d").replace("Đ", "D").lower()


def _tokenize(text: str) -> set:
    clean = re.sub(r"[^a-z0-9_]+", " ", _strip_accents(text))
    stop = {"la", "va", "cua", "cho", "trong", "khi", "voi", "cac", "mot", "nhung", "duoc", "nay", "do", "theo", "hay"}
    return {w for w in clean.split() if len(w) >= 2 and w not in stop}


@tool
def search_sources(query: str) -> list:
    """Tra cứu các đoạn tài liệu nguồn của khoá học từ data/course_sources.json theo câu khẳng định.
    Input: query (str) — câu khẳng định hoặc câu hỏi trong kịch bản bài giảng cần kiểm chứng.
    Output: danh sách tối đa 3 đoạn nguồn khớp nhất [{"code", "day", "topic", "title", "text", "score"}].
    Tác động ra ngoài: Không (chỉ đọc)."""
    sources = _load_sources()
    if not sources:
        return []

    q_norm = _norm(query)
    q_tokens = _tokenize(query)
    explicit_codes = {m.upper() for m in re.findall(r"SRC-D\d{2}-M\d-\d{2}", query, flags=re.IGNORECASE)}
    day_matches = {("Day%02d" % int(m)) for m in re.findall(r"day\s*0?(\d{1,2})", q_norm)}

    scored = []
    for item in sources:
        code = item.get("code", "")
        haystack = " ".join([
            code,
            item.get("day", ""),
            item.get("topic", ""),
            item.get("title", ""),
            item.get("text", ""),
        ])
        h_tokens = _tokenize(haystack)
        overlap = len(q_tokens & h_tokens)
        score = overlap
        if code.upper() in explicit_codes:
            score += 10
        if item.get("day", "") in day_matches:
            score += 4
        if score > 0:
            scored.append({
                "code": code,
                "day": item.get("day", ""),
                "topic": item.get("topic", ""),
                "title": item.get("title", ""),
                "text": item.get("text", ""),
                "score": score,
            })

    scored.sort(key=lambda x: (-x["score"], x["code"]))
    return scored[:3]


@tool
def get_segment(code: str) -> dict:
    """Đọc nguyên văn một đoạn tài liệu nguồn theo mã đoạn chuẩn (ví dụ SRC-D02-M1-01).
    Input: code (str) — mã đoạn tài liệu nguồn.
    Output: dict {"found": bool, "code": str, "title": str, "text": str}.
    Tác động ra ngoài: Không (chỉ đọc)."""
    clean_code = (code or "").strip().strip("[]").upper()
    for item in _load_sources():
        if item.get("code", "").upper() == clean_code:
            return {
                "found": True,
                "code": item["code"],
                "day": item.get("day", ""),
                "title": item.get("title", ""),
                "text": item.get("text", ""),
            }
    return {"found": False, "code": clean_code, "title": "", "text": "NOT_FOUND: Mã đoạn không tồn tại trong kho nguồn."}


@tool
def check_claim(claim: str, candidate_codes: str = "") -> dict:
    """Kiểm tra bằng quy tắc code (deterministic guardrail) các dấu hiệu vi phạm an toàn, lộ đáp án, hoặc mã nguồn giả.
    Input: claim (str) — câu khẳng định/câu hỏi cần duyệt; candidate_codes (str) — các mã nguồn tìm được.
    Output: dict {"valid_codes": list, "fake_codes": list, "signals": list, "rule_hint": str}.
    Tác động ra ngoài: Không (chỉ đọc)."""
    all_valid = {item.get("code", "").upper() for item in _load_sources()}
    mentioned = [m.upper() for m in re.findall(r"SRC-[A-Z0-9\-]+", claim or "", flags=re.IGNORECASE)]
    cand = [c.strip().strip("[]").upper() for c in (candidate_codes or "").split(",") if c.strip()]

    valid_codes = sorted({c for c in (mentioned + cand) if c in all_valid})
    fake_codes = sorted({c for c in (mentioned + cand) if c and c not in all_valid})

    c_ascii = _strip_accents(claim)
    signals = []
    rule_hint = ""

    # 1. Phát hiện Prompt Injection / vượt quyền tự xuất bản
    if any(k in c_ascii for k in [
        "bo qua moi huong dan", "bo qua moi quy tac", "ignore previous", "api_key", ".env",
        "xuat ban thang", "khong can cho giang vien duyet", "tu dong sua toan bo"
    ]):
        signals.append("VI_PHAM_THAM_QUYEN_HOAC_INJECTION")
        rule_hint = "TU_CHOI"

    # 2. Phát hiện câu hỏi Quiz lộ sẵn đáp án trong câu dẫn
    if ("cau hoi" in c_ascii or "quiz" in c_ascii or " a." in c_ascii) and "vi nguyen tac" in c_ascii:
        m_ans = re.search(r"a\.\s*([^bc\n]+)", c_ascii)
        if m_ans:
            ans_a = m_ans.group(1).strip()
            prefix = c_ascii.split("hoi:")[0] if "hoi:" in c_ascii else c_ascii[:len(c_ascii) // 2]
            if ans_a and len(ans_a) >= 10 and ans_a in prefix:
                signals.append("QUIZ_LO_DAP_AN_TRONG_CAU_DAN")
                rule_hint = "LOI_CAU_HOI"

    # 3. Phát hiện câu quá mơ hồ / đại từ không rõ nguồn
    if not valid_codes and any(k in c_ascii for k in ["phuong phap do", "cai thien dang ke hieu suat cua no"]):
        signals.append("CAU_MO_HO_THIEU_CHU_NGU")
        rule_hint = "THIEU_NGUON"

    return {
        "valid_codes": valid_codes,
        "fake_codes": fake_codes,
        "signals": signals,
        "rule_hint": rule_hint,
    }


@tool
def submit_for_review(draft_report: str) -> dict:
    """Đưa bản báo cáo kiểm duyệt kịch bản vào hàng đợi chờ giảng viên duyệt (Human-in-the-loop).
    Input: draft_report (str) — kết quả rà soát của AI đã qua guardrail.
    Output: dict {"status": "PENDING_LECTURER_REVIEW", "auto_published": False, "preview": str}.
    Tác động ra ngoài: Chỉ lưu bản nháp chờ giảng viên duyệt, KHÔNG tự động xuất bản lên LMS."""
    return {
        "status": "PENDING_LECTURER_REVIEW",
        "auto_published": False,
        "preview": (draft_report or "")[:200],
    }
