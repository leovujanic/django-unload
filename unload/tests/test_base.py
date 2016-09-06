# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.apps import apps
from django.conf import settings
from django.test import TestCase

from ..base import Template
from ..utils import get_contents


class TestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        The setUpClass is used because the templates paths are not changed in
        the following tests.
        """
        super(TestBase, cls).setUpClass()
        # Find directories with templates
        templates_dir = settings.TEMPLATES[0]['DIRS'][0]
        app = apps.get_app_config('app')
        app_templates = os.path.join(app.path, 'templates', 'app', 'templates')
        app_tags = os.path.join(app.path, 'templates', 'app', 'tags')
        # Save the path of each template for further testing
        cls.master_template = os.path.join(templates_dir, 'master.html')
        cls.tag_template = os.path.join(app_tags, 'tag_template.html')
        cls.double_loads = os.path.join(app_templates, 'double_loads.html')
        cls.with_tags = os.path.join(app_templates, 'with_tags.html')
        cls.without_tags = os.path.join(app_templates, 'without_tags.html')
        cls.from_syntax_with_tags = os.path.join(app_templates,
                                                 'from_syntax_with_tags.html')
        cls.from_syntax_without_tags = os.path.join(app_templates,
                                                    'from_syntax_without_tags.html')

    def test_get_tokens_master_template(self):
        master_template = Template(
            template_string=get_contents(self.master_template),
            name=self.master_template)

        self.assertEqual(master_template.tokens[1].split_contents(),
                         ['block', 'title'])
        self.assertEqual(master_template.tokens[3].split_contents(),
                         ['endblock', 'title'])
        self.assertEqual(master_template.tokens[5].split_contents(),
                         ['block', 'body'])
        self.assertEqual(master_template.tokens[7].split_contents(),
                         ['endblock', 'body'])

    def test_get_tokens_tag_template(self):
        # Test tag template
        tag_template = Template(
            template_string=get_contents(self.tag_template),
            name=self.tag_template)
        self.assertEqual(tag_template.tokens[1].contents, 'tag_name')

    def test_get_tokens_double_loads(self):
        # Test double loads
        double_loads = Template(
            template_string=get_contents(self.double_loads),
            name=self.double_loads)

        self.assertEqual(double_loads.tokens[0].split_contents(),
                         ['extends', '"master.html"'])
        self.assertEqual(double_loads.tokens[2].split_contents(),
                         ['load', 'app_tags'])
        self.assertEqual(double_loads.tokens[4].split_contents(),
                         ['load', 'app_tags'])
        self.assertEqual(double_loads.tokens[6].split_contents(),
                         ['block', 'body'])
        self.assertEqual(double_loads.tokens[8].split_contents(),
                         ['endblock', 'body'])

    def test_get_tokens_with_tags(self):
        with_tags = Template(
            template_string=get_contents(self.with_tags),
            name=self.with_tags)
        self.assertEqual(with_tags.tokens[0].split_contents(),
                         ['extends', '"master.html"'])
        self.assertEqual(with_tags.tokens[2].split_contents(),
                         ['load', 'app_tags'])
        self.assertEqual(with_tags.tokens[4].split_contents(),
                         ['block', 'body'])
        self.assertEqual(with_tags.tokens[6].split_contents(),
                         ['example_inclusion_tag'])
        self.assertEqual(with_tags.tokens[8].split_contents(),
                         ['example_simple_tag'])
        self.assertEqual(with_tags.tokens[10].split_contents(),
                         ['example_assignment_tag', 'as', 'example'])
        self.assertEqual(with_tags.tokens[12].split_contents(),
                         ['2|plus:5'])
        self.assertEqual(with_tags.tokens[14].split_contents(),
                         ['endblock', 'body'])

    def test_get_tokens_from_syntax_with_tags(self):
        from_syntax_with_tags = Template(
            template_string=get_contents(self.from_syntax_with_tags),
            name=self.from_syntax_with_tags)

        self.assertEqual(from_syntax_with_tags.tokens[0].split_contents(),
                         ['extends', '"master.html"'])
        self.assertEqual(from_syntax_with_tags.tokens[2].split_contents(),
                         ['load', 'example_inclusion_tag',
                          'example_simple_tag', 'example_assignment_tag',
                          'plus', 'from', 'app_tags'])
        self.assertEqual(from_syntax_with_tags.tokens[4].split_contents(),
                         ['block', 'body'])
        self.assertEqual(from_syntax_with_tags.tokens[6].split_contents(),
                         ['example_inclusion_tag'])
        self.assertEqual(from_syntax_with_tags.tokens[8].split_contents(),
                         ['example_simple_tag'])
        self.assertEqual(from_syntax_with_tags.tokens[10].split_contents(),
                         ['example_assignment_tag', 'as', 'example'])
        self.assertEqual(from_syntax_with_tags.tokens[12].split_contents(),
                         ['2|plus:5'])
        self.assertEqual(from_syntax_with_tags.tokens[14].split_contents(),
                         ['endblock', 'body'])

    def test_get_tokens_without_tags(self):
        without_tags = Template(
            template_string=get_contents(self.without_tags),
            name=self.without_tags)

        self.assertEqual(without_tags.tokens[0].split_contents(),
                         ['extends', '"master.html"'])
        self.assertEqual(without_tags.tokens[2].split_contents(),
                         ['load', 'app_tags'])
        self.assertEqual(without_tags.tokens[4].split_contents(),
                         ['block', 'body'])
        self.assertEqual(without_tags.tokens[6].split_contents(),
                         ['endblock', 'body'])

    def test_get_tokens_from_syntax_without_tags(self):
        # Test double loads
        from_syntax_without_tags = Template(
            template_string=get_contents(self.from_syntax_without_tags),
            name=self.from_syntax_without_tags)

        self.assertEqual(from_syntax_without_tags.tokens[0].split_contents(),
                         ['extends', '"master.html"'])
        self.assertEqual(from_syntax_without_tags.tokens[2].split_contents(),
                         ['load', 'example_simple_tag', 'plus', 'from',
                         'app_tags'])
        self.assertEqual(from_syntax_without_tags.tokens[4].split_contents(),
                         ['block', 'body'])
        self.assertEqual(from_syntax_without_tags.tokens[6].split_contents(),
                         ['endblock', 'body'])

    def test_parse_load_block(self):

        master_template = Template(
            template_string=get_contents(self.master_template),
            name=self.master_template)
        self.assertEqual(master_template.loaded_modules, {})
        self.assertEqual(master_template.loaded_members, {})

        tag_template = Template(
            template_string=get_contents(self.tag_template),
            name=self.tag_template)
        self.assertEqual(tag_template.loaded_modules, {})
        self.assertEqual(tag_template.loaded_members, {})

        double_loads = Template(
            template_string=get_contents(self.double_loads),
            name=self.double_loads)
        self.assertEqual(double_loads.loaded_modules,
                         {'app_tags': [2, 3]})
        self.assertEqual(double_loads.loaded_members, {})

        with_tags = Template(
            template_string=get_contents(self.with_tags),
            name=self.with_tags)
        self.assertEqual(with_tags.loaded_modules,
                         {'app_tags': [2]})
        self.assertEqual(with_tags.loaded_members, {})

        from_syntax_with_tags = Template(
            template_string=get_contents(self.from_syntax_with_tags),
            name=self.from_syntax_with_tags)
        self.assertEqual(from_syntax_with_tags.loaded_modules,
                         {'app_tags': [2]})
        self.assertEqual(from_syntax_with_tags.loaded_members,
                         {
                            'example_assignment_tag': [2],
                            'example_inclusion_tag': [2],
                            'example_simple_tag': [2],
                            'plus': [2]
                         })

        without_tags = Template(
            template_string=get_contents(self.without_tags),
            name=self.without_tags)
        self.assertEqual(without_tags.loaded_modules,
                         {'app_tags': [2]})
        self.assertEqual(without_tags.loaded_members, {})

        from_syntax_without_tags = Template(
            template_string=get_contents(self.from_syntax_without_tags),
            name=self.from_syntax_without_tags)
        self.assertEqual(from_syntax_without_tags.loaded_modules,
                         {'app_tags': [2]})
        self.assertEqual(from_syntax_without_tags.loaded_members,
                         {
                            'example_simple_tag': [2],
                            'plus': [2]
                         })

    def test_get_used_tags_and_filters(self):

        master_template = Template(
            template_string=get_contents(self.master_template),
            name=self.master_template)
        self.assertEqual(master_template.used_tags, [])
        self.assertEqual(master_template.used_filters, [])

        tag_template = Template(
            template_string=get_contents(self.tag_template),
            name=self.tag_template)
        self.assertEqual(tag_template.used_tags, [])
        self.assertEqual(tag_template.used_filters, [])

        double_loads = Template(
            template_string=get_contents(self.double_loads),
            name=self.double_loads)
        self.assertEqual(double_loads.used_tags, [])
        self.assertEqual(double_loads.used_filters, [])

        with_tags = Template(
            template_string=get_contents(self.with_tags),
            name=self.with_tags)
        self.assertEqual(with_tags.used_tags,
                         ['example_inclusion_tag', 'example_simple_tag',
                          'example_assignment_tag'])
        self.assertEqual(with_tags.used_filters, ['plus'])

        from_syntax_with_tags = Template(
            template_string=get_contents(self.from_syntax_with_tags),
            name=self.from_syntax_with_tags)
        self.assertEqual(from_syntax_with_tags.used_tags,
                         ['example_inclusion_tag', 'example_simple_tag',
                          'example_assignment_tag'])
        self.assertEqual(from_syntax_with_tags.used_filters, ['plus'])

        without_tags = Template(
            template_string=get_contents(self.without_tags),
            name=self.without_tags)
        self.assertEqual(without_tags.used_tags, [])
        self.assertEqual(without_tags.used_filters, [])

        from_syntax_without_tags = Template(
            template_string=get_contents(self.from_syntax_without_tags),
            name=self.from_syntax_without_tags)
        self.assertEqual(from_syntax_without_tags.used_tags, [])
        self.assertEqual(from_syntax_without_tags.used_filters, [])
