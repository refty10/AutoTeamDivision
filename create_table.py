import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from html2image import Html2Image


def create_table(members):
    template = ""
    with open('template.html', 'r', encoding='UTF-8') as f:
        template = f.read()

    md = f"{template}"\
         "|ブルーチーム|レッドチーム|\n"\
         "|:----------:|:----------:|\n"

    for index, member in enumerate(members):
        if index % 2 == 0:
            md += f"|{member['name']}: <span>{member['rank']}</span>|"
        else:
            md += f"{member['name']}: <span>{member['rank']}</span>|\n"

    html = markdown.markdown(md,
                             extensions=[GithubFlavoredMarkdownExtension()])

    with open('team.html', 'w', encoding="UTF-8") as f:
        f.write(html)

    hti = Html2Image()
    hti.screenshot(html_str=html, save_as='team.png', size=(405, 160))
