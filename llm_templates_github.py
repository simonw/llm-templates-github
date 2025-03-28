from llm import Template, hookimpl
import yaml
import httpx


@hookimpl
def register_template_loaders(register):
    register("gh", github_template_loader)


def github_template_loader(template_path: str) -> Template:
    """
    Load a template from GitHub

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

    # Fetch template directly from GitHub
    path = f"{template_name}.yaml"
    url = f"https://raw.githubusercontent.com/{username}/{repo}/main/{path}"

    try:
        response = httpx.get(url)
        if response.status_code == 200:
            content = response.text
        else:
            raise ValueError(
                f"Template '{template_name}' not found in repository '{username}/{repo}' (HTTP {response.status_code})"
            )
    except httpx.HTTPError as ex:
        raise ValueError(f"Failed to fetch template from GitHub: {ex}")

    # Parse YAML and create template
    try:
        loaded = yaml.safe_load(content)
        if isinstance(loaded, str):
            return Template(name=template_path, prompt=loaded)
        else:
            return Template(name=template_path, **loaded)
    except yaml.YAMLError as ex:
        raise ValueError(f"Invalid YAML in GitHub template: {ex}")
