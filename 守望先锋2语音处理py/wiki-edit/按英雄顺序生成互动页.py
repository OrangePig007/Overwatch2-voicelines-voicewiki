import argparse
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_DIALOGUE_FILES = [
    Path(r"G:\守望语音\ow-dmon-ver\对话output_两人及以下.txt"),
]
DEFAULT_OUTPUT = Path(r"G:\GithubFile\Overwatch2-voicelines-voicewiki\守望先锋2语音处理py\wiki-edit\wiki-dia-new.txt")
DEFAULT_DETECT_SOURCE = Path(r"G:\GithubFile\Overwatch2-voicelines-voicewiki\守望先锋2语音处理py\wiki-edit\wiki-dia.txt")

HERO_ORDER = [
    ("D.Va", "D.Va"),
    ("Orisa", "奥丽莎"),
    ("Zarya", "查莉娅"),
    ("Winston", "温斯顿"),
    ("Wrecking Ball", "破坏球"),
    ("Reinhardt", "莱因哈特"),
    ("Sigma", "西格玛"),
    ("Roadhog", "路霸"),
    ("Doomfist", "末日铁拳"),
    ("Junker Queen", "渣客女王"),
    ("Ramattra", "拉玛刹"),
    ("Mauga", "毛加"),
    ("Hazard", "骇灾"),
    ("Domina", "金驭"),
    ("D.Mon", "D.Mon"),
    ("Hanzo", "半藏"),
    ("Echo", "回声"),
    ("Bastion", "堡垒"),
    ("Soldier76", "士兵：76"),
    ("Torbjorn", "托比昂"),
    ("Reaper", "死神"),
    ("Pharah", "法老之鹰"),
    ("Genji", "源氏"),
    ("Junkrat", "狂鼠"),
    ("Tracer", "猎空"),
    ("Symmetra", "秩序之光"),
    ("Mei", "美"),
    ("Ashe", "艾什"),
    ("Cassidy", "卡西迪"),
    ("Sombra", "黑影"),
    ("Widowmaker", "黑百合"),
    ("Sojourn", "索杰恩"),
    ("Venture", "探奇"),
    ("Freja", "弗蕾娅"),
    ("Vendetta", "斩仇"),
    ("Anran", "安燃"),
    ("Emre", "埃姆雷"),
    ("Sierra", "西拉"),
    ("Shion", "死怨"),
    ("Lucio", "卢西奥"),
    ("Mercy", "天使"),
    ("Ana", "安娜"),
    ("Baptiste", "巴蒂斯特"),
    ("Brigitte", "布丽吉塔"),
    ("Zenyatta", "禅雅塔"),
    ("Moira", "莫伊拉"),
    ("Kiriko", "雾子"),
    ("Lifeweaver", "生命之梭"),
    ("Illari", "伊拉锐"),
    ("Juno", "朱诺"),
    ("Wuyang", "无漾"),
    ("Mizuki", "瑞稀"),
    ("Jetpack Cat", "飞天猫"),
]

EN_ALIASES = {
    "Soldier_ 76": "Soldier76",
    "Soldier: 76": "Soldier76",
    "Torbjörn": "Torbjorn",
    "Lúcio": "Lucio",
    "JetpackCat": "Jetpack Cat",
}

EN_TO_ZH = {en: zh for en, zh in HERO_ORDER}
ZH_TO_EN = {zh: en for en, zh in HERO_ORDER}
ZH_ORDER = [zh for _, zh in HERO_ORDER]
RANK = {zh: index for index, zh in enumerate(ZH_ORDER)}
TANK_END_ZH = "D.Mon"
DAMAGE_START_ZH = "半藏"
DAMAGE_END_ZH = "死怨"
SUPPORT_START_ZH = "卢西奥"


def parse_args():
    parser = argparse.ArgumentParser(description="按英雄顺序生成英雄互动页，靠前英雄已收录的对话用 section-h 引用。")
    parser.add_argument("hero", nargs="?", help="目标英雄中文名或英文名；不填则从输出文件第一行 Back 模板识别")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        nargs="+",
        default=DEFAULT_DIALOGUE_FILES,
        help="新增对话表输入，可传多个文件；默认只读取新对话",
    )
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT, help=f"输出文件，默认：{DEFAULT_OUTPUT}")
    parser.add_argument(
        "--detect-source",
        type=Path,
        default=DEFAULT_DETECT_SOURCE,
        help=f"未指定英雄且输出文件为空时，用来识别目标英雄的文件，默认：{DEFAULT_DETECT_SOURCE}",
    )
    return parser.parse_args()


def normalize_en(hero):
    return EN_ALIASES.get(hero, hero)


def hero_to_zh(hero):
    if hero in ZH_TO_EN:
        return hero
    return EN_TO_ZH.get(normalize_en(hero), hero)


def page_title(hero_zh):
    if hero_zh == "D.Va":
        return "D.Va(守望先锋2)/英雄互动"
    return f"{hero_zh}(守望先锋2)/英雄互动"


def section_ref(source_hero_zh, target_hero_zh):
    return f"{{{{#section-h:{page_title(source_hero_zh)}|{target_hero_zh}}}}}"


def tank_module(target_hero_zh):
    return f"{{{{ow-dialog-module-tank|{target_hero_zh}}}}}"


def damage_module(target_hero_zh):
    return f"{{{{ow-dialog-module-damage|{target_hero_zh}}}}}"


def clean_en_text(text, zh_hint=""):
    def replace_pseudo_quote(match):
        prefix = match.group(1)
        inner = match.group(2)
        suffix = "?" if not inner.endswith((".", "!", "…")) and ("”？" in zh_hint or '"?' in zh_hint) else ""
        return f'{prefix}"{inner}"{suffix}'

    text = re.sub(r'(^|[\s(])\?([^\s?\n|][^?\n|]*?)\?', replace_pseudo_quote, text)
    text = re.sub(r'(?<=[A-Za-z0-9])\?(?=[A-Za-z0-9])', '/', text)
    return text


def clean_voice_block(block):
    def replace_en(match):
        return match.group(1) + clean_en_text(match.group(2), match.group(3))

    return re.sub(r'(\|en\d+=)([^|\n]*)(?=\|zh\d+=([^|\n]*))', replace_en, block)


def table_key(block):
    return tuple(re.findall(r"\|file\d+=([^|\n]+)", block))


def clean_section_body(body):
    return re.sub(
        r"\{\{OWVoiceTable\n.*?\n\}\}",
        lambda match: clean_voice_block(match.group(0).strip()),
        body,
        flags=re.S,
    ).strip()


def collect_existing_sections(output_path):
    if not output_path.exists():
        return {}

    text = output_path.read_text(encoding="utf-8")
    back_match = re.match(r'(?s)(\{\{Back\|.*?\}\}\s*)', text)
    rest = text[back_match.end():] if back_match else text
    heading_re = re.compile(r'^==\s*(.+?)\s*==\s*$', re.M)
    headings = list(heading_re.finditer(rest))
    notes = {}

    for index, match in enumerate(headings):
        title = match.group(1).strip()
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(rest)
        body = clean_section_body(rest[start:end])
        if body and body != "暂时没有对话……":
            notes[title] = body

    return notes


def collect_existing_sections_from(paths):
    merged = {}
    for path in paths:
        for title, body in collect_existing_sections(path).items():
            if title not in merged:
                merged[title] = body
    return merged


def collect_section_table_keys(body):
    return {
        table_key(block)
        for block in re.findall(r"\{\{OWVoiceTable\n.*?\n\}\}", body, re.S)
    }


def detect_file_hero(path):
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return ""

    first_line = path.read_text(encoding="utf-8").splitlines()[0].strip()
    match = re.match(r"\{\{Back\|.*?\|(.+?)\}\}", first_line)
    return match.group(1).strip() if match else ""


def existing_read_sources(output_path, fallback_path, target_zh):
    sources = []
    if fallback_path.exists() and fallback_path.read_text(encoding="utf-8").strip():
        sources.append(fallback_path)

    output_hero = hero_to_zh(detect_file_hero(output_path)) if output_path.exists() else ""
    if (
        output_path.exists()
        and output_path.read_text(encoding="utf-8").strip()
        and output_path != fallback_path
        and output_hero == target_zh
    ):
        sources.append(output_path)
    return sources


def collect_dialogues(paths):
    pair_to_blocks = defaultdict(list)
    seen = defaultdict(set)

    for path in paths:
        text = path.read_text(encoding="utf-8")
        blocks = [
            clean_voice_block(block.strip())
            for block in re.findall(r"\{\{OWVoiceTable\n.*?\n\}\}", text, re.S)
        ]

        for block in blocks:
            heroes = {hero_to_zh(match.group(1).strip()) for match in re.finditer(r"\|hero\d+=([^|\n]+)", block)}
            if len(heroes) != 2:
                continue
            pair = tuple(sorted(heroes, key=lambda name: RANK.get(name, 999)))
            key = table_key(block)
            if key not in seen[pair]:
                pair_to_blocks[pair].append(block)
                seen[pair].add(key)

    return pair_to_blocks


def merge_dialogues(old_sources, new_sources):
    pair_to_blocks = defaultdict(list)
    seen = defaultdict(set)

    for source_group in (old_sources, new_sources):
        source_dialogues = collect_dialogues(source_group)
        for pair, blocks in source_dialogues.items():
            for block in blocks:
                key = table_key(block)
                if key not in seen[pair]:
                    pair_to_blocks[pair].append(block)
                    seen[pair].add(key)

    return pair_to_blocks


def detect_target_hero(detect_path):
    if not detect_path.exists():
        raise FileNotFoundError(f"未指定目标英雄，且识别文件不存在：{detect_path}")

    target = detect_file_hero(detect_path)
    if not target:
        first_line = detect_path.read_text(encoding="utf-8").splitlines()[0].strip()
        raise ValueError(f"未指定目标英雄，且识别文件第一行不是可识别的 Back 模板：{first_line}")

    return target


def main():
    args = parse_args()
    target_zh = hero_to_zh(args.hero or detect_target_hero(args.detect_source))
    target_rank = RANK[target_zh]
    read_sources = existing_read_sources(args.output, args.detect_source, target_zh)
    new_pair_to_blocks = collect_dialogues(args.input)
    existing_sections = collect_existing_sections_from(read_sources)

    parts = [f"{{{{Back|{target_zh}(守望先锋2)|{target_zh}}}}}"]
    use_tank_module = target_rank >= RANK[DAMAGE_START_ZH]
    use_damage_module = target_rank >= RANK[SUPPORT_START_ZH]
    if use_tank_module:
        module_lines = [tank_module(target_zh)]
        if use_damage_module:
            module_lines.append(damage_module(target_zh))
        parts.append("\n".join(module_lines))

    full_count = 0
    ref_count = 0
    empty_count = 0
    module_count = int(use_tank_module) + int(use_damage_module)

    for other_zh in ZH_ORDER:
        if other_zh == target_zh:
            continue
        if use_tank_module and RANK[other_zh] <= RANK[TANK_END_ZH]:
            continue
        if use_damage_module and RANK[other_zh] <= RANK[DAMAGE_END_ZH]:
            continue
        pair = tuple(sorted((target_zh, other_zh), key=lambda name: RANK.get(name, 999)))
        existing_body = existing_sections.get(other_zh, "")
        existing_keys = collect_section_table_keys(existing_body)
        blocks = [
            block
            for block in new_pair_to_blocks.get(pair, [])
            if table_key(block) not in existing_keys
        ]

        if RANK[other_zh] < target_rank:
            body = section_ref(other_zh, target_zh)
            ref_count += 1
        elif blocks:
            body_parts = blocks[:]
            if existing_body:
                body_parts.append(existing_body)
            body = "\n\n".join(body_parts)
            full_count += 1
        else:
            body = existing_body or "暂时没有对话……"
            empty_count += 1

        parts.append(f"== {other_zh} ==\n{body}")

    output_text = "\n\n".join(parts).rstrip() + "\n"
    output_text = re.sub(r"(\{\{#section-h:[^\n]+)\n\n(?=== )", r"\1\n", output_text)
    output_text = re.sub(r"(\{\{ow-dialog-module-(?:tank|damage)\|[^\n]+)\n\n(?=(?:\{\{ow-dialog-module-|== ))", r"\1\n", output_text)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output_text, encoding="utf-8")
    print(f"目标英雄：{target_zh}")
    print(f"全文章节：{full_count}")
    print(f"引用章节：{ref_count}")
    print(f"空章节：{empty_count}")
    print(f"模块章节：{module_count}")
    print(f"输出：{args.output}")


if __name__ == "__main__":
    main()
