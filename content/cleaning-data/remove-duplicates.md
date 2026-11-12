---
title: Удалить дубликаты в колонке
description: Убирает повторяющиеся значения в указанном столбце
warnings:
  - Удаляет данные без возможности отмены — сделайте копию листа
---

## Задача

Удаляет повторяющиеся значения в столбце A на листе "Sheet1".

## VBA

```vba
Sub RemoveDuplicates()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Sheet1")
    ws.Range("A:A").RemoveDuplicates Columns:=1, Header:=xlYes
End Sub
```

## Apps Script

```javascript
function removeDuplicates() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  sheet.getRange('A:A').removeDuplicates();
}
```
