#!/usr/bin/env PYTHONBREAKPOINT=breakword.breakpoint python3

# To run this program properly, the PYTHONBREAKPOINT environment
# variable must be set to breakword.breakpoint

if __name__ == "__main__":
    for i in range(5):
        breakpoint(i)
