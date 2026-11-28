"""Khung chạy bản chạy thử (dòng lệnh): gõ đầu vào → answer() trong agent.py → in kết quả.

Chạy bằng: python run.py   (hoặc giao diện web: python ui/server.py)
Nâng cấp sau CP4 (từ góp ý của người dùng thử U1 & U2 trong validation/log.md):
- Hỗ trợ gõ `/multi` để dán nguyên kịch bản nhiều dòng (kết thúc bằng một dòng trống) mà không bị tách thành nhiều lượt chạy.
- Hỗ trợ gõ `/demo` để chạy nhanh kịch bản bài giảng mẫu có cả [Slide 1], [Lời giảng], [Slide 2], [Slide 3].
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SAMPLE_SLIDE_SCRIPT = (
    "[Slide 1 - Kiến trúc ứng dụng AI] Một sản phẩm AI là ứng dụng phần mềm bọc quanh model với hợp đồng dữ liệu đầu vào đầu ra rõ ràng (structured output). "
    "[Lời giảng Slide 1] Khi quy trình xử lý đã biết trước các bước cố định, nhóm nên ưu tiên chọn Workflow cố định thay vì Multi-Agent để tiết kiệm chi phí và dễ đo kiểm. "
    "[Slide 2 - Thống kê thị trường] Theo báo cáo của McKinsey năm 2026, 94% hệ thống Multi-Agent giúp tăng gấp 3 lần doanh thu cho doanh nghiệp EdTech. "
    "[Slide 3 - Quy tắc chọn mức tự động] Với tác vụ có hậu quả sai sót rất đắt như tự động xuất bản bài giảng, nhóm bắt buộc phải chọn mức AI tự làm hoàn toàn mà không cần người duyệt."
)


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path


def main() -> int:
    try:
        import tracing
        from agent import answer
    except Exception as e:
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print("Bản chạy thử Track A3 (Kiểm duyệt kịch bản & slide bài giảng AI).")
    print("  • Gõ 1 câu hoặc cả đoạn kịch bản rồi Enter (giao diện Web trực quan: python ui/server.py).")
    print("  • Gõ /multi để dán kịch bản nhiều dòng (nhấn Enter ở dòng trống để chạy 1 lượt).")
    print("  • Gõ /demo để chạy kịch bản mẫu gồm [Slide 1] + [Lời giảng] + [Slide 2] + [Slide 3].")
    print("  • Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).")
    blank = 0
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        if text.lower() == "/multi":
            print("  (Chế độ nhiều dòng: dán kịch bản vào dưới đây, kết thúc bằng 1 dòng trống):")
            buf = []
            while True:
                try:
                    ln = input("  | ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if not ln:
                    break
                buf.append(ln)
            text = " ".join(buf).strip()
            if not text:
                continue
        elif text.lower() == "/demo":
            text = SAMPLE_SLIDE_SCRIPT
            print("  [Đầu vào /demo]: %s\n" % text)

        tracing.begin("app")
        try:
            result = answer(text)
        except NotImplementedError as e:
            tracing.end()
            print("Chưa nối model: %s" % e)
            return 1
        except Exception as e:
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


if __name__ == "__main__":
    sys.exit(main())
