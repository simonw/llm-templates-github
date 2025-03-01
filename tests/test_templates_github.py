import llm


def test_plugin_is_installed():
    assert "gh" in llm.get_template_loaders()
