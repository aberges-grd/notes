import argparse
from pathlib import Path


def crawl_directory(directory, level=None, alias=None):
    def _crawl_directory(dir_path, curr_level):
        if level is not None and curr_level > level:
            return

        nested_dict = {}
        for item in dir_path.iterdir():
            if item.is_file():
                nested_dict[item.name] = None
            elif item.is_dir():
                nested_dict[item.name] = _crawl_directory(item, curr_level + 1)

        return nested_dict

    if alias is None:
        alias = directory.name

    return {alias: _crawl_directory(directory, 1)}


def to_dirtree_format(nested_dict):
    def _to_dirtree_format(nested_dict, depth=1):
        dirtree_str = ""

        for key, value in nested_dict.items():
            dirtree_str += f".{depth} {key}.\n"
            if value is None:  # It's a file
                pass
            else:  # It's a directory
                dirtree_str += _to_dirtree_format(value, depth + 1)

        return dirtree_str

    dirtree_str = _to_dirtree_format(nested_dict).replace("_", r"\_")
    return "\\dirtree{%\n" + dirtree_str + "}"


def main():
    parser = argparse.ArgumentParser(
        description="Recursively crawl a directory and create a nested dictionary representing the file and folder structure"
    )
    parser.add_argument("directory", type=Path, help="The directory to crawl")
    parser.add_argument(
        "--level", "-L", type=int, default=None, help="The maximum depth of recursion"
    )
    parser.add_argument(
        "--alias", "-a", type=str, default=None, help="An alias for the input directory"
    )
    parser.add_argument(
        "--to-dirtree",
        "-D",
        action="store_true",
        default=False,
        help="formats the output to LaTeX dirtree instead of JSON.",
    )

    args = parser.parse_args()

    result = crawl_directory(args.directory, args.level, args.alias)
    result = result if not args.to_dirtree else to_dirtree_format(result)
    print(result)


if __name__ == "__main__":
    main()
