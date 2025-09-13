# اسکریپت تولید فایل Word با فونت‌های مخصوص

# ایجاد فایل Word موقت با فونت‌های مطلوب
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false

# ایجاد سند جدید
$doc = $wordApp.Documents.Add()

# تنظیم فونت‌های مختلف
$styles = $doc.Styles

# تنظیم فونت برای تیترها (B Titr)
$titleStyle = $styles.Item("Heading 1")
$titleStyle.Font.Name = "B Titr"
$titleStyle.Font.Size = 18
$titleStyle.Font.Bold = $true

$heading2Style = $styles.Item("Heading 2")
$heading2Style.Font.Name = "B Titr"
$heading2Style.Font.Size = 16
$heading2Style.Font.Bold = $true

$heading3Style = $styles.Item("Heading 3")
$heading3Style.Font.Name = "B Titr"
$heading3Style.Font.Size = 14
$heading3Style.Font.Bold = $true

# تنظیم فونت برای متن معمولی (B Nazanin)
$normalStyle = $styles.Item("Normal")
$normalStyle.Font.Name = "B Nazanin"
$normalStyle.Font.Size = 12

# ذخیره template
$templatePath = "$(Get-Location)\custom_template.dotx"
$doc.SaveAs2($templatePath, 16) # 16 = Word template format

# بستن Word
$doc.Close()
$wordApp.Quit()

Write-Host "Template Word ایجاد شد: $templatePath" -ForegroundColor Green

# حالا pandoc را با template سفارشی اجرا می‌کنیم
pandoc "مقاله_کامل_بازتاب_متاکلاس_C++23.md" -o "مقاله_نهایی_با_فونت_مخصوص.docx" `
    --from=markdown `
    --to=docx `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --highlight-style=tango `
    --reference-doc="custom_template.dotx" `
    --metadata title="بازتاب و متاکلاس‌های C++23: آینده برنامه‌نویسی عمومی" `
    --metadata author="محمدرضا علی‌پور" `
    --metadata date="آگوست 2025"

Write-Host "فایل Word نهایی با فونت‌های مخصوص ایجاد شد!" -ForegroundColor Green
