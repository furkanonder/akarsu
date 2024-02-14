import sys
import textwrap
import unittest

from akarsu.akarsu import Akarsu

# Set encoding to UTF-8 when testing on windows-latest
if sys.platform == "win32":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


class TestNine(unittest.TestCase):
    def check_events(self, events, expected_events):
        for event, expected_event in zip(events, expected_events):
            with self.subTest(event=event, expected_event=expected_event):
                self.assertEqual(event, expected_event)

    def test_profile_print(self):
        code = "print('Hello, world!')"
        events = Akarsu(code, "<string>").profile()
        expected_events = [("C_CALL", "<string>", "<built-in function print>")]
        self.check_events(events, expected_events)

    def test_profile_isinstance(self):
        code = "isinstance(1, int)"
        events = Akarsu(code, "<string>").profile()
        expected_events = [("C_CALL", "<string>", "<built-in function isinstance>")]
        self.check_events(events, expected_events)

    def test_profile_generator(self):
        code = "list(i for i in range(5))"
        events = Akarsu(code, "<string>").profile()
        expected_events = [
            ("C_CALL", "<string>", "<class 'range'>"),
            ("PY_CALL", "<string>", "<genexpr>"),
            ("C_CALL", "<string>", "<class 'list'>"),
            ("PY_START", "<string>", "<genexpr>"),
            ("YIELD", "<string>", "<genexpr>"),
            ("RESUME", "<string>", "<genexpr>"),
            ("YIELD", "<string>", "<genexpr>"),
            ("RESUME", "<string>", "<genexpr>"),
            ("YIELD", "<string>", "<genexpr>"),
            ("RESUME", "<string>", "<genexpr>"),
            ("YIELD", "<string>", "<genexpr>"),
            ("RESUME", "<string>", "<genexpr>"),
            ("YIELD", "<string>", "<genexpr>"),
            ("RESUME", "<string>", "<genexpr>"),
            ("PY_RETURN", "<string>", "<genexpr>"),
        ]
        self.check_events(events, expected_events)

    def test_profile_nested_functions(self):
        source = textwrap.dedent("""
            def foo():
                print("Hello, world!")
            def bar():
                foo()
            bar()
            """)
        events = Akarsu(source, "<string>").profile()
        expected_events = [
            ("PY_CALL", "<string>", "bar"),
            ("PY_START", "<string>", "bar"),
            ("PY_CALL", "<string>", "foo"),
            ("PY_START", "<string>", "foo"),
            ("C_CALL", "<string>", "<built-in function print>"),
            ("C_RETURN", "<string>", "foo"),
            ("PY_RETURN", "<string>", "foo"),
            ("PY_RETURN", "<string>", "bar"),
        ]
        self.check_events(events, expected_events)

    def test_profile_class(self):
        source = textwrap.dedent("""
            class C:
                def foo(self):
                    x = 1
            c = C()
            c.foo()
            """)
        events = Akarsu(source, "<string>").profile()
        expected_events = [
            ("C_CALL", "<string>", "<built-in function __build_class__>"),
            ("PY_START", "<string>", "C"),
            ("PY_RETURN", "<string>", "C"),
            ("PY_CALL", "<string>", "foo"),
            ("PY_START", "<string>", "foo"),
            ("PY_RETURN", "<string>", "foo"),
        ]
        self.check_events(events, expected_events)

    def test_profile_class_method(self):
        source = textwrap.dedent("""
            class MyClass:
                @classmethod
                def foo(cls):
                    print("Hello, world!")
            my_class = MyClass()
            my_class.foo()
            """)
        events = Akarsu(source, "<string>").profile()
        expected_events = [
            ("C_CALL", "<string>", "<built-in function __build_class__>"),
            ("PY_START", "<string>", "MyClass"),
            ("C_CALL", "<string>", "<class 'classmethod'>"),
            ("C_RETURN", "<string>", "MyClass"),
            ("PY_RETURN", "<string>", "MyClass"),
            ("PY_CALL", "<string>", "foo"),
            ("PY_START", "<string>", "foo"),
            ("C_CALL", "<string>", "<built-in function print>"),
            ("C_RETURN", "<string>", "foo"),
            ("PY_RETURN", "<string>", "foo"),
        ]
        self.check_events(events, expected_events)
