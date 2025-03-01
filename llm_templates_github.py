from llm import Template, hookimpl, user_dir
import yaml
import httpx
from pathlib import Path


@hookimpl
def register_template_loaders(register):
    register("gh", github_template_loader)


def get_cache_dir() -> Path:
    return user_dir() / "templates_github"


def github_template_loader(template_path: str) -> Template:
    """
    Load a template from GitHub or local cache if available

    Format: username/repo/template_name (without the .yaml extension)
      or username/template_name which means username/llm-templates/template_name
    """
    parts = template_path.split("/")
    if len(parts) == 2:
        parts.insert(1, "llm-templates")
    elif len(parts) != 3:
        raise ValueError(
            "GitHub template format should be 'username/repo/template_name' or 'username/template_name'"
        )

    username, repo, template_name = parts

    repo_path = f"{username}/{repo}"

    # Check if template exists in cache
    cache_dir = get_cache_dir()
    cache_file = cache_dir / repo_path / f"{template_name}.yaml"

    if cache_file.exists():
        try:
            # Load from cache
            loaded = yaml.safe_load(cache_file.read_text())
            if isinstance(loaded, str):
                return Template(name=template_path, prompt=loaded)

            return Template(name=template_path, **loaded)
        except Exception:
            # If cache loading fails, try fetching from GitHub
            pass

    content = None
    path = f"{template_name}.yaml"
    url = f"https://raw.githubusercontent.com/{username}/{repo}/main/{path}"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            content = response.text
    except httpx.HTTPError:
        pass

    if not content:
        raise ValueError(
            f"Template '{template_name}' not found in repository '{repo_path}'"
        )

    # Parse YAML and create template
    try:
        loaded = yaml.safe_load(content)
        if isinstance(loaded, str):
            template = Template(name=template_path, prompt=loaded)
        else:
            template = Template(name=template_path, **loaded)

        # Cache the template
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(content)

        return template
    except yaml.YAMLError as ex:
        raise ValueError(f"Invalid YAML in GitHub template: {ex}")
