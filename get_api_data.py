import datetime
import json
import os

from github import Github

from repos import repos

# Github token for authenticated requests
g = Github(os.environ['GITHUB_TOKEN'])


def get_repo_info(full_repo_name):
    repo = g.get_repo(full_repo_name)  # Fully qualified name, e.g. "tom/myrepo"
    data = {
        "name": repo.name,
        "description": repo.description,
        "language": repo.language,
        "stars": repo.stargazers_count,
        "updated_at": (datetime.datetime.now() - repo.updated_at).days,
        "url": repo.html_url,
        "homepage": repo.homepage,
        "private": repo.private,
        "owner": repo.owner.login,
    }
    return data


def save_to_json(repos_nested):
    data = {}

    def save_category(category):
        if isinstance(category, list):
            for repo_name_in in category:
                if "/" in repo_name_in:
                    # Fully qualified name, e.g. "tom/myrepo"
                    info = get_repo_info(repo_name_in)
                else:
                    # Assume "tadamcz" as the owner
                    info = get_repo_info(f"tadamcz/{repo_name_in}")
                data[repo_name_in] = info
        else:
            for subcategory in category.values():
                save_category(subcategory)

    for category in repos_nested.values():
        save_category(category)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    save_to_json(repos)
