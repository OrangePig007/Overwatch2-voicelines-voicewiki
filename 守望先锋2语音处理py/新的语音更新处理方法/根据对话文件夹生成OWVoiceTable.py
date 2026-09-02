import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


DEFAULT_BASE_DIR = Path(r"G:\守望语音\ow-dmon-ver")
DEFAULT_ZH_DIR = DEFAULT_BASE_DIR / "对话(zh)"
DEFAULT_EN_DIR = DEFAULT_BASE_DIR / "对话(en)"
DEFAULT_OUTPUT = DEFAULT_BASE_DIR / "对话output.txt"
DEFAULT_LOG = DEFAULT_BASE_DIR / "对话output_log.txt"

CONVO_DIR_RE = re.compile(r"^[0-9A-Fa-f]{12}\.[^.]+$")
VOICE_FILE_RE = re.compile(r"^(\d+)-(.+?)-([0-9A-Fa-f]{12}\.[^-]+)(?:-(.*))?$")
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
    "JetpackCat": "Jetpack Cat",
    "Unknown54": "Genji",
    "Unknown278": "Juno",
    "UnknownA6": "Lucio",
    "Unknown1": "Reaper",
    "Unknown4": "Pharah",
}
EN_HERO_RANK = {name: index for index, (name, _) in enumerate(HERO_ORDER)}
ZH_HERO_RANK = {name: index for index, (_, name) in enumerate(HERO_ORDER)}


def parse_args():
    parser = argparse.ArgumentParser(description="根据中英文对话文件夹生成 OWVoiceTable 文本。")
    parser.add_argument("--zh-dir", type=Path, default=DEFAULT_ZH_DIR, help=f"中文对话目录，默认：{DEFAULT_ZH_DIR}")
    parser.add_argument("--en-dir", type=Path, default=DEFAULT_EN_DIR, help=f"英文对话目录，默认：{DEFAULT_EN_DIR}")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT, help=f"输出 txt，默认：{DEFAULT_OUTPUT}")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help=f"问题日志，默认：{DEFAULT_LOG}")
    return parser.parse_args()


def restore_filename_text(text, lang, zh_hint=""):
    text = (text or "").strip()
    if not text:
        return ""

    if lang == "zh":
        text = text.replace(")_ ", ") ")
        text = text.replace("）_ ", "） ")
        text = re.sub(r"_(.+?)_", r"“\1”", text)
        text = text.replace("_", "?")
        text = text.replace("（", "(").replace("）：", ")").replace("）", ")")
    else:
        text = text.replace(")_ ", ") ")
        text = restore_english_placeholders(text, zh_hint)

    if lang == "en" and text and text[-1] not in ".!?)”’…":
        text += "."

    return text


def restore_english_placeholders(text, zh_hint=""):
    chars = list(text)
    underscore_indexes = [index for index, char in enumerate(chars) if char == "_"]
    quote_indexes = set()

    for left, right in zip(underscore_indexes, underscore_indexes[1:]):
        before_left = chars[left - 1] if left > 0 else ""
        after_left = chars[left + 1] if left + 1 < len(chars) else ""
        before_right = chars[right - 1] if right > 0 else ""
        after_right = chars[right + 1] if right + 1 < len(chars) else ""

        left_can_open = left == 0 or before_left.isspace() or before_left in "([{"
        right_can_close = right == len(chars) - 1 or after_right.isspace() or after_right in ".,!?)]}…"
        inner_text = "".join(chars[left + 1 : right]).strip()

        if left_can_open and after_left and not after_left.isspace() and before_right and not before_right.isspace() and right_can_close and inner_text:
            quote_indexes.add(left)
            quote_indexes.add(right)

    result = []
    open_quote = True
    for index, char in enumerate(chars):
        if char != "_":
            result.append(char)
        elif index in quote_indexes:
            result.append('"' if open_quote else '"')
            open_quote = not open_quote
        else:
            next_non_space = ""
            for next_char in chars[index + 1 :]:
                if not next_char.isspace():
                    next_non_space = next_char
                    break
            if index + 1 < len(chars) and chars[index + 1].isspace() and next_non_space.islower():
                if "：" in zh_hint or ":" in zh_hint:
                    result.append(":")
                elif "，" in zh_hint or "," in zh_hint:
                    result.append(",")
                else:
                    result.append(":")
            else:
                result.append("?")

    return "".join(result)


def collect_conversation_dirs(root):
    conversations = {}
    for path in root.rglob("*"):
        if path.is_dir() and CONVO_DIR_RE.match(path.name):
            conversations.setdefault(path.name.upper(), path)
    return conversations


def description_dirs(conversation_dir):
    return [path.name for path in conversation_dir.iterdir() if path.is_dir()]


def parse_voice_file(path, lang, fallback_text=""):
    match = VOICE_FILE_RE.match(path.stem)
    if not match:
        return None

    order = int(match.group(1))
    hero = match.group(2).strip()
    file_id = match.group(3).strip()
    raw_text = match.group(4) or fallback_text

    return {
        "order": order,
        "hero": hero,
        "file": file_id,
        "raw_text": raw_text,
        "text": restore_filename_text(raw_text, lang),
        "name": path.name,
    }


def collect_voice_entries(conversation_dir, lang, logs):
    entries = []
    desc_names = description_dirs(conversation_dir)
    direct_files = sorted(path for path in conversation_dir.iterdir() if path.is_file() and path.suffix.lower() == ".ogg")

    # 部分无文字音频会复制在一个描述性子文件夹里，例如 “(questioning meows)”。
    desc_by_file = {}
    for desc_dir in [path for path in conversation_dir.iterdir() if path.is_dir()]:
        for file_path in desc_dir.glob("*.ogg"):
            desc_by_file[file_path.name] = desc_dir.name

    files = direct_files
    if not files:
        files = sorted(path for path in conversation_dir.rglob("*.ogg") if path.is_file())

    for file_path in files:
        fallback = desc_by_file.get(file_path.name, "")
        parsed = parse_voice_file(file_path, lang, fallback)
        if parsed:
            entries.append(parsed)
        else:
            logs.append(f"[无法解析文件名] {file_path}")

    if desc_names and not desc_by_file:
        logs.append(f"[描述目录未匹配音频] {conversation_dir} | {'、'.join(desc_names)}")

    grouped = defaultdict(list)
    for entry in entries:
        grouped[entry["order"]].append(entry)

    ordered = []
    for order in sorted(grouped):
        ordered.extend(sorted(grouped[order], key=lambda item: item["file"]))
    return ordered


def hero_rank(en_hero, zh_hero=""):
    normalized_en = EN_ALIASES.get(en_hero, en_hero)
    if normalized_en in EN_HERO_RANK:
        return EN_HERO_RANK[normalized_en]
    if zh_hero in ZH_HERO_RANK:
        return ZH_HERO_RANK[zh_hero]
    return len(HERO_ORDER) + 999


def display_hero_name(en_hero):
    return EN_ALIASES.get(en_hero, en_hero)


def conversation_sort_key(conversation_id, en_entries, zh_entries):
    zh_by_order = defaultdict(list)
    for entry in zh_entries:
        zh_by_order[entry["order"]].append(entry)

    zh_used = defaultdict(int)
    ranks = []
    for en_entry in en_entries:
        order = en_entry["order"]
        zh_index = zh_used[order]
        zh_entry = zh_by_order[order][zh_index] if zh_index < len(zh_by_order[order]) else None
        zh_used[order] += 1
        ranks.append(hero_rank(en_entry["hero"], zh_entry["hero"] if zh_entry else ""))

    unique_ranks = tuple(sorted(set(ranks)))
    return (unique_ranks, conversation_id)


def build_table(conversation_id, en_entries, zh_entries, logs):
    lines = ["{{OWVoiceTable"]
    zh_by_order = defaultdict(list)
    for entry in zh_entries:
        zh_by_order[entry["order"]].append(entry)

    zh_used = defaultdict(int)
    for index, en_entry in enumerate(en_entries, start=1):
        order = en_entry["order"]
        zh_index = zh_used[order]
        zh_entry = zh_by_order[order][zh_index] if zh_index < len(zh_by_order[order]) else None
        zh_used[order] += 1

        zh_text = zh_entry["text"] if zh_entry else ""
        en_text = restore_filename_text(en_entry["raw_text"], "en", zh_text) if en_entry["raw_text"] else en_entry["text"]
        if not zh_entry:
            logs.append(f"[缺少中文行] {conversation_id} | order={order} | {en_entry['name']}")

        lines.append(
            f"|hero{index}={display_hero_name(en_entry['hero'])}|file{index}={en_entry['file']}|en{index}={en_text}|zh{index}={zh_text}"
        )

    for order, entries in zh_by_order.items():
        if zh_used[order] < len(entries):
            for extra in entries[zh_used[order] :]:
                logs.append(f"[中文行未使用] {conversation_id} | order={order} | {extra['name']}")

    lines.append("}}")
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    logs = []
    zh_dirs = collect_conversation_dirs(args.zh_dir)
    en_dirs = collect_conversation_dirs(args.en_dir)
    all_ids = sorted(set(zh_dirs) | set(en_dirs))

    table_items = []
    built_count = 0
    for conversation_id in all_ids:
        en_dir = en_dirs.get(conversation_id)
        zh_dir = zh_dirs.get(conversation_id)
        if not en_dir:
            logs.append(f"[缺少英文目录] {conversation_id} | zh={zh_dir}")
            continue
        if not zh_dir:
            logs.append(f"[缺少中文目录] {conversation_id} | en={en_dir}")

        en_entries = collect_voice_entries(en_dir, "en", logs)
        zh_entries = collect_voice_entries(zh_dir, "zh", logs) if zh_dir else []
        if not en_entries:
            logs.append(f"[英文目录无音频] {conversation_id} | {en_dir}")
            continue

        table_items.append(
            (
                conversation_sort_key(conversation_id, en_entries, zh_entries),
                build_table(conversation_id, en_entries, zh_entries, logs),
            )
        )
        built_count += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    tables = [table for _, table in sorted(table_items, key=lambda item: item[0])]
    args.output.write_text("\n\n".join(tables) + ("\n" if tables else ""), encoding="utf-8")
    args.log.write_text("\n".join(logs) + ("\n" if logs else ""), encoding="utf-8")

    print(f"英文对话目录：{len(en_dirs)}")
    print(f"中文对话目录：{len(zh_dirs)}")
    print(f"生成对话表：{built_count}")
    print(f"输出文件：{args.output}")
    print(f"问题日志：{args.log}（{len(logs)} 条）")


if __name__ == "__main__":
    main()
