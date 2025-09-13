# اسکریپت حل مشکل کاراکترهای فارسی و ایجاد فایل Word ژورنالی
param(
    [string]$InputMarkdown = "مقاله_کامل_بازتاب_متاکلاس_C++23.md",
    [string]$OutputWord = "مقاله_ژورنالی_نهایی.docx"
)

Write-Host "شروع پردازش مقاله..." -ForegroundColor Green

# مرحله 1: خواندن فایل markdown و تصحیح مشکلات کدها
$content = Get-Content $InputMarkdown -Encoding UTF8 -Raw

Write-Host "تصحیح مشکلات کاراکترهای فارسی در کدها..." -ForegroundColor Yellow

# جایگزینی کاراکترهای مربعی با کاراکترهای فارسی صحیح
$persianFixes = @{
    '□' = ' '
    '■' = ''
    '▫' = ''
    '▪' = ''
    '◦' = ''
    '‌' = ''  # نیم‌فاصله
    'â€Œ' = ''
    'ï»¿' = ''  # BOM
}

foreach ($fix in $persianFixes.GetEnumerator()) {
    $content = $content -replace [regex]::Escape($fix.Key), $fix.Value
}

# تصحیح کامنت‌های فارسی در کدها
$content = $content -replace '//\s*([ا-ی\s]+)', '// $1'
$content = $content -replace '/\*\s*([ا-ی\s\n\r]+)\s*\*/', '/* $1 */'

# تصحیح فاصله‌های اضافی
$content = $content -replace '\s+', ' '
$content = $content -replace '\n\s+\n', "`n`n"

# ذخیره فایل تصحیح شده
$fixedFile = "مقاله_تصحیح_شده.md"
$content | Out-File -FilePath $fixedFile -Encoding UTF8

Write-Host "ایجاد فایل HTML با استایل ژورنالی..." -ForegroundColor Yellow

# ایجاد HTML با استایل کامل
$htmlTemplate = @"
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بازتاب و متاکلاس‌ها در C++23</title>
    <style>
$(Get-Content "journal_style.css" -Raw)
    </style>
</head>
<body class="docx-compatible">
    <div class="title">بازتاب و متاکلاس‌ها در ++C23: طراحی و پیاده‌سازی</div>
    <div class="subtitle">مطالعه جامع بر روی سیستم بازتاب و الگوی متاکلاس در استاندارد جدید ++C</div>
    
    <div class="author">نویسنده اول، نویسنده دوم</div>
    <div class="affiliation">دانشگاه علوم کامپیوتر، انستیتوی تحقیقات فناوری</div>
    
    <div class="abstract">
        <div class="abstract-title">چکیده</div>
        این مقاله به بررسی جامع سیستم بازتاب (Reflection) و الگوی متاکلاس (Metaclass) در استاندارد جدید ++C23 می‌پردازد. با معرفی قابلیت‌های جدید زبان، این تحقیق راه‌حل‌های نوآورانه‌ای برای مشکلات برنامه‌نویسی متاپروگرمینگ ارائه می‌دهد.
    </div>
    
    <div class="keywords">
        <span class="keywords-title">کلمات کلیدی:</span>
        بازتاب، متاکلاس، ++C23، متاپروگرمینگ، کامپایل تایم
    </div>

CONTENT_PLACEHOLDER
</body>
</html>
"@

# تبدیل markdown به HTML
pandoc $fixedFile -t html --highlight-style=pygments | Out-String | ForEach-Object {
    $htmlTemplate -replace "CONTENT_PLACEHOLDER", $_
} | Out-File -FilePath "مقاله_نهایی_ژورنالی.html" -Encoding UTF8

Write-Host "تبدیل HTML به Word..." -ForegroundColor Yellow

# تبدیل HTML به Word با تنظیمات حرفه‌ای
pandoc "مقاله_نهایی_ژورنالی.html" `
    --from=html `
    --to=docx `
    --output=$OutputWord `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --highlight-style=pygments `
    --reference-doc="reference.docx"

if (Test-Path $OutputWord) {
    Write-Host "فایل Word با موفقیت ایجاد شد: $OutputWord" -ForegroundColor Green
    
    # نمایش اطلاعات فایل
    $fileInfo = Get-Item $OutputWord
    Write-Host "حجم فایل: $([math]::Round($fileInfo.Length / 1KB, 2)) KB" -ForegroundColor Cyan
    Write-Host "زمان ایجاد: $($fileInfo.LastWriteTime)" -ForegroundColor Cyan
} else {
    Write-Host "خطا در ایجاد فایل Word!" -ForegroundColor Red
}

Write-Host "پردازش کامل شد!" -ForegroundColor Green
