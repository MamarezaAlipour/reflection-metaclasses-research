# اسکریپت تصحیح کاراکترهای فارسی در فایل markdown
param(
    [string]$InputFile = "مقاله_کامل_بازتاب_متاکلاس_C++23.md",
    [string]$OutputFile = "مقاله_تصحیح_شده_نهایی.md"
)

Write-Host "خواندن فایل markdown..." -ForegroundColor Green

# خواندن محتوای فایل
$content = Get-Content $InputFile -Encoding UTF8 -Raw

Write-Host "تصحیح کاراکترهای مشکل‌دار..." -ForegroundColor Yellow

# تصحیح کاراکترهای مربعی و نامناسب
$fixes = @{
    # کاراکترهای مربعی
    '□' = ' '
    '■' = ''
    '▫' = ''
    '▪' = ''
    '◦' = ''
    '∎' = ''
    '☐' = ''
    '☑' = ''
    '☒' = ''
    
    # کاراکترهای غیرقابل نمایش
    'â€Œ' = ''
    'â€‹' = ''
    'ï»¿' = ''  # BOM
    'â€‍' = ''
    
    # تصحیح نیم‌فاصله‌های اضافی
    '‌‌+' = '‌'
    ' ‌' = ' '
    '‌ ' = ' '
    
    # تصحیح فاصله‌های اضافی
    '  +' = ' '
    '\n\s+\n' = "`n`n"
    
    # تصحیح علائم نگارشی
    '،،' = '،'
    '...' = '…'
    '!!!' = '!'
    '???' = '?'
}

foreach ($fix in $fixes.GetEnumerator()) {
    $content = $content -replace $fix.Key, $fix.Value
}

Write-Host "تصحیح بلوک‌های کد..." -ForegroundColor Yellow

# تصحیح کامنت‌های فارسی در کدها
$codeBlockPattern = '```cpp(.*?)```'
$content = [regex]::Replace($content, $codeBlockPattern, {
    param($match)
    $codeContent = $match.Groups[1].Value
    
    # تصحیح کامنت‌های فارسی
    $codeContent = $codeContent -replace '//\s*([ا-ی\s۰-۹]+)', '// $1'
    $codeContent = $codeContent -replace '/\*\s*([ا-ی\s۰-۹\n\r]+)\s*\*/', '/* $1 */'
    
    # حذف کاراکترهای غیرضروری از کد
    $codeContent = $codeContent -replace '□', ' '
    $codeContent = $codeContent -replace '■', ''
    
    return "``````cpp$codeContent``````"
}, [System.Text.RegularExpressions.RegexOptions]::Singleline)

Write-Host "تصحیح فرمت‌بندی..." -ForegroundColor Yellow

# تصحیح عناوین
$content = $content -replace '^(#+)\s*([^\n]+)', '$1 $2'

# تصحیح فهرست‌ها
$content = $content -replace '^\s*[-*+]\s+', '- '
$content = $content -replace '^\s*(\d+\.)\s+', '$1 '

# تصحیح جداول
$content = $content -replace '\|\s*\|', '|'
$content = $content -replace '\s*\|\s*', ' | '

Write-Host "ذخیره فایل تصحیح شده..." -ForegroundColor Green

# ذخیره فایل
$content | Out-File -FilePath $OutputFile -Encoding UTF8 -NoNewline

if (Test-Path $OutputFile) {
    $fileSize = (Get-Item $OutputFile).Length
    Write-Host "فایل تصحیح شده ایجاد شد: $OutputFile" -ForegroundColor Green
    Write-Host "حجم فایل: $([math]::Round($fileSize / 1KB, 2)) KB" -ForegroundColor Cyan
} else {
    Write-Host "خطا در ایجاد فایل!" -ForegroundColor Red
}

return $OutputFile
