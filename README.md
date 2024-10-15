## Overview and features

GUI accepting a newline delimited list (e.g. from a copied Excel/Google Sheets spreadsheet) and returning a list wrapped in double quotes with separating commas. Output text can be copied to clipboard.

I suggest compiling using e.g. `pyinstaller`.

- Allows swapping between double (default) and single quotes
- Blank list items will be ignored

## Shortcuts

**Input window**: `CMD` + `Enter` (or `CTRL` + `Enter` on PC/Linux) will submit & process the input text

**Output window**: `Enter` will copy the output text to your clipboard and close the output window

## Example Input & Output

Sample input:
```
Item 1
Item 2
Item 3

Item 4
```

Sample output (double quote mode):
```
"Item 1",
"Item 2",
"Item 3",
"Item 4"
```
