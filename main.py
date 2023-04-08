import argparse

from playwright.sync_api import sync_playwright

from WPHelper import WordPressHelper

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="hoand.xyz", type=str, help="Blog Domain")
    parser.add_argument("-u", "--username", default="quizzical-bhabha", type=str, help="Account username")
    parser.add_argument("-p", "--password", default="GxUDmafJG3v2d7Azfn", type=str, help="Account Password")
    parser.add_argument("-t", "--title", default="TITLE_1", type=str, help="Blog Title")
    parser.add_argument("-a", "--tagline", default="TAGLINE_1", type=str, help="Blog Tagline")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser_ = p.chromium.launch()
        helper = WordPressHelper(browser_, args.domain, args.username, args.password)

        helper.delete_post("Hello World")

        helper.delete_page("Sample Page")
        helper.delete_page("Privacy Policy")
        helper.delete_page("Test Page1")

        helper.install_plugin("Customizer Export/Import")

        helper.delete_plugin("All-in-One WP Migration")

        helper.install_theme("Kadence")

        helper.uncheck_submit_comments()

        helper.delete_unused_theme()

        helper.change_title_tagline("Hello", "world")

        helper.import_customization_file()

        browser_.close()
