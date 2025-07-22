import re
from pathlib import Path, UnsupportedOperation
from collections import defaultdict
from typing import Generator, Sequence


def rename_files(path: str | Path, replacement: str, pattern: str, escaped=True):
    posix_path = Path(path)

    if not posix_path.exists():
        raise FileNotFoundError(f"{posix_path} not found")

    if posix_path.is_dir():
        files = list(posix_path.iterdir())
        prefix = get_common_prefix([f.name for f in files])

        for i, file in enumerate(files):
            if not file.is_file():
                continue

            ext = file.suffix
            new_name = f"{prefix}{i}{ext}"
            dest = file.parent / new_name
            file.rename(dest)
    else:
        fname = match_and_replace(posix_path.stem, pattern, replacement, escaped)
        new_name = f"{fname}{posix_path.suffix}"
        dest = posix_path.with_name(new_name)
        posix_path.rename(dest)


def organize_file_by_prefix(dir_path: str | Path):
    posix_path = Path(dir_path)
    if posix_path.is_file():
        raise UnsupportedOperation("cannot classify single file")
    if not posix_path.exists():
        raise FileNotFoundError(f"{posix_path} not found")

    groups = classify_group_and_file([f for f in posix_path.iterdir()])
    for folder in groups.keys():
        Path(folder).mkdir(exist_ok=True)
        for file in groups[folder]:
            file.rename(
                folder / match_and_replace(file.name, "[^0-9A-Za-z._-]+", "", False)
            )


def match_and_replace(string: str, pattern: str, replacement: str, to_escape):
    if len(pattern) == 0:
        return string
    if to_escape:
        pattern = re.escape(pattern)
    str_match = re.sub(pattern, replacement, string, count=0)
    return str_match


def get_common_prefix(filenames: Sequence[str], attempt_better: bool = False) -> str:
    if not filenames:
        raise ValueError("Empty sequence isn't allowed")
    if len(filenames) == 1:
        return ""

    filenames = sorted(filenames, key=len)
    prefix = filenames[0]

    if not attempt_better:
        second = filenames[1]
        match_length = 0
        for i in range(len(prefix)):
            ch1 = prefix[i]
            ch2 = second[i]
            if ch1 != ch2 or not ch1.isalnum():
                break
            match_length += 1

        if match_length == 0:
            return ""

        prefix = prefix[:match_length]
        for f in filenames[2:]:
            if not f.startswith(prefix):
                return ""
        return prefix
    else:
        while prefix:
            if all(f.startswith(prefix) for f in filenames):
                return prefix
            prefix = prefix[:-1]
        return ""


def classify_group_and_file(paths: Sequence[Path] | Generator[Path]):
    groups = defaultdict(list)  # type: defaultdict[Path, list[Path]]
    for path in paths:
        if path.is_dir():
            continue
        name = path.stem
        parent = path.parent
        matched_str = re.match(r"\d*[0-9a-zA-Z]+\d*", name)
        if matched_str:
            group = matched_str.group()
            groups[parent / group].append(path)
    return groups


if __name__ == "__main__":
    import os

    x = "/home/rudy/Downloads/firefox/FreeDinoSprite/png"
    y = organize_file_by_prefix(x)
    print(y)
