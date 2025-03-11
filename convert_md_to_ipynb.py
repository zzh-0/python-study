import nbformat as nbf
import os
from pathlib import Path


# 定义一个函数将Markdown内容转换为Notebook单元格
def md_to_notebook_cells(md_content):
    cells = []
    current_cell = {"cell_type": "markdown", "source": []}
    lines = md_content.split("\n")
    for line in lines:
        if line.startswith("```python"):
            if current_cell["cell_type"] == "markdown":
                cells.append(
                    nbf.v4.new_markdown_cell("\n".join(current_cell["source"]))
                )
            current_cell = {"cell_type": "code", "source": []}
        elif line.startswith("```"):
            if current_cell["cell_type"] == "code":
                cells.append(nbf.v4.new_code_cell("\n".join(current_cell["source"])))
            current_cell = {"cell_type": "markdown", "source": []}
        else:
            current_cell["source"].append(line)
    if current_cell["source"]:
        if current_cell["cell_type"] == "markdown":
            cells.append(nbf.v4.new_markdown_cell("\n".join(current_cell["source"])))
        elif current_cell["cell_type"] == "code":
            cells.append(nbf.v4.new_code_cell("\n".join(current_cell["source"])))
    return cells


# 定义根目录和输出目录
base_dir = "python宝典"  # 根据实际情况调整根目录
output_base = "python宝典-ipynb"

# 确保输出目录存在
os.makedirs(output_base, exist_ok=True)

# 遍历所有子目录中的 .md 文件
for md_path in Path(base_dir).rglob("*.md"):
    # 构造对应的 .ipynb 输出路径
    relative_path = md_path.relative_to(base_dir)
    ipynb_path = Path(output_base) / relative_path.with_suffix(".ipynb")

    # 创建输出目录（如果不存在）
    os.makedirs(ipynb_path.parent, exist_ok=True)

    # 读取 Markdown 文件内容
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 调用已有的函数将 Markdown 转换为 Notebook 单元格
    cells = md_to_notebook_cells(md_content)
    nb = nbf.v4.new_notebook(cells=cells)

    # 写入 Notebook 文件
    with open(ipynb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"已转换: {md_path} -> {ipynb_path}")

print("全部转换完成！")
