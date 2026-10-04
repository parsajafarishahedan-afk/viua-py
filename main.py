import http.server
import socketserver
import webbrowser
import os

# ===== تنظیمات =====
PORT = 8000                     # پورت سرور (می‌توانید تغییر دهید)
HTML_FILE = "index.html"        # نام فایل HTML شما

# ===== تغییر مسیر به پوشه فعلی =====
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ===== بررسی وجود فایل HTML =====
if not os.path.exists(HTML_FILE):
    print(f"❌ فایل {HTML_FILE} پیدا نشد!")
    print("لطفاً نام فایل HTML خود را در متغیر HTML_FILE وارد کنید.")
    exit()

# ===== ساخت سرور =====
Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/{HTML_FILE}"
        print("=" * 50)
        print(f"✅ سرور با موفقیت اجرا شد!")
        print(f"🌐 آدرس سایت شما: {url}")
        print(f"📁 پوشه فعلی: {os.getcwd()}")
        print("=" * 50)
        print("برای توقف سرور، کلید Ctrl+C را فشار دهید.")
        print("=" * 50)

        # باز کردن خودکار مرورگر
        webbrowser.open(url)

        # اجرای دائمی سرور
        httpd.serve_forever()

except KeyboardInterrupt:
    print("\n🛑 سرور متوقف شد.")
except OSError as e:
    print(f"❌ خطا: {e}")
    print(f"احتمالاً پورت {PORT} اشغال است. یک پورت دیگر امتحان کنید.")