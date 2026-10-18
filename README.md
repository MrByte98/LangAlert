<div align="center">

# ⚡ LangAlert — دستیار هوشمند تصحیح زبان کیبورد
### Intelligent Cross-Platform Keyboard Layout Mismatch Detection & Correction Utility

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-00f0ff.svg?style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-a855f7.svg?style=flat-square)](#)
[![GUI](https://img.shields.io/badge/GUI-PyQt6%20%7C%20Cyber%20Neon-ec4899.svg?style=flat-square)](#)
[![Engine](https://img.shields.io/badge/Engine-Character%20N--Gram%20Model-10b981.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](#)

[**فارسی (Persian)**](#-فارسی) • [**English**](#-english)

</div>

---

<a name="-فارسی"></a>
## 🇮🇷 راهنمای فارسی

### ۱. معرفی اجمالی پروژه
**LangAlert** یک ابزار پس‌زمینه (System Tray) سبک، سریع و کاملاً مدرن است که خطاهای ناشی از تایپ با چیدمان زبان اشتباه کیبورد (به‌ویژه میان دو زبان **فارسی ⮂ انگلیسی**) را در کسری از ثانیه شناسایی و تصحیح می‌کند.

در سیستم‌های چندزبانه بسیار پیش می‌آید که کیبورد سیستم روی انگلیسی است اما کاربر قصد تایپ متن فارسی داشته است (مثلاً تایپ ناخواسته **`sghl`** به جای **«سلام»**)، یا برعکس، کیبورد روی فارسی است ولی قصد تایپ انگلیسی بوده (مانند تایپ ناخواسته **`پخاشپپشی`** به جای **`mohammad`** یا **`اثممخ`** به جای **`hello`**).

**LangAlert** این خطا را بلافاصله تشخیص داده، با یک صدای زنگ ملایم هارمونیک و نمایش یک بج شیشه‌ای زیبا با تم **Cyber Neon Glassmorphism** در گوشه صفحه، متن اصلی و تبدیل‌شده را همراه با امکان **کپی فوری با ۱ کلیک** یا **جایگزینی مستقیم و خودکار در همان برنامه** در اختیار شما می‌گذارد.

---

### ۲. ویژگی‌های کلیدی و برجسته

* 🧠 **مدل آماری پیشرفته Character N-Gram (Trigram + Bigram):**
  - بی‌نیاز از فایل‌های حجیم و ایستا دیکشنری (با حجم مدل کمتر از ۱۰۰ کیلوبایت).
  - پوشش ۱۰۰٪ انواع کلمات عامیانه، نام‌های خاص (مانند `mohammad`, `reza`)، اصطلاحات اختصاری و کلمات جدید از طریق ارزیابی آماری توالی حروف (Perplexity Scoring).
* 🎯 **تشخیص هوشمند چیدمان فعال سیستم‌عامل (Active OS Layout Awareness):**
  - بررسی بلادرنگ زبان فعال پنجره پیش‌زمینه (Windows Win32 API / Linux X11-Wayland).
  - حذف کامل هشدارهای اشتباه (False Positives) زمانی که کاربر متنی فارسی را در چیدمان فارسی یا انگلیسی را در چیدمان انگلیسی تایپ می‌کند.
* 💎 **طراحی مدرن Cyber Neon Glassmorphism:**
  - فریم نئونی با حاشیه گرادیان فیروزه‌ای-بنفش (`#00f0ff` تا `#a855f7`).
  - تایپوگرافی چشم‌نواز با فونت استاندارد و زیبای **وزیر (Vazirmatn)**.
  - اسلایدرهای زنده تنظیم شفافیت پنجره (Window Opacity) و شفافیت اعلان شناور (Toast Opacity).
* 🔔 **اعلان شناور و بازخورد صوتی کریستالی:**
  - بج گوشه صفحه با شمارشگر معکوس و مکث هوشمند هنگام قرار گرفتن ماوس.
  - سنتز درون‌برنامه‌ای اصوات دلنشین (Crystal Chime، Subtle Bell، Modern Beep) بدون نیاز به فایل‌های صوتی حجیم خارجی.
* ⚙️ **داشبورد تنظیمات جامع و تاریخچه:**
  - تنظیم حساسیت (Low, Medium, High)، حداقل طول کلمه و کلیدهای تحریک (Space, Enter, Pause).
  - تب تاریخچه با امکان مرور و کپی دوباره تبدیل‌های قبلی.
  - محیط تست زنده (Live Playground) برای بررسی آنی کلمات.

---

### ۳. نصب و اجرای مستقیم (از طریق پایتون)

#### پیش‌نیازها:
* پایتون نسخه ۳.۱۰ یا بالاتر

```bash
# کلون یا دانلود مخزن
git clone https://github.com/your-username/auto_change.git
cd auto_change

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای برنامه (با باز شدن پنل تنظیمات در بار اول)
python run.py

# اجرای مستقیم در پس‌زمینه (Minimized در System Tray)
python run.py --minimized
```

---

### ۴. نحوه بیلد و ساخت فایل اجرایی مستقل (Standalone Build)

#### 🪟 بیلد ویندوز (Windows):
پروژه مجهز به اسکریپت بیلد کاملاً خودکار است:
```bash
# نصب PyInstaller
pip install pyinstaller

# اجرای اسکریپت بیلد
python build_standalone.py
```
* خروجی در پوشه `dist/LangAlert/LangAlert.exe` قرار می‌گیرد.
* همچنین فایل فشرده آماده انتشار `dist/LangAlert-windows-x64.zip` ایجاد می‌شود که بدون نیاز به پایتون روی هر سیستمی قابل اجراست.

#### 🐧 بیلد لینوکس (Linux):
در محیط‌های لینوکسی (Ubuntu, Debian, Fedora, Arch) کافی است اسکریپت بیلد لینوکس را اجرا کنید:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
* خروجی به شکل بسته مستقل `dist/packages/LangAlert-linux-x86_64.tar.gz` ایجاد خواهد شد.

#### 🚀 بیلد ابری همزمان (GitHub Actions CI/CD):
یک ورک‌فلو کامل در مسیر `.github/workflows/build.yml` قرار دارد که با هر Push یا Release، به طور همزمان روی ماشین‌های اوبونتو و ویندوز بیلد نیتیو گرفته و فایل‌های اجرایی را آماده دانلود می‌کند.

---

### ۵. تست سریع نمونه‌ها
کافیست برنامه را اجرا کرده و در هر نرم‌افزاری (Notepad، مرورگر، تلگرام و...) عبارت‌های زیر را تایپ کنید:
* تایپ `sghl` ➔ اعلان تبدیل به **«سلام»**
* تایپ `o,fd` ➔ اعلان تبدیل به **«خوبی»**
* تایپ `sghl ]x,vd` ➔ اعلان تبدیل به **«سلام چطوری»**
* تایپ `پخاشپپشی` ➔ اعلان تبدیل به **`mohammad`**
* تایپ `اثممخ` ➔ اعلان تبدیل به **`hello`**
* تایپ `فثسف` ➔ اعلان تبدیل به **`test`**
* تایپ `صخقمی` ➔ اعلان تبدیل به **`world`**

---

<br/>

---

<a name="-english"></a>
## 🇬🇧 English Guide

### 1. Project Overview
**LangAlert** is a lightweight, responsive, and cross-platform desktop background utility (System Tray) designed to instantly detect and correct keyboard layout mismatches (specifically between **Persian ⮂ English**).

In multilingual desktop environments, users frequently start typing without looking at the active language indicator. You might intend to type Persian while the layout is English (e.g. typing **`sghl`** instead of **`سلام`**), or type English while the keyboard is set to Persian (e.g. typing **`پخاشپپشی`** instead of **`mohammad`** or **`اثممخ`** instead of **`hello`**).

**LangAlert** detects this in milliseconds, plays an unobtrusive harmonic audio chime, and displays an elegant floating **Cyber Neon Glassmorphism** alert badge with **1-Click Copy** and **Direct In-Place Auto-Replace**.

---

### 2. Key Features

* 🧠 **Statistical Character N-Gram Engine (Trigram + Bigram):**
  - Replaces heavy, static wordlists with compact (<100 KB) transition probability matrices.
  - 100% coverage for arbitrary text, slang, names (e.g., `mohammad`, `reza`), and novel words using perplexity scoring.
* 🎯 **Active OS Foreground Window Layout Awareness:**
  - Inspects active foreground window keyboard layout in real-time (Windows Win32 API & Linux X11/Wayland).
  - Eliminates false positives when legitimately typing Persian in Persian layout or English in English layout.
* 💎 **Cyber Neon Glassmorphism Aesthetic:**
  - Modern glowing cyan-to-purple gradient border (`#00f0ff` to `#a855f7`).
  - Persian typography powered by bundled **Vazirmatn** fonts.
  - Interactive sliders for real-time Window Opacity and Toast Opacity adjustment.
* 🔔 **Floating Toast Badge & Harmonic Audio Chimes:**
  - Floating badge with a countdown progress bar, pause-on-hover, and smooth fade animation.
  - Clean synthesized chimes (*Crystal Chime*, *Subtle Bell*, *Modern Beep*) generated on-the-fly without external sound assets.
* ⚙️ **Comprehensive Settings & History Dashboard:**
  - Customizable sensitivity, trigger keys (Space, Enter, Pause), and word length thresholds.
  - History tab with quick re-copy capability.
  - Interactive Live Playground for instant conversion testing.

---

### 3. Installation & Direct Run (Python)

#### Prerequisites:
* Python 3.10 or later

```bash
# Clone the repository
git clone https://github.com/your-username/auto_change.git
cd auto_change

# Install dependencies
pip install -r requirements.txt

# Run the application (opens settings dashboard on launch)
python run.py

# Run directly in background (System Tray mode)
python run.py --minimized
```

---

### 4. Standalone Executable Packaging

#### 🪟 Windows Build:
Package into a standalone folder and `.zip` archive (no Python required on target machine):
```bash
pip install pyinstaller
python build_standalone.py
```
* Output binary: `dist/LangAlert/LangAlert.exe`
* Distributable zip: `dist/LangAlert-windows-x64.zip`

#### 🐧 Linux Build:
On any Linux distribution (Ubuntu, Debian, Fedora, Arch):
```bash
chmod +x build_linux.sh
./build_linux.sh
```
* Output archive: `dist/packages/LangAlert-linux-x86_64.tar.gz`

#### 🚀 Automated Multiplatform CI/CD:
The repository includes a ready-to-use GitHub Actions workflow at `.github/workflows/build.yml`. On push or tag, native Windows (`.zip`) and Linux (`.tar.gz`) binaries are built and uploaded automatically.

---

### 5. Project Structure

```
auto_change/
├── run.py                     # Application entry point
├── build_standalone.py        # Windows/universal PyInstaller packaging script
├── build_linux.sh             # Linux standalone build script
├── requirements.txt           # Python dependencies
├── README.md                  # Bilingual documentation
├── .github/workflows/
│   └── build.yml              # GitHub Actions CI/CD for automated builds
├── tests/                     # Automated test suites
│   ├── test_integration.py
│   ├── test_layout_scenarios.py
│   └── test_ngram_evaluation.py
└── langswitch/                # Core application package
    ├── config.py              # Configuration storage & AppData paths
    ├── converter.py           # Keyboard layout coordinate mapping
    ├── detector.py            # Intelligent mismatch detection logic
    ├── layout_detector.py     # Real-time active OS keyboard layout detector
    ├── ngram_model.py         # Statistical Trigram/Bigram perplexity engine
    ├── keyboard_listener.py   # Global keystroke hook & in-place text replacer
    ├── sound_player.py        # Zero-latency harmonic audio synthesizer
    ├── dictionaries/          # Compact N-gram transition matrices
    └── ui/
        ├── styles.py          # Cyber Neon Glassmorphism stylesheet
        ├── neon_frame.py      # Custom gradient-bordered glass widget
        ├── toast_badge.py     # Floating top-right glassmorphic alert badge
        ├── settings_window.py # Settings dashboard, history & playground
        └── tray_icon.py       # Cross-platform System Tray integration
```

---

### 6. Quick Test Examples
With the application running, type any of the following sequences in any editor or messenger:
* Type `sghl` ➔ Alerts and converts to **`سلام`**
* Type `o,fd` ➔ Alerts and converts to **`خوبی`**
* Type `sghl ]x,vd` ➔ Alerts and converts to **`سلام چطوری`**
* Type `پخاشپپشی` ➔ Alerts and converts to **`mohammad`**
* Type `اثممخ` ➔ Alerts and converts to **`hello`**
* Type `فثسف` ➔ Alerts and converts to **`test`**
* Type `صخقمی` ➔ Alerts and converts to **`world`**

---

### 📄 License
This project is open-source under the [MIT License](LICENSE).
