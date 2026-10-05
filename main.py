"""
=========================================================
   viua Python — Web Server (main.py)
   اجرای سایت روی سرور محلی + باز کردن خودکار مرورگر
=========================================================
"""

import http.server
import socketserver
import webbrowser
import os
import socket
import sys
import threading
import time


# ============ تنظیمات ============
PORT = 8000                    # پورت پیش‌فرض سرور
HTML_FILE = "index.html"       # نام فایل اصلی سایت
AUTO_OPEN = True               # باز کردن خودکار مرورگر
# ==================================


# ============ توابع کمکی ============

def get_local_ip():
    """گرفتن IP لوکال برای نمایش در موبایل و دستگاه‌های دیگر"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def find_free_port(start_port=8000, max_tries=20):
    """پیدا کردن پورت آزاد اگر پورت پیش‌فرض اشغال باشد"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    return None


def print_banner(url, port, ip):
    """نمایش بنر خوش‌آمد"""
    print()
    print("=" * 58)
    print("     🐍  viua Python — Web Server  🐍")
    print("=" * 58)
    print(f"  ✅  سرور با موفقیت اجرا شد!")
    print(f"  📁  پوشه سایت    :  {os.getcwd()}")
    print(f"  🌐  آدرس محلی    :  {url}")
    print(f"  📱  آدرس شبکه    :  http://{ip}:{port}/{HTML_FILE}")
    print(f"  🔌  پورت         :  {port}")
    print("-" * 58)
    print("  ⏹   برای توقف سرور، کلیدهای Ctrl + C را بزنید")
    print("=" * 58)
    print()


def open_browser_later(url, delay=1.2):
    """باز کردن مرورگر با تأخیر کم (بعد از آماده شدن سرور)"""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️  مرورگر به‌صورت خودکار باز نشد: {e}")
    threading.Thread(target=_open, daemon=True).start()


# ============ هندر سفارشی ============

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """هندر سفارشی برای نمایش زیباتر درخواست‌ها"""

    def log_message(self, format, *args):
        # لاگ ساده و رنگی در ترمینال
        method = args[0] if args else ""
        path = args[1] if len(args) > 1 else ""
        status = args[2] if len(args) > 2 else ""

        # فیلتر کردن درخواست‌های روت و فاوآیکون
        if path == "/" or "favicon" in path:
            icon = "🏠" if path == "/" else "🔖"
        elif path.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            icon = "🖼️ "
        elif path.endswith((".css",)):
            icon = "🎨"
        elif path.endswith((".js",)):
            icon = "📜"
        elif path.endswith((".html", ".htm")):
            icon = "📄"
        else:
            icon = "📎"

        print(f"  {icon}  [{method}]  {path}   →  {status}")

    def end_headers(self):
        # جلوگیری از کش شدن در حین توسعه
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


# ============ اجرای اصلی ============

def main():
    # تغییر مسیر به پوشه‌ی همین فایل
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # بررسی وجود فایل HTML
    if not os.path.exists(HTML_FILE):
        print()
        print("=" * 58)
        print(f"  ❌  فایل «{HTML_FILE}» پیدا نشد!")
        print("=" * 58)
        print(f"  📁  پوشه فعلی: {script_dir}")
        print(f"  📄  فایل‌های موجود:")
        for f in sorted(os.listdir(".")):
            print(f"        - {f}")
        print()
        print(f"  💡  لطفاً نام فایل HTML خود را در متغیر HTML_FILE تغییر دهید.")
        print("=" * 58)
        sys.exit(1)

    # پیدا کردن پورت آزاد
    global PORT
    free_port = find_free_port(PORT)
    if free_port is None:
        print(f"❌  هیچ پورت آزادی در محدوده {PORT} تا {PORT + 20} پیدا نشد.")
        sys.exit(1)
    PORT = free_port

    url = f"http://localhost:{PORT}/{HTML_FILE}"
    ip = get_local_ip()

    # ساخت و اجرای سرور
    try:
        handler = CustomHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print_banner(url, PORT, ip)

            if AUTO_OPEN:
                open_browser_later(url)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass

    except OSError as e:
        print(f"\n❌  خطا در اجرای سرور: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌  خطای غیرمنتظره: {e}")
        sys.exit(1)
    finally:
        print()
        print("=" * 58)
        print("  🛑  سرور متوقف شد. خدانگهدار! 🐍")
        print("=" * 58)
        print()


if __name__ == "__main__":
    main()
