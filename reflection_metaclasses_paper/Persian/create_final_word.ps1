# ایجاد فایل Word نهایی با تمام تنظیمات
param(
    [string]$InputFile = "مقاله_تصحیح_شده_نهایی.md",
    [string]$OutputFile = "مقاله_C++23_حرفه‌ای_نهایی.docx"
)

Write-Host "شروع تبدیل به Word..." -ForegroundColor Green

# ایجاد فایل Word با pandoc و تنظیمات کامل
pandoc $InputFile `
    --from=markdown `
    --to=docx `
    --output=$OutputFile `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --highlight-style=pygments `
    --metadata title="بازتاب و متاکلاس‌ها در ++C23" `
    --metadata subtitle="طراحی و پیاده‌سازی" `
    --metadata author="نویسندگان مقاله" `
    --metadata lang="fa-IR" `
    --metadata dir="rtl"

if (Test-Path $OutputFile) {
    Write-Host "فایل Word اولیه ایجاد شد. اعمال تنظیمات فونت..." -ForegroundColor Yellow
    
    # باز کردن Word برای تنظیم فونت‌ها
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    
    try {
        $doc = $word.Documents.Open((Resolve-Path $OutputFile).Path)
        
        Write-Host "تنظیم فونت‌های فارسی..." -ForegroundColor Yellow
        
        # تنظیم فونت کل سند
        $range = $doc.Range()
        $range.Font.Name = "B Nazanin"
        $range.Font.Size = 11
        $range.ParagraphFormat.ReadingOrder = 2  # RTL
        
        # تنظیم عناوین
        $styles = $doc.Styles
        
        # Heading 1
        $h1 = $styles["Heading 1"]
        $h1.Font.Name = "B Titr"
        $h1.Font.Size = 18
        $h1.Font.Bold = $true
        $h1.Font.Color = 128  # آبی
        $h1.ParagraphFormat.Alignment = 2  # Center
        
        # Heading 2  
        $h2 = $styles["Heading 2"]
        $h2.Font.Name = "B Titr"
        $h2.Font.Size = 16
        $h2.Font.Bold = $true
        $h2.Font.Color = 128
        
        # Heading 3
        $h3 = $styles["Heading 3"]
        $h3.Font.Name = "B Titr"
        $h3.Font.Size = 14
        $h3.Font.Bold = $true
        $h3.Font.Color = 3355443
        
        Write-Host "تنظیم استایل کدها..." -ForegroundColor Yellow
        
        # جستجو و تنظیم بلوک‌های کد
        $findRange = $doc.Range()
        $findRange.Find.ClearFormatting()
        $findRange.Find.Style = "Source Code"
        
        while ($findRange.Find.Execute()) {
            $findRange.Font.Name = "Consolas"
            $findRange.Font.Size = 9
            $findRange.Shading.BackgroundPatternColor = 15790320  # خاکستری روشن
            $findRange.Collapse(0)  # End
        }
        
        # تنظیم کدهای درون خطی
        $findRange = $doc.Range()
        $findRange.Find.ClearFormatting()
        $findRange.Find.Font.Name = "Courier New"
        
        while ($findRange.Find.Execute()) {
            $findRange.Font.Name = "Consolas"
            $findRange.Font.Size = 10
            $findRange.Collapse(0)
        }
        
        Write-Host "تنظیم حاشیه‌ها و فرمت کلی..." -ForegroundColor Yellow
        
        # تنظیم حاشیه‌ها (2.5 سانتی‌متر)
        $doc.Range().PageSetup.LeftMargin = 90
        $doc.Range().PageSetup.RightMargin = 90 
        $doc.Range().PageSetup.TopMargin = 90
        $doc.Range().PageSetup.BottomMargin = 90
        
        # تنظیم فاصله خطوط
        $doc.Range().ParagraphFormat.LineSpacing = 18  # 1.5 خط
        
        # ذخیره تغییرات
        $doc.Save()
        $doc.Close()
        
        $fileInfo = Get-Item $OutputFile
        Write-Host "فایل Word نهایی آماده شد!" -ForegroundColor Green
        Write-Host "نام فایل: $($fileInfo.Name)" -ForegroundColor Cyan
        Write-Host "حجم: $([math]::Round($fileInfo.Length / 1KB, 2)) KB" -ForegroundColor Cyan
        Write-Host "مسیر: $($fileInfo.FullName)" -ForegroundColor Cyan
        
    } catch {
        Write-Error "خطا در تنظیم فونت‌ها: $($_.Exception.Message)"
    } finally {
        $word.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    }
    
} else {
    Write-Host "خطا در ایجاد فایل Word!" -ForegroundColor Red
}

Write-Host "`nمقاله شما آماده است!" -ForegroundColor Green
Write-Host "فایل Word شامل:" -ForegroundColor White
Write-Host "✓ فونت B Titr برای عناوین" -ForegroundColor Green
Write-Host "✓ فونت B Nazanin برای متن فارسی" -ForegroundColor Green  
Write-Host "✓ فونت Consolas برای کدها" -ForegroundColor Green
Write-Host "✓ فرمت ژورنالی حرفه‌ای" -ForegroundColor Green
Write-Host "✓ فهرست مطالب خودکار" -ForegroundColor Green
Write-Host "✓ شماره‌گذاری بخش‌ها" -ForegroundColor Green
