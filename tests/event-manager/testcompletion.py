#!/usr/bin/env python
# vi: set et ts=4:

import unittest
from emtest import EventManagerMock
from uzbl.plugins.config import Config
from uzbl.plugins.keycmd import KeyCmd
from uzbl.plugins.completion import CompletionPlugin


class DummyFormatter(object):
    def format(self, partial, completions):
        return '[%s] %s' % (partial, ', '.join(sorted(completions)))


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManagerMock(
            (), (CompletionPlugin,),
            (), ((Config, dict), (KeyCmd, None))
        )
        self.uzbl = self.event_manager.add()

    def test_builtins(self):
        c = CompletionPlugin[self.uzbl]
        c.add_builtins('["spam", "egg"]')
        self.assertIn('spam', c.completion)
        self.assertIn('egg', c.completion)

    def test_config(self):
        c = CompletionPlugin[self.uzbl]
        c.add_config_key('spam', 'SPAM')
        self.assertIn('@spam', c.completion)


class TestCompletion(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManagerMock(
            (), (KeyCmd, CompletionPlugin),
            (), ((Config, dict),)
        )
        self.uzbl = self.event_manager.add()

        c = CompletionPlugin[self.uzbl]
        c.listformatter = DummyFormatter()
        c.add_builtins('["spam", "egg", "bar", "baz"]')
        c.add_config_key('spam', 'SPAM')
        c.add_config_key('Something', 'Else')

    def test_incomplete_keyword(self):
        k, c = KeyCmd[self.uzbl], CompletionPlugin[self.uzbl]
        k.keylet.keycmd = 'sp'
        k.keylet.cursor = len(k.keylet.keycmd)

        r = c.get_incomplete_keyword()
        self.assertEqual(r, 'sp')

    def test_incomplete_keyword_var(self):
        k, c = KeyCmd[self.uzbl], CompletionPlugin[self.uzbl]
        k.keylet.keycmd = 'set @sp'
        k.keylet.cursor = len(k.keylet.keycmd)

        r = c.get_incomplete_keyword()
        self.assertEqual(r, '@sp')

    def test_incomplete_keyword_var_noat(self):
        k, c = KeyCmd[self.uzbl], CompletionPlugin[self.uzbl]
        k.keylet.keycmd = 'set Some'
        k.keylet.cursor = len(k.keylet.keycmd)

        r = c.get_incomplete_keyword()
        self.assertEqual(r, '@Some')

    def test_stop_completion(self):
        config, c = Config[self.uzbl], CompletionPlugin[self.uzbl]
        c.completion.level = 99
        config['completion_list'] = 'test'

        c.stop_completion()
        self.assertNotIn('completion_list', config)
        self.assertEqual(c.completion.level, 0)

    def test_completion(self):
        k, c = KeyCmd[self.uzbl], CompletionPlugin[self.uzbl]
        config = Config[self.uzbl]

        comp = (
            ('sp', 'spam '),
            ('e', 'egg '),
            ('set @sp', 'set @spam '),
        )

        for i, o in comp:
            k.keylet.keycmd = i
            k.keylet.cursor = len(k.keylet.keycmd)

            c.start_completion()
            self.assertEqual(k.keylet.keycmd, o)
            c.start_completion()
            self.assertNotIn('completion_list', config)

    def test_completion_list(self):
        k, c = KeyCmd[self.uzbl], CompletionPlugin[self.uzbl]
        config = Config[self.uzbl]

        comp = (
            ('b', 'ba', '[ba] bar, baz'),
        )

        for i, o, l in comp:
            k.keylet.keycmd = i
            k.keylet.cursor = len(k.keylet.keycmd)

            c.start_completion()
            self.assertEqual(k.keylet.keycmd, o)
            c.start_completion()
            self.assertEqual(config['completion_list'], l)
