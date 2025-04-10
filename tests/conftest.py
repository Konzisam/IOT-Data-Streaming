import sys
import os

# Add the root directory (the parent of 'jobs' and 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jobs')))
# print(sys.path)