import argparse
import re
import shutil
import sys
from pathlib import Path


DEFAULT_BASE_DIR = Path(r"G:\守望语音\ow-dmon-ver")
DEFAULT_ZH_DIR = DEFAULT_BASE_DIR / "对话(zh)"
DEFAULT_EN_DIR = DEFAULT_BASE_DIR / "对话(en)"
DEFAULT_OUTPUT_DIR = DEFAULT_BASE_DIR / "对话upload"
DEFAULT_LOG = DEFAULT_BASE_DIR / "对话upload_log.txt"

VOICE_ID_RE = re.compile(r"^[^-]+-[^-]+-([0-9A-Fa-f]{12}\.[^-]+)(?:-|$)")


def parse_args():
    parser = argparse.ArgumentParser(description="把中英文对话音频按 FileId_lang.ogg 平铺复制到一个文件夹。")
    parser.add_argument("--zh-dir", type=Path, default=DEFAULT_ZH_DIR, help=f"中文对话目录，默认：{DEFAULT_ZH_DIR}")
    parser.add_argument("--en-dir", type=Path, default=DEFAULT_EN_DIR, help=f"英文对话目录，默认：{DEFAULT_EN_DIR}")
    parser.add_argument("-o", "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help=f"输出目录，默认：{DEFAULT_OUTPUT_DIR}")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help=f"日志文件，默认：{DEFAULT_LOG}")
    return parser.parse_args()


def extract_file_id(filename):
    match = VOICE_ID_RE.match(Path(filename).stem)
    return match.group(1) if match else ""


def flat_audio_name(filename, lang):
    file_id = extract_file_id(filename)
    if not file_id:
        return ""
    return f"{file_id}_{lang}.ogg"


def copy_flat_audio(src_root, output_dir, lang, logs):
    copied = 0
    skipped = 0
    overwritten = 0

    for src_path in sorted(src_root.rglob("*.ogg")):
        new_name = flat_audio_name(src_path.name, lang)
        if not new_name:
            logs.append(f"[无法解析文件名] {src_path}")
            skipped += 1
            continue

        dst_path = output_dir / new_name
        if dst_path.exists():
            overwritten += 1
            logs.append(f"[覆盖] {dst_path.name} <- {src_path}")

        shutil.copy2(src_path, dst_path)
        copied += 1

    return copied, skipped, overwritten


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    logs = []
    args.output_dir.mkdir(parents=True, exist_ok=True)

    zh_result = copy_flat_audio(args.zh_dir, args.output_dir, "zh", logs)
    en_result = copy_flat_audio(args.en_dir, args.output_dir, "en", logs)

    args.log.write_text("\n".join(logs) + ("\n" if logs else ""), encoding="utf-8")

    print(f"输出目录：{args.output_dir}")
    print(f"中文：复制 {zh_result[0]}，跳过 {zh_result[1]}，覆盖 {zh_result[2]}")
    print(f"英文：复制 {en_result[0]}，跳过 {en_result[1]}，覆盖 {en_result[2]}")
    print(f"日志：{args.log}（{len(logs)} 条）")


if __name__ == "__main__":
    main()
