import datetime
import json

from repos import repos

# Define a default color for languages not present in the colors data
default_color = "#586069"  # GitHub's default text color


# Helper function to generate HTML for a single repo
def generate_repo_html(repo_data):
    # Map the language to the relative URL of a PNG image.
    language_image_url = f'img/{repo_data["language"].lower().replace(" ", "_")}.png'

    # Pad the description with spaces. This makes boxes have the same width.
    # We have very limited formatting options supported on GitHub.com
    length = len(repo_data['description'])
    repo_data['description'] = repo_data['description'] + "&nbsp; " * (200 - length)

    # Homepage
    homepage = repo_data['homepage']
    if homepage:
        # Remove the scheme, protocol and trailing slash
        homepage_name = homepage.replace("https://", "").replace("http://", "").rstrip("/")
    else:
        homepage_name = ""

    # Generate the HTML
    html = f"""
        <div style="border: 1px solid #e1e4e8; padding: 16px; margin: 16px 0;">
            <table style="width: 100%;">
                <tr>
                    <td>
                        <strong>
                            <a href='{repo_data["url"]}'>{repo_data['name']}</a>
                        </strong>
                        <span style="float: right;">
                            <a href='{repo_data.get("homepage", "")}' style="font-size: 12px;">{homepage_name}</a>
                        </span>
                        <p style="margin: 0; font-size: 14px;">{repo_data['description']}</p>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: right;">
                        <a href='{repo_data["url"]}'>
                            <img src="{language_image_url}" alt="" width="12" height="12">
                        </a>
                        {repo_data['language']} &nbsp;&nbsp;
                        <a href='{repo_data["url"]}/stargazers'>
                            <img src="img/star.png" alt="" width="16" height="16">
                        </a>
                        {repo_data['stars']} &nbsp;&nbsp;
                        Updated {repo_data['updated_at']} days ago
                    </td>
                </tr>
            </table>
        </div>
        """
    # Remove indentation
    html = "\n".join([line.strip() for line in html.split("\n")])
    return html


# Helper function to check if a category contains repos or subcategories
def is_repo_list(category):
    # If the category is a list, it contains repos
    if isinstance(category, list):
        return True
    # If the category is a dict, it contains subcategories
    elif isinstance(category, dict):
        return False
    else:
        raise TypeError(f"Invalid type for category: {type(category)}")


# Helper function to generate HTML for a single category
def generate_category_html(category_name, category, level=2):
    html = f"<h{level}>{category_name}</h{level}>"
    if is_repo_list(category):
        for repo_url in category:
            html += generate_repo_html(data[repo_url])
    else:
        for subcategory_name, subcategory in category.items():
            html += generate_category_html(subcategory_name, subcategory, level + 1)
    return html


if __name__ == "__main__":
    # Load the json data
    with open('data.json') as f:
        data = json.load(f)

    # Generate the full Markdown
    md = open('header.md').read()
    for category_name, category in repos.items():
        md += generate_category_html(category_name, category)

    md += f"<hr><p>This file was auto-generated on {datetime.date.today()} using data from the GitHub API.</p>"

    # Write the HTML to a file
    with open('README.md', 'w') as f:
        f.write(md)
