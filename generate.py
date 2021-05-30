# -*- coding: utf-8 -*-

title = '''# awesome-github-collection
GitHub 个人收藏
'''


def generate_content():
    import json
    with open("data.json", "r") as f:
        text = f.read()
    data = {}
    for item in json.loads(text):
        name = item["name"]
        url = item.get("url", f"https://github.com/{name}")
        parts = [f"- [{name}]({url})"]
        icon_url = item.get("icon_url", None)
        if icon_url is not None:
            parts.append(
                f"![](https://img.shields.io/github/stars/{name})" if len(
                    icon_url) == 0 else "".join([f"![]({i})" for i in icon_url])
            )
        if item.get("description", None):
            parts.append("\- "+item["description"])
        keys = item["type"].split("/")
        temp = data
        for k in keys:
            temp = temp.setdefault(k, {})
        temp.setdefault("write", []).append("\n".join(parts))
    to_write = ""
    for k, v in data.items():
        to_write += get_content_to_write(k, v, "#") + "\n"
    return to_write


def get_content_to_write(k, v, head):
    to_write = f"\n{head} {k}"
    if "write" in v.keys():
        to_write += "\n"+"\n".join(v.pop("write"))
    for k1, v1 in v.items():
        to_write += get_content_to_write(k1, v1, head+"#")
    return to_write


def generate_toc():
    import os
    with open("data.json", "r") as f:
        text = f.read()
    toc = ""
    with os.popen('./gh-md-toc README.md') as cmd:
        for line in cmd.readlines():
            if "*" in line:
                toc += line
    return toc


def write_output(data):
    with open("README.md", "w") as f:
        f.write(data)


if __name__ == "__main__":
    content = generate_content()
    write_output(content)
    toc = generate_toc()
    split_line = "\n---\n"
    data = title + split_line + "\n"+toc + split_line + content
    write_output(data)
