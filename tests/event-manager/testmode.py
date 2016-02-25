#!/usr/bin/env python
# vi: set et ts=4:



import unittest
from emtest import EventManagerMock
from uzbl.plugins.config import Config
from uzbl.plugins.mode import ModePlugin
from uzbl.plugins.on_set import OnSetPlugin

class ModeParseTest(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManagerMock(
            (), (OnSetPlugin, ModePlugin),
            (), ((Config, dict),)
        )
        self.uzbl = self.event_manager.add()

    def test_parse_config(self):
        uzbl = self.uzbl
        m = ModePlugin[uzbl]

        mode, key, value = 'foo', 'x', 'y'
        m.parse_mode_config((mode, key, value))
        self.assertIn(mode, m.mode_config)
        self.assertIn(key, m.mode_config[mode])
        self.assertEqual(m.mode_config[mode][key], value)


class ModeTest(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManagerMock(
            (), (OnSetPlugin, ModePlugin),
            (), ((Config, dict),)
        )
        self.uzbl = self.event_manager.add()

        mode = ModePlugin[self.uzbl]
        config = Config[self.uzbl]

        mode.parse_mode_config(('mode0', 'foo', 'default'))

        mode.parse_mode_config(('mode1', 'foo', 'xxx'))
        mode.parse_mode_config('mode1 bar "spam spam"')
        mode.parse_mode_config('mode1 baz foo="baz"')

        mode.parse_mode_config(('mode2', 'foo', 'XXX'))
        mode.parse_mode_config(('mode2', 'spam', 'spam'))

        config['default_mode'] = 'mode0'
        mode.default_mode_updated(None, 'mode0')

    def test_mode_sets_vars(self):
        mode, config = ModePlugin[self.uzbl], Config[self.uzbl]
        mode.mode_updated(None, 'mode1')

        self.assertIn('foo', config)
        self.assertIn('bar', config)
        self.assertIn('baz', config)
        self.assertEqual(config['foo'], 'xxx')
        self.assertEqual(config['bar'], 'spam spam')
        self.assertEqual(config['baz'], 'foo="baz"')

    def test_mode_overwrite_vars(self):
        mode, config = ModePlugin[self.uzbl], Config[self.uzbl]
        config['mode'] = 'mode1'
        mode.mode_updated(None, 'mode1')
        config['mode'] = 'mode2'
        mode.mode_updated(None, 'mode2')

        self.assertIn('foo', config)
        self.assertIn('bar', config)
        self.assertIn('baz', config)
        self.assertIn('spam', config)
        self.assertEqual(config['foo'], 'XXX')
        self.assertEqual(config['bar'], 'spam spam')
        self.assertEqual(config['baz'], 'foo="baz"')
        self.assertEqual(config['spam'], 'spam')

    def test_default_mode(self):
        ''' Setting to mode to nothing should enter the default mode'''
        mode, config = ModePlugin[self.uzbl], Config[self.uzbl]

        config['foo'] = 'nthth'
        config['mode'] = ''
        mode.mode_updated(None, '')
        self.assertEqual(config['mode'], 'mode0')
        mode.mode_updated(None, config['mode'])
        self.assertEqual(config['mode'], 'mode0')
        self.assertEqual(config['foo'], 'default')
