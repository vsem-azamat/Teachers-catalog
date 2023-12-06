import os
import sys
import re
import unittest
from bot.text_assets import TextMenu

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTextMenu(unittest.TestCase):
    TEST_INNER_DICTS = []
    text_menu_instance = TextMenu
    for inner_class in text_menu_instance.__dict__.values():
        if inner_class == TextMenu:
            continue
        # Add all dicts in inner_class
        if isinstance(inner_class, type):
            # Get all dicts in inner_class
            for inner_dict in inner_class.__dict__.values():
                if isinstance(inner_dict, dict):
                    TEST_INNER_DICTS.append(inner_dict)


    def test_find_all_language_in_dicts(self):
        """
        Check if all dicts has 4 languages (ru, en, cz, ua)
        """
        for inner_dict in self.TEST_INNER_DICTS:
            # Skip dicts with languages
            if inner_dict == 'languages':
                continue
            
            # Skip dicts with bool keys
            if isinstance(list(inner_dict.keys())[0], bool):
                continue
            
            # Skip dicts with emoji keys
            if "🇷🇺" in inner_dict.keys():
                continue

            # Check if all dicts has 4 languages
            with self.subTest(inner_dict=inner_dict):
                for language in ['ru', 'en', 'cz', 'ua']:

                    self.assertIn(
                        language, 
                        inner_dict.keys(),
                        f"Dict {inner_dict} doesn't have language {language}"
                        )

    # TODO: I'm not sure if this regex is good idea
    # I'm tryed py_w3c.validators.html.validator but it's so slow and strange work
    def test_check_all_html_tags(self):
        """
        Check if all dicts has correct html tags
        """
        # Define patterns
        open_tag_pattern = re.compile(r'<[^/][^>]*>')
        closed_tag_pattern = re.compile(r'</[^>]+>')

        # Iterate over all dicts
        for inner_dict in self.TEST_INNER_DICTS:
            # Iterate over all values in dict
            for dict_value in inner_dict.values():
                # Check if value is string
                if isinstance(dict_value, str):
                    with self.subTest(dict_value=dict_value):
                        open_tags = open_tag_pattern.findall(dict_value)
                        closed_tags = closed_tag_pattern.findall(dict_value)
                        self.assertEqual(
                            len(open_tags), 
                            len(closed_tags),
                            f"Dict {inner_dict} has incorrect html tags\n Open tags: {open_tags}\n Closed tags: {closed_tags}"
                            )


if __name__ == '__main__':
    unittest.main()