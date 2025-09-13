# EasyCLI
یه کتابخونه ساده برای ساخت ابزارهای خط فرمان (CLI) در پایتون.

## نصب
```bash
pip install easycli
```

## مثال ساده
```python
from easycli import CLI

app = CLI("myapp")

@app.command("greet")
def greet(name: str):
    print(f"سلام، {name}!")

if __name__ == "__main__":
    app.run()
```

## مثال پیشرفته با گروه‌ها و پرچم‌ها
```python
app = CLI("myapp")

user_group = app.group("user")

@user_group.command("add")
def add(username: str, age: int = 18, admin: bool = False):
    print(f"اضافه شد: {username}, سن: {age}, ادمین: {admin}")
```

اجرا:
```bash
$ myapp user add Bob --age 30 --admin
```

## قابلیت‌ها
- دستورات ساده و چندسطحی
- پرچم‌های بلند/کوتاه با مقادیر پیش‌فرض
- اعتبارسنجی آرگومان‌ها
- راهنمای خودکار (--help)

## لایسنس
MIT