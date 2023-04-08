# WordPress Helper

## Installation
### Using pip
```angular2html
pip install git+https://github.com/cefege/WP-Helper/
```
or clone the repository
```angular2html
git clone https://github.com/cefege/WP-Helper/
```
## Usage
1. Import needed packages
```
from playwright.sync_api import sync_playwright
from WPHelper import WordPressHelper
```
2. Create browser and initiate WordPressHelper instance
```angular2html
with sync_playwright() as p:
    browser_ = p.chromium.launch()
    helper = WordPressHelper(browser_, args.domain, args.username, args.password)
```
4. Use the available functions
```
helper.delete_post(post_name)
helper.delete_page(page_name)
helper.install_plugin(plugin_name)
helper.delete_plugin(plugin_name)
helper.install_theme(theme_name)
helper.uncheck_submit_comments()
helper.delete_unused_theme()
helper.change_title_tagline(title, tagline)
helper.import_customization_file()
```

### refer to `main.py` for a complete example

* From command line

```angular2html
python main.py -d "DOMAIN" -u "USERNAME" -p "PASSWD" -t "TITLE" -a "TAGLINE"
```
