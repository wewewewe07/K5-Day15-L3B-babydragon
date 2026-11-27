# TUỲ CHỌN, chỉ cho máy có sẵn make. Lệnh chính là `python run.py …` (chạy được cả trên Windows).
# Makefile này chỉ gọi lại run.py, không làm gì thêm.
PY ?= python3
run: ; $(PY) run.py
check: ; $(PY) run.py check
eval: ; $(PY) run.py eval
eval-try: ; $(PY) run.py eval --try
score: ; $(PY) run.py score $(RUN)
simulate: ; $(PY) run.py simulate
simulate-try: ; $(PY) run.py simulate --try
.PHONY: run check eval eval-try score simulate simulate-try
