import datetime
import json
import os

from github import Github

from repos import repos

# Github token for authenticated requests
g = Github(os.environ['GITHUB_TOKEN'])


def get_repo_info(username, repo_name):
    repo = g.get_user(username).get_repo(repo_name)
    if repo.private:
        raise ValueError(f"Repo {repo_name} is private")
    data = {
        "name": repo.name,
        "description": repo.description,
        "language": repo.language,
        "stars": repo.stargazers_count,
        "updated_at": (datetime.datetime.now() - repo.updated_at).days,
        "url": repo.html_url,
    }
    return data


def save_to_json(repos_nested):
    data = {}

    def save_category(category):
        if isinstance(category, list):
            for repo_name in category:
                data[repo_name] = get_repo_info("tadamcz", repo_name)
        else:
            for subcategory in category.values():
                save_category(subcategory)

    for category in repos_nested.values():
        save_category(category)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    save_to_json(repos)
