import os
import json
import yaml
import datetime
import urllib.parse

# === 配置路径 ===
obsidian_vault_path = "."  # <<< 修改为你的 Obsidian 笔记库路径
vault_name = "markdown"  # <<< 修改为 Obsidian 中实际 vault 名
output_json_path = os.path.join(obsidian_vault_path, "index.json")

now = datetime.datetime.now().isoformat()

def extract_metadata_and_content(file_path):
    """解析 Obsidian Markdown 文件的 YAML Frontmatter + 正文"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        return {}, ""

    metadata = {}
    content_lines = []
    is_yaml = False
    yaml_lines = []
    in_yaml = False
    yaml_done = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        # 开始 YAML
        if stripped == "---" and not in_yaml and not yaml_done:
            in_yaml = True
            continue
        # 结束 YAML
        elif stripped == "---" and in_yaml:
            in_yaml = False
            yaml_done = True
            continue

        if in_yaml:
            yaml_lines.append(line)
        else:
            content_lines.append(line)  # 不 strip，保留 Markdown 格式

    try:
        metadata = yaml.safe_load("".join(yaml_lines)) or {}
        if not isinstance(metadata, dict):
            metadata = {}
    except yaml.YAMLError:
        metadata = {}

    content = "".join(content_lines).strip()
    return metadata, content

def generate_index():
    notes = []

    for root, _, files in os.walk(obsidian_vault_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, obsidian_vault_path)
                metadata, content = extract_metadata_and_content(file_path)

                title = metadata.get("title", file.replace(".md", ""))
                created = metadata.get("created", now)
                updated = metadata.get("updated", now)
                category = metadata.get("category", "Uncategorized")
                subcategory = metadata.get("subcategory", "")
                tags = metadata.get("tags", [])
                lang = metadata.get("lang", "en")

                # 编码文件路径供 Obsidian URI 使用
                uri_file_path = urllib.parse.quote(rel_path)
                obsidian_url = f"obsidian://open?vault={vault_name}&file={uri_file_path}"

                notes.append({
                    "title": title,
                    "created": created,
                    "updated": updated,
                    "category": category,
                    "subcategory": subcategory,
                    "tags": tags,
                    "url": obsidian_url,
                    "lang": lang,
                    "filepath": rel_path,
                    "content": content
                })

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    print(f"✅ index.json 已生成，共处理 {len(notes)} 个笔记。")
