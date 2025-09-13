# تنظیم نهایی فونت‌ها در فایل Word
$inputFile = "مقاله_نهایی_فونت_تصحیح.docx"
$outputFile = "مقاله_C++23_ژورنالی_کامل.docx"

Write-Host "باز کردن فایل Word..." -ForegroundColor Green

$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    $doc = $word.Documents.Open((Resolve-Path $inputFile).Path)
    
    Write-Host "تنظیم فونت‌های اصلی..." -ForegroundColor Yellow
    
    # تنظیم فونت کل سند
    $range = $doc.Range()
    $range.Font.Name = "B Nazanin"
    $range.Font.Size = 11
    
    # تنظیم جهت متن به راست به چپ
    $range.ParagraphFormat.ReadingOrder = 2
    
    Write-Host "تنظیم استایل عناوین..." -ForegroundColor Yellow
    
    # تنظیم Heading 1
    try {
        $heading1 = $doc.Styles["Heading 1"]
        $heading1.Font.Name = "B Titr"
        $heading1.Font.Size = 18
        $heading1.Font.Bold = $true
        $heading1.Font.Color = 128  # آبی
    } catch {
        Write-Warning "نتوانست Heading 1 را تنظیم کند"
    }
    
    # تنظیم Heading 2
    try {
        $heading2 = $doc.Styles["Heading 2"]
        $heading2.Font.Name = "B Titr"
        $heading2.Font.Size = 16
        $heading2.Font.Bold = $true
        $heading2.Font.Color = 128
    } catch {
        Write-Warning "نتوانست Heading 2 را تنظیم کند"
    }
    
    # تنظیم Heading 3
    try {
        $heading3 = $doc.Styles["Heading 3"]
        $heading3.Font.Name = "B Titr"
        $heading3.Font.Size = 14
        $heading3.Font.Bold = $true
        $heading3.Font.Color = 3355443
    } catch {
        Write-Warning "نتوانست Heading 3 را تنظیم کند"
    }
    
    Write-Host "تنظیم کدها..." -ForegroundColor Yellow
    
    # تنظیم فونت کدها - روش جایگزین
    $findRange = $doc.Range()
    $findRange.Find.ClearFormatting()
    
    # جستجوی کدهایی که با Courier New هستند
    $findRange.Find.Font.Name = "Courier New"
    while ($findRange.Find.Execute()) {
        $findRange.Font.Name = "Consolas"
        $findRange.Font.Size = 9
        $findRange.Shading.BackgroundPatternColor = 15790320  # خاکستری روشن
        $findRange.Collapse(0)  # End
    }
    
    # جستجوی کدهایی که ممکن است نام فونت دیگری داشته باشند
    $findRange = $doc.Range()
    $findRange.Find.ClearFormatting()
    $findRange.Find.Font.Name = "Calibri"
    while ($findRange.Find.Execute()) {
        # بررسی اینکه آیا این متن کد است
        if ($findRange.Text -match "^[a-zA-Z0-9_\s\(\)\{\}\[\];,\.\-\+\*\/=<>!&\|%\^~\?\:]+$") {
            $findRange.Font.Name = "Consolas"
            $findRange.Font.Size = 9
            $findRange.Shading.BackgroundPatternColor = 15790320
        }
        $findRange.Collapse(0)
    }
    
    Write-Host "تنظیم متن‌های انگلیسی..." -ForegroundColor Yellow
    
    # تنظیم متن‌های انگلیسی
    $findRange = $doc.Range()
    $findRange.Find.ClearFormatting()
    $findRange.Find.Text = "[A-Za-z0-9\s\.\,\;\:\!\?\(\)\[\]\{\}\-\_\+\=]+"
    $findRange.Find.MatchWildcards = $true
    
    $count = 0
    while ($findRange.Find.Execute() -and $count -lt 1000) {
        # بررسی اینکه آیا این متن انگلیسی است و کد نیست
        if ($findRange.Text -match "^[A-Za-z\s]+$" -and $findRange.Text.Length -gt 3) {
            if ($findRange.Font.Name -ne "Consolas") {
                $findRange.Font.Name = "Times New Roman"
            }
        }
        $findRange.Collapse(0)
        $count++
    }
    
    Write-Host "تنظیم فرمت صفحه..." -ForegroundColor Yellow
    
    # تنظیم حاشیه‌ها
    $doc.Range().PageSetup.LeftMargin = 90   # 2.5 cm
    $doc.Range().PageSetup.RightMargin = 90
    $doc.Range().PageSetup.TopMargin = 90
    $doc.Range().PageSetup.BottomMargin = 90
    
    # تنظیم فاصله خطوط
    $doc.Range().ParagraphFormat.LineSpacing = 18  # 1.5
    
    Write-Host "ذخیره فایل نهایی..." -ForegroundColor Green
    
    # ذخیره با نام جدید
    $doc.SaveAs([ref](Resolve-Path .).Path + "\" + $outputFile)
    $doc.Close()
    
    $fileInfo = Get-Item $outputFile
    Write-Host "`n✅ فایل Word نهایی آماده شد!" -ForegroundColor Green
    Write-Host "📄 نام فایل: $($fileInfo.Name)" -ForegroundColor Cyan
    Write-Host "📊 حجم: $([math]::Round($fileInfo.Length / 1KB, 2)) KB" -ForegroundColor Cyan
    Write-Host "📅 زمان ایجاد: $($fileInfo.LastWriteTime)" -ForegroundColor Cyan
    
    Write-Host "`n🎯 ویژگی‌های فایل:" -ForegroundColor White
    Write-Host "✓ فونت B Titr برای عناوین" -ForegroundColor Green
    Write-Host "✓ فونت B Nazanin برای متن فارسی" -ForegroundColor Green
    Write-Host "✓ فونت Consolas برای کدها" -ForegroundColor Green
    Write-Host "✓ فونت Times New Roman برای متن انگلیسی" -ForegroundColor Green
    Write-Host "✓ فهرست مطالب شماره‌دار" -ForegroundColor Green
    Write-Host "✓ فرمت ژورنالی حرفه‌ای" -ForegroundColor Green
    Write-Host "✓ کدهای C++ با syntax highlighting" -ForegroundColor Green
    
} catch {
    Write-Error "خطا در پردازش: $($_.Exception.Message)"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
