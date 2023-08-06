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
        "pushed_at": (datetime.datetime.now() - repo.pushed_at).days,
        "url": repo.html_url,
        "homepage": repo.homepage,
        "private": repo.private,
        "owner": repo.owner.login,
    }
    return data


def save_to_json(repos_nested):
    data = {}

    def save(obj):
        if isinstance(obj, str):  # Base case
            if "/" in obj:
                # Fully qualified name, e.g. "tom/myrepo"
                info = get_repo_info(obj)
            else:
                # Assume "tadamcz" as the owner
                info = get_repo_info(f"tadamcz/{obj}")
            data[obj] = info
        if isinstance(obj, list):
            for repo_name in obj:
                save(repo_name)
        elif isinstance(obj, dict):
            for category_name, category_items in obj.items():
                save(category_items)

    save(repos_nested)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    save_to_json(repos)
