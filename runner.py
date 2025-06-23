# runner.py
import sys
import io
import traceback

def run_code(code: str, user_input: str = ""):
    stdout = io.StringIO()
    stderr = io.StringIO()
    stdin = io.StringIO(user_input)
    exec_globals = {}

    try:
        sys.stdout = stdout
        sys.stderr = stderr
        sys.stdin = stdin

        exec(code, exec_globals)  # Only use exec for full code execution
    except Exception:
        traceback.print_exc(file=stderr)
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdin = sys.__stdin__

    return {
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue()
    }
