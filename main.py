# coding: utf-8
import sys

from modules.fulfill_inquiry import FulfillInquiry
from modules.menu import MainMenu


if __name__ == "__main__":
    mock = None
    # mock = [sys.argv[0], "-n", "3", "-l"]
    # mock = [sys.argv[0], "-n", "5", "-p", "месо, шунка", "-a", "мляко"]
    # mock = [sys.argv[0], "-n", "6", "-p", "яйца, ", "-a", "месо"]
    mock = [sys.argv[0], "-n", "12", "-d", "карофено пюре", "-a", "месо"]
    # mock = [sys.argv[0], "-n", "5", "-p", "месо, шунка", "-a", "Глутен,мляко", "-d", "палачинки"]  # raises
    # mock = [sys.argv[0], "-n", "5", "-l", "-p", "месо, шунка", "-a", "мляко"]
    # mock = [sys.argv[0], "-n", "5", "-p", "месо, шунка", "-a", "Глутен,мляко", "-d", "палачинки"]
    f = FulfillInquiry(mock_argv=mock, strict=False)
    menu = MainMenu(fulfilled_inquiry=f)
    menu.main_menu()
