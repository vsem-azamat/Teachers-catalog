import re
import pytest
from bot.text_assets import TextMenu

# Инициализация данных для тестов
TEST_INNER_DICTS = []
text_menu_instance = TextMenu
for inner_class in text_menu_instance.__dict__.values():
    if inner_class == TextMenu:
        continue
    if isinstance(inner_class, type):
        for inner_dict in inner_class.__dict__.values():
            if isinstance(inner_dict, dict):
                TEST_INNER_DICTS.append(inner_dict)


@pytest.mark.parametrize("inner_dict", TEST_INNER_DICTS)
def test_find_all_language_in_dicts(inner_dict):
    """
    Check that all dictionaries have 4 languages (ru, en, cz, ua)
    """
    if inner_dict == 'languages':
        pytest.skip("Skipping dicts with languages")
    if isinstance(list(inner_dict.keys())[0], bool):
        pytest.skip("Skipping dicts with bool keys")
    if "🇷🇺" in inner_dict.keys():
        pytest.skip("Skipping dicts with emoji keys")

    for language in ['ru', 'en', 'cz', 'ua']:
        assert language in inner_dict.keys(), f"Dict {inner_dict} doesn't have language {language}"


@pytest.mark.parametrize("inner_dict", TEST_INNER_DICTS)
def test_check_all_html_tags(inner_dict):
    """
    Check correctness of HTML tags in dictionary values
    """
    open_tag_pattern = re.compile(r'<[^/][^>]*>')
    closed_tag_pattern = re.compile(r'</[^>]+>')
    for dict_value in inner_dict.values():
        if isinstance(dict_value, str):
            open_tags = open_tag_pattern.findall(dict_value)
            closed_tags = closed_tag_pattern.findall(dict_value)
            assert len(open_tags) == len(closed_tags), f"Dict {inner_dict} has incorrect html tags\n Open tags: {open_tags}\n Closed tags: {closed_tags}"
