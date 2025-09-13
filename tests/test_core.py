import pytest
import sys
from io import StringIO
from easycli import CLI

def capture_output(func, args):
    sys.argv = ['test'] + args
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    func()
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return output

@pytest.fixture
def app():
    app = CLI("testapp")
    
    @app.command("greet")
    def greet(name: str, verbose: bool = False):
        if verbose:
            print("Verbose mode")
        print(f"Hello, {name}")
    
    user_group = app.group("user")
    
    @user_group.command("add")
    def add(username: str):
        print(f"Added {username}")
    
    return app

def test_simple_command(app):
    output = capture_output(app.run, ["greet", "Alice"])
    assert output == "Hello, Alice"

def test_flag(app):
    output = capture_output(app.run, ["greet", "Alice", "--verbose"])
    assert output == "Verbose mode\nHello, Alice"

def test_subcommand(app):
    output = capture_output(app.run, ["user", "add", "Bob"])
    assert output == "Added Bob"

def test_help(app):
    output = capture_output(app.run, ["--help"])
    assert "Commands:" in output
    assert "Groups:" in output

def test_invalid(app):
    output = capture_output(app.run, ["invalid"])
    assert "Error" in output