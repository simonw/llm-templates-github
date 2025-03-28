import pytest
from llm_templates_github import github_template_loader
from llm import Template
import yaml


@pytest.mark.parametrize(
    "template_path, expected_url, yaml_content_dict",
    [
        # Test case 1: Full path (user/repo/template) with simple string content
        (
            "testuser/testrepo/simple",
            "https://raw.githubusercontent.com/testuser/testrepo/main/simple.yaml",
            "Just a simple prompt.",
        ),
        # Test case 2: Short path (user/template) with simple string content
        (
            "testuser/short",
            "https://raw.githubusercontent.com/testuser/llm-templates/main/short.yaml",
            "Shorthand prompt.",
        ),
        # Test case 3: Full path with dictionary content
        (
            "dev/coolstuff/complex",
            "https://raw.githubusercontent.com/dev/coolstuff/main/complex.yaml",
            {
                "prompt": "Complex prompt with {{variable}}",
                "system": "You are helpful.",
                "model": "gpt-4",
            },
        ),
        # Test case 4: Short path with dictionary content
        (
            "dev/dict_template",
            "https://raw.githubusercontent.com/dev/llm-templates/main/dict_template.yaml",
            {"prompt": "Another dict prompt", "system": "Be concise"},
        ),
    ],
)
def test_github_loader_success(
    httpx_mock, template_path, expected_url, yaml_content_dict
):
    """Tests successful loading of templates via different paths and content types."""
    if isinstance(yaml_content_dict, dict):
        yaml_string = yaml.dump(yaml_content_dict)
        expected_template = Template(name=template_path, **yaml_content_dict)
    else:  # It's a string
        yaml_string = yaml_content_dict
        expected_template = Template(name=template_path, prompt=yaml_content_dict)

    httpx_mock.add_response(
        url=expected_url, method="GET", text=yaml_string, status_code=200
    )

    template = github_template_loader(template_path)

    assert template == expected_template
    # Check specific fields if __eq__ is not comprehensive
    assert template.name == template_path
    if isinstance(yaml_content_dict, dict):
        assert template.prompt == yaml_content_dict.get("prompt")
        assert template.system == yaml_content_dict.get("system")
        assert template.model == yaml_content_dict.get("model")
    else:
        assert template.prompt == yaml_content_dict
        assert template.system is None  # Assuming default is None
        assert template.model is None  # Assuming default is None
