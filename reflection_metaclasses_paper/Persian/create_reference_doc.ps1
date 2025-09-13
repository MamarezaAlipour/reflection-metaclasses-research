# ایجاد فایل مرجع Word برای تنظیم فونت‌ها
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    $doc = $word.Documents.Add()
    
    # تنظیم فونت پیش‌فرض
    $doc.Range().Font.Name = "B Nazanin"
    $doc.Range().Font.Size = 11
    
    # تنظیم استایل‌های عناوین
    $heading1 = $doc.Styles["Heading 1"]
    $heading1.Font.Name = "B Titr"
    $heading1.Font.Size = 18
    $heading1.Font.Bold = $true
    $heading1.Font.Color = 128  # آبی تیره
    
    $heading2 = $doc.Styles["Heading 2"]
    $heading2.Font.Name = "B Titr"
    $heading2.Font.Size = 16
    $heading2.Font.Bold = $true
    $heading2.Font.Color = 128
    
    $heading3 = $doc.Styles["Heading 3"]
    $heading3.Font.Name = "B Titr"
    $heading3.Font.Size = 14
    $heading3.Font.Bold = $true
    $heading3.Font.Color = 3355443  # آبی کمرنگ
    
    # ایجاد استایل کد
    $codeStyle = $doc.Styles.Add("Code Block", 1)  # Character style
    $codeStyle.Font.Name = "Consolas"
    $codeStyle.Font.Size = 9
    $codeStyle.Font.Color = 0  # مشکی
    $codeStyle.Shading.BackgroundPatternColor = 15790320  # خاکستری روشن
    
    # تنظیم حاشیه‌ها
    $doc.Range().PageSetup.LeftMargin = 90   # 2.5 cm
    $doc.Range().PageSetup.RightMargin = 90
    $doc.Range().PageSetup.TopMargin = 90
    $doc.Range().PageSetup.BottomMargin = 90
    
    # تنظیم جهت متن
    $doc.Range().ParagraphFormat.ReadingOrder = 2  # RTL
    
    # ذخیره به عنوان template
    $doc.SaveAs([ref]"C:\Users\P - K\Downloads\cpp prop\reflection_metaclasses_paper\Persian\reference.docx")
    $doc.Close()
    
    Write-Host "فایل مرجع Word ایجاد شد: reference.docx" -ForegroundColor Green
    
} catch {
    Write-Error "خطا در ایجاد فایل مرجع: $($_.Exception.Message)"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
