
import argparse
import re
import sys
from pathlib import Path


CONDITIONS = ["击杀语音", "交流信号", "局内触发", "任务相关", "地图触发"]
DEFAULT_VOICE_ROOT = Path(r"G:\守望语音")
DEFAULT_FILEFOLDER = "ow-dmon-ver"
DEFAULT_HERO = "D.Mon"


def parse_args():
    parser = argparse.ArgumentParser(
        description="根据 5 个条件模板，从英雄全条件文本中自动填充并导出 txt。"
    )
    parser.add_argument("-H", "--hero", default=DEFAULT_HERO, help=f"英雄英文目录名，默认：{DEFAULT_HERO}")
    parser.add_argument("-f", "--folder", default=DEFAULT_FILEFOLDER, help=f"语音工程文件夹名，默认：{DEFAULT_FILEFOLDER}")
    parser.add_argument("--voice-root", type=Path, default=DEFAULT_VOICE_ROOT, help=f"语音根目录，默认：{DEFAULT_VOICE_ROOT}")
    parser.add_argument("-s", "--source", type=Path, help="全条件文本路径；不填则自动查找最新的 英雄-日期-所有音频.txt")
    parser.add_argument("-o", "--output-dir", type=Path, help="输出目录；不填则输出到全条件文本所在目录")
    parser.add_argument(
        "-c",
        "--conditions",
        nargs="+",
        default=CONDITIONS,
        help="要导出的条件名，可指定一个或多个；默认导出全部 5 个条件",
    )
    parser.add_argument("--template-dir", type=Path, default=Path(__file__).resolve().parent, help="模板所在目录")
    parser.add_argument("--prefix-hero", action="store_true", help="输出文件名前加英雄名，避免多个英雄结果混在一起")
    return parser.parse_args()


def find_latest_source(hero, search_dir):
    patterns = [f"{hero}-*-所有音频.txt", f"{hero}-*.txt"]
    matches = []
    for pattern in patterns:
        matches.extend(search_dir.glob(pattern))

    matches = [path for path in matches if path.is_file()]
    if not matches:
        raise FileNotFoundError(f"没有找到全条件文本：{search_dir}\\{hero}-*-所有音频.txt")

    return max(matches, key=lambda path: path.stat().st_mtime)


def load_sections(source_text, hero):
    section_pattern = re.compile(r"^==(.+?)==\s*$", re.MULTILINE)
    matches = list(section_pattern.finditer(source_text))
    sections = {}

    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        content = source_text[start:end].strip("\n")

        if title.startswith(f"{hero}\\"):
            code = title[len(hero) + 1 :]
            sections[code] = content
        sections.setdefault(title, content)

    return sections


def extract_template_codes(template_text):
    codes = []
    for line in template_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            codes.append(stripped[1:].strip())
    return codes


def fill_template(template_text, sections):
    output_lines = []
    missing_codes = []

    for line in template_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            code = stripped[1:].strip()
            content = sections.get(code)
            if content:
                output_lines.extend(content.splitlines())
            else:
                output_lines.append(line)
                missing_codes.append(code)
        else:
            output_lines.append(line)

    return "\n".join(output_lines).rstrip() + "\n", missing_codes


def build_output_name(condition, hero, prefix_hero):
    if prefix_hero:
        return f"{hero}-{condition}output.txt"
    return f"{condition}output.txt"


def export_condition(condition, template_dir, output_dir, hero, sections, prefix_hero):
    template_path = template_dir / f"{condition}模板.txt"
    if not template_path.exists():
        raise FileNotFoundError(f"模板不存在：{template_path}")

    template_text = template_path.read_text(encoding="utf-8")
    final_text, missing_codes = fill_template(template_text, sections)

    output_path = output_dir / build_output_name(condition, hero, prefix_hero)
    output_path.write_text(final_text, encoding="utf-8")

    return output_path, len(extract_template_codes(template_text)) - len(missing_codes), missing_codes


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    search_dir = args.voice_root / args.folder
    source_path = args.source or find_latest_source(args.hero, search_dir)
    output_dir = args.output_dir or source_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    source_text = source_path.read_text(encoding="utf-8")
    sections = load_sections(source_text, args.hero)

    print(f"英雄：{args.hero}")
    print(f"全条件文本：{source_path}")
    print(f"输出目录：{output_dir}")

    for condition in args.conditions:
        output_path, filled_count, missing_codes = export_condition(
            condition=condition,
            template_dir=args.template_dir,
            output_dir=output_dir,
            hero=args.hero,
            sections=sections,
            prefix_hero=args.prefix_hero,
        )
        print(f"[完成] {condition}: {output_path}，填充 {filled_count} 项，未匹配 {len(missing_codes)} 项")
        if missing_codes:
            print("       未匹配：" + "、".join(missing_codes))


if __name__ == "__main__":
    main()
