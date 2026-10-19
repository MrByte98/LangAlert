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

### ۳. دریافت، نصب و اجرای مستقیم (از طریق پایتون)

#### پیش‌نیازها:
* پایتون نسخه ۳.۱۰ یا بالاتر

```bash
# کلون مخزن رسمی برنامه
git clone https://github.com/MrByte98/LangAlert.git
cd LangAlert

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای برنامه (با باز شدن پنل تنظیمات در بار اول)
python run.py

# اجرای مستقیم در پس‌زمینه (Minimized در System Tray)
python run.py --minimized
```

---

### ۴. بسته‌های نصبی و فایل‌های اجرایی مستقل (Standalone & Packages)

#### 🪟 ویندوز (Windows):
پروژه مجهز به اسکریپت بیلد کاملاً خودکار جهت تولید تک‌فایل نصبی و پرتابل است:
* **تک‌فایل نصبی استاندارد (`LangAlert-Setup.exe`):**
  با اجرای این فایل، برنامه به صورت خودکار در مسیر کاربری نصب شده، آیکون ⚡ روی دسکتاپ و منوی استارت ایجاد می‌گردد و در بخش Programs ویندوز (جهت حذف آسان در آینده) ثبت می‌شود.
* **تک‌فایل بدون نیاز به نصب (`LangAlert.exe`):**
  یک باینری کاملاً مستقل (Portable) که بدون نیاز به نصب یا استخراج، با دو بار کلیک مستقیماً اجرا می‌شود.

برای بیلد مجدد در ویندوز:
```bash
pip install pyinstaller pillow
python build_standalone.py
```
* خروجی‌های ویندوز:
  - فایل نصبی: `dist/LangAlert-Setup.exe`
  - فایل پرتابل: `dist/LangAlert.exe`

#### 🐧 لینوکس (Linux / Debian / Ubuntu):
برای کاربران لینوکس، هم پکیج استاندارد دبیان (`.deb`) و هم باینری پرتابل آماده است:
* **بسته نصبی دبیان/اوبونتو (`langalert_1.0.0_amd64.deb`):**
  نصب آسان در اوبونتو، دبیان، مینت و سایر توزیع‌های مبتنی بر دبیان با دستور:
  ```bash
  sudo dpkg -i langalert_1.0.0_amd64.deb
  ```
  این بسته برنامه را به منوی برنامه‌ها (Application Menu) همراه با آیکون ⚡ و به مسیر `/usr/bin/langalert` اضافه می‌کند.

برای بیلد بسته‌ها در لینوکس:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
* خروجی‌های لینوکس:
  - بسته نصبی: `dist/packages/langalert_1.0.0_amd64.deb`
  - آرشیو فشرده مستقل: `dist/packages/LangAlert-linux-x86_64.tar.gz`

#### 🚀 خط لوله خودکار CI/CD (GitHub Actions):
یک ورک‌فلو کامل در مسیر `.github/workflows/build.yml` فعال است که با هر انتشار یا کامیت روی گیت‌هاب، فایل‌های `LangAlert-Setup.exe`، `LangAlert.exe` و `langalert_1.0.0_amd64.deb` را به صورت خودکار بیلد کرده و برای دانلود قرار می‌دهد.

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
# Clone official repository
git clone https://github.com/MrByte98/LangAlert.git
cd LangAlert

# Install dependencies
pip install -r requirements.txt

# Run the application (opens settings dashboard on launch)
python run.py

# Run directly in background (System Tray mode)
python run.py --minimized
```

---

### 4. Standalone Packages & Installers

#### 🪟 Windows:
Automated single-file installer and portable binary generation:
* **Single-File Setup Installer (`LangAlert-Setup.exe`):**
  Installs the application into `%LOCALAPPDATA%\Programs\LangAlert\`, creates ⚡ Desktop & Start Menu shortcuts, and registers in Windows Apps & Features for clean uninstallation.
* **Single Portable Executable (`LangAlert.exe`):**
  A self-contained standalone binary that runs immediately without installation.

To build on Windows:
```bash
pip install pyinstaller pillow
python build_standalone.py
```
* Output files:
  - Setup Installer: `dist/LangAlert-Setup.exe`
  - Portable Executable: `dist/LangAlert.exe`

#### 🐧 Linux (Debian / Ubuntu / Generic):
* **Debian/Ubuntu Package (`langalert_1.0.0_amd64.deb`):**
  Install natively using:
  ```bash
  sudo dpkg -i langalert_1.0.0_amd64.deb
  ```
  Integrates with your system's Application Menu with the ⚡ icon and symlinks to `/usr/bin/langalert`.

To build on Linux:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
* Output packages:
  - Debian package: `dist/packages/langalert_1.0.0_amd64.deb`
  - Standalone tar.gz: `dist/packages/LangAlert-linux-x86_64.tar.gz`

#### 🚀 Automated Multiplatform CI/CD:
The repository includes a GitHub Actions workflow at `.github/workflows/build.yml`. On push or tag, native Windows (`LangAlert-Setup.exe`, `LangAlert.exe`) and Linux (`.deb`, `.tar.gz`) binaries are compiled and released automatically.

---

### 5. Project Structure

```
LangAlert/
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
