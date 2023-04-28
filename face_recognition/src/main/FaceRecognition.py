import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from GUI.HomeGUI import HomeGUI

def main():
    # LoginGUI()
    HomeGUI()

