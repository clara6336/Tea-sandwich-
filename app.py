#!/usr/bin/env python3
"""Hello world app that fetches a 3-digit prime from an Alpine container."""

from __future__ import annotations

import subprocess
import sys


def get_prime_from_alpine() -> int:
    """Run a short Python program inside an Alpine container and return its prime output."""
    container_python = r'''
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

for candidate in range(100, 1000):
    if is_prime(candidate):
        print(candidate)
        break
'''

    command = [
        "docker",
        "run",
        "--rm",
        "alpine",
        "sh",
        "-c",
        "apk add --no-cache python3 >/dev/null && python3 -c \"$PYCODE\"",
    ]

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        env={"PYCODE": container_python},
    )

    prime_text = result.stdout.strip()
    if not prime_text.isdigit() or len(prime_text) != 3:
        raise ValueError(f"Unexpected output from container: {prime_text!r}")

    return int(prime_text)


def main() -> None:
    print("Hello, world!")
    prime = get_prime_from_alpine()
    print(f"3-digit prime from Alpine container: {prime}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("Docker is not installed or not on PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.strip() or str(exc), file=sys.stderr)
        sys.exit(exc.returncode or 1)
