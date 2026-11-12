---
title: Сводная таблица по продажам
description: Строит сводную по регионам и месяцам из листа "Данные"
warnings:
  - Требует, чтобы данные были в формате "дата | регион | сумма"
---

## Задача

Строит сводную таблицу: строки — регионы, столбцы — месяцы, значения — сумма продаж.

## VBA

```vba
Sub BuildPivot()
    Dim pc As PivotCache
    Dim pt As PivotTable
    Set pc = ActiveWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=Sheets("Данные").Range("A1").CurrentRegion)
    Set pt = pc.CreatePivotTable( _
        TableDestination:=Sheets("Свод").Range("A3"))
    pt.PivotFields("Регион").Orientation = xlRowField
    pt.PivotFields("Месяц").Orientation = xlColumnField
    pt.AddDataField pt.PivotFields("Сумма"), "Итого", xlSum
End Sub
```

## Apps Script

```javascript
function buildPivot() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const source = ss.getSheetByName('Данные');
  const target = ss.getSheetByName('Свод');
  const range = source.getRange('A1:C' + source.getLastRow());
  const pivot = target.getRange('A3').createPivotTable(range);
  pivot.addRowGroup(source.getRange('A2'));
  pivot.addColumnGroup(source.getRange('B2'));
  pivot.addPivotValue(source.getRange('C2'), SpreadsheetApp.PivotTableSummarizeFunction.SUM);
}
```
