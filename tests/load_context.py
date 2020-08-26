
def load_context():
    """
    Add the src dir to sys.path so we can 
    import code in the test folder as expected
    """
    import sys, os
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_path + '/../src')
