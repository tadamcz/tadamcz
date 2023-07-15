import datetime
import json
from htmlmin import minify
import humanize
from jinja2 import Template
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
    repo_data['description'] = repo_data['description'] + "&nbsp; " * (110 - length)

    # Homepage
    homepage = repo_data['homepage']
    if homepage:
        # Remove the scheme, protocol and trailing slash
        homepage_name = homepage.replace("https://", "").replace("http://", "").rstrip("/")
    else:
        homepage_name = ""

    # Calculate the humanized updated_at value
    updated_at = datetime.datetime.now() - datetime.timedelta(days=repo_data['updated_at'])
    updated_at_humanized = humanize.naturaltime(updated_at)

    # Generate the HTML
    template = open('repo.html').read()
    template = Template(template)
    html = template.render(
        url=repo_data['url'],
        name=repo_data['name'],
        language=repo_data['language'],
        language_image_url=language_image_url,
        homepage=homepage,
        description=repo_data['description'],
        homepage_name=homepage_name,
        stars=repo_data['stars'],
        updated_at_humanized=updated_at_humanized,
        private=repo_data['private'],
    )
    html = minify(html)  # Strip whitespace for Markdown compatibility
    html = "\n\n" + html + "\n\n"  # Separate repos with newlines for readability
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
        for repo_name in category:
            html += generate_repo_html(data[repo_name])
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

    md += f"<hr><p>This file was generated on {datetime.date.today()} using data from the GitHub API.</p>"

    # Write the HTML to a file
    with open('README.md', 'w') as f:
        f.write(md)
