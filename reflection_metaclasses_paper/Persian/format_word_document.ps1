# اسکریپت تنظیم فونت‌ها در فایل Word
param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    
    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

# ایجاد آبجکت Word
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    # باز کردن فایل
    $doc = $word.Documents.Open($InputFile)
    
    Write-Host "تنظیم فونت‌ها در حال انجام..."
    
    # انتخاب تمام متن
    $range = $doc.Range()
    
    # تنظیم فونت پیش‌فرض: B Nazanin
    $range.Font.Name = "B Nazanin"
    $range.Font.Size = 11
    
    # تنظیم فونت برای عناوین (Heading styles)
    for ($i = 1; $i -le 9; $i++) {
        $headingStyle = $doc.Styles["Heading $i"]
        $headingStyle.Font.Name = "B Titr"
        $headingStyle.Font.Bold = $true
        
        switch ($i) {
            1 { $headingStyle.Font.Size = 16 }
            2 { $headingStyle.Font.Size = 14 }
            3 { $headingStyle.Font.Size = 13 }
            default { $headingStyle.Font.Size = 12 }
        }
    }
    
    # تنظیم فونت برای کدها
    $codeStyle = $doc.Styles["Code"]
    if ($codeStyle) {
        $codeStyle.Font.Name = "Consolas"
        $codeStyle.Font.Size = 10
    }
    
    # جستجو و تنظیم متن‌های انگلیسی
    $englishPattern = "[A-Za-z0-9\s\.\,\;\:\!\?\(\)\[\]\{\}\-\_\+\=\@\#\$\%\^\&\*\\\/\<\>\`\~\|]+"
    
    $findRange = $doc.Range()
    $findRange.Find.ClearFormatting()
    $findRange.Find.Text = $englishPattern
    $findRange.Find.MatchWildcards = $true
    
    while ($findRange.Find.Execute()) {
        # بررسی اینکه آیا این متن کد است یا نه
        if ($findRange.Style.NameLocal -match "Code|Pre|Verbatim") {
            $findRange.Font.Name = "Consolas"
            $findRange.Font.Size = 10
        } else {
            $findRange.Font.Name = "Times New Roman"
            $findRange.Font.Size = 11
        }
        
        # ادامه جستجو
        $findRange.Collapse(0)  # End
    }
    
    # تنظیم جهت متن (راست به چپ)
    $doc.Range().ParagraphFormat.ReadingOrder = 2  # Right to Left
    
    # تنظیم حاشیه‌ها
    $doc.Range().PageSetup.LeftMargin = 72    # 1 inch
    $doc.Range().PageSetup.RightMargin = 72   # 1 inch
    $doc.Range().PageSetup.TopMargin = 72     # 1 inch
    $doc.Range().PageSetup.BottomMargin = 72  # 1 inch
    
    Write-Host "ذخیره فایل..."
    
    # ذخیره فایل جدید
    $doc.SaveAs([ref]$OutputFile)
    $doc.Close()
    
    Write-Host "فایل با موفقیت ایجاد شد: $OutputFile"
    
} catch {
    Write-Error "خطا در پردازش فایل: $($_.Exception.Message)"
} finally {
    # بستن Word
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
