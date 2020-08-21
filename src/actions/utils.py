def load_context():
    import sys, os
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_path + '/../')
    