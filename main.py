from __future__ import annotations

import argparse
from pathlib import Path

import pyreadstat


PROJECT_DIR = Path(__file__).resolve().parent
XPT_DIR = PROJECT_DIR / "XPT_files"
TXT_DIR = PROJECT_DIR / "TXT_files"


def ensure_folders() -> None:
    XPT_DIR.mkdir(exist_ok=True)
    TXT_DIR.mkdir(exist_ok=True)


def find_xpt_files() -> list[Path]:
    xpt_files = sorted(XPT_DIR.glob("*.xpt"))
    if not xpt_files:
        raise FileNotFoundError(f"No .xpt files found in {XPT_DIR}.")

    return xpt_files


def resolve_input_path(input_arg: Path) -> Path:
    if input_arg.is_absolute() or input_arg.parent != Path("."):
        return input_arg

    return XPT_DIR / input_arg


def write_xpt_to_txt(input_path: Path, output_path: Path) -> None:
    data_frame, metadata = pyreadstat.read_xport(input_path)

    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(f"Source file: {input_path}\n")
        output_file.write(f"Rows: {len(data_frame)}\n")
        output_file.write(f"Columns: {len(data_frame.columns)}\n\n")

        if metadata.column_labels:
            output_file.write("Column labels:\n")
            for column_name, label in zip(metadata.column_names, metadata.column_labels):
                if label:
                    output_file.write(f"- {column_name}: {label}\n")
            output_file.write("\n")

        output_file.write("Data:\n")
        output_file.write(data_frame.to_string(index=False))
        output_file.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read SAS XPORT .xpt files from XPT_files and print their contents "
            "to .txt files in TXT_files."
        )
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help=(
            "Optional .xpt filename or path. Defaults to converting every .xpt "
            "file in XPT_files."
        ),
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help=(
            "Optional output .txt path for a single input. Defaults to "
            "TXT_files/INPUT_NAME.txt."
        ),
    )
    return parser.parse_args()


def main() -> None:
    ensure_folders()
    args = parse_args()

    if args.input:
        input_paths = [resolve_input_path(args.input)]
    else:
        input_paths = find_xpt_files()

    if args.output and len(input_paths) > 1:
        raise ValueError("Output path can only be used when converting one input file.")

    for input_path in input_paths:
        if input_path.suffix.lower() != ".xpt":
            raise ValueError(f"Expected a .xpt input file, got: {input_path}")

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        output_path = args.output or (TXT_DIR / input_path.with_suffix(".txt").name)
        write_xpt_to_txt(input_path, output_path)
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
