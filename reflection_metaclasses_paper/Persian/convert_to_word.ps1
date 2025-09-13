# اسکریپت تبدیل مقاله به فرمت Word

# نصب Pandoc (در صورت عدم وجود)
# Invoke-WebRequest https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-windows-x86_64.msi -OutFile pandoc.msi
# Start-Process pandoc.msi /wait

# تبدیل فایل markdown به Word با فرمت حرفه‌ای
$inputFile = "مقاله_کامل_بازتاب_متاکلاس_C++23.md"
$outputFile = "مقاله_کامل_بازتاب_متاکلاس_C++23.docx"

# دستور pandoc برای تبدیل
pandoc $inputFile -o $outputFile `
    --from=markdown `
    --to=docx `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --highlight-style=tango `
    --reference-doc=template.docx `
    --metadata title="بازتاب و متاکلاس‌ها در C++23" `
    --metadata author="محمدرضا علی‌پور" `
    --metadata date="آگوست 2025"

Write-Host "فایل Word با موفقیت ایجاد شد: $outputFile" -ForegroundColor Green

# تبدیل به PDF نیز
$pdfFile = "مقاله_کامل_بازتاب_متاکلاس_C++23.pdf"
pandoc $inputFile -o $pdfFile `
    --from=markdown `
    --to=pdf `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --highlight-style=tango `
    --pdf-engine=xelatex `
    --variable mainfont="Times New Roman" `
    --variable fontsize=12pt `
    --variable geometry="margin=2.5cm" `
    --metadata title="بازتاب و متاکلاس‌ها در C++23" `
    --metadata author="محمدرضا علی‌پور"

Write-Host "فایل PDF با موفقیت ایجاد شد: $pdfFile" -ForegroundColor Green
