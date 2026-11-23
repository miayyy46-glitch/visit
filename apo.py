import os
from datetime import datetime
from flask import Flask, render_template_string, request

app = Flask(__name__)

# صفحة الزائر العادية
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>مرحباً</title></head>
<body>
    <h2>تم الدخول بنجاح</h2>
    <p>الوقت: <strong>{{ visit_time }}</strong></p>
    <p>عنوان IP: <strong>{{ visitor_ip }}</strong></p>
</body>
</html>
"""


# 1. رابط الزوار (الذي تشاركه مع الناس)
@app.route("/visit")
def track_visit():
  current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  visitor_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

  # حفظ الوقت والـ IP في ملف نصي حقيقي
  with open("visits_log.txt", "a", encoding="utf-8") as file:
    file.write(f"الوقت: {current_time} | IP: {visitor_ip}\n")

  return render_template_string(
      HTML_PAGE, visit_time=current_time, visitor_ip=visitor_ip
  )


# 2. رابطك السري أنت فقط لقراءة محتوى الملف النصي
@app.route("/my-secret-logs")
def view_logs():
  if os.path.exists("visits_log.txt"):
    with open("visits_log.txt", "r", encoding="utf-8") as file:
      content = file.read()
    # عرض محتوى الملف كما هو في المتصفح
    return f"<pre style='font-size:16px; direction:ltr;'>{content}</pre>"
  else:
    return "لا توجد زيارات مسجلة في الملف حتى الآن."


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
