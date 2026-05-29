# readXPT

`readXPT` is a quick way to look inside the contents of SAS XPORT `.xpt` files.

The script reads `.xpt` files and writes easy-to-open `.txt` files that include:

- the source file name
- row and column counts
- column labels, when available
- the file data

## Setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Put your `.xpt` files in the `XPT_files` folder.

To convert every `.xpt` file in `XPT_files`:

```bash
python main.py
```

The output `.txt` files will be written to `TXT_files`.

## Example

To inspect one file:

```bash
python main.py DEMO_J.xpt
```

This reads:

```text
XPT_files/DEMO_J.xpt
```

and writes:

```text
TXT_files/DEMO_J.txt
```

You can also choose a custom output path:

```bash
python main.py DEMO_J.xpt TXT_files/demo_output.txt
```
