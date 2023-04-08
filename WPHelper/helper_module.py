class WordPressHelper:
    """ Class that automates WordPress cleaning """

    def __init__(self, browser, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password
        self.page = browser.new_page()
        # Accept any popup messages
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.__login()

    def __login(self):
        self.page.goto(f"https://{self.domain}/wp-login.php")
        # Fill username and password
        self.page.fill('#user_login', self.username)
        self.page.fill('#user_pass', self.password)
        # press submit button
        self.page.click('#wp-submit')
        # Check if logged successfully
        if self.page.url == f"https://{self.domain}/wp-admin/":
            print(f"[Log In] Logged In")
        else:
            print("Please Enter a Valid Username/Password")
            exit()

    def delete_post(self, post_name):
        # names used in the URL
        encoded_name = post_name.replace(' ', '+')
        self.page.goto(f"https://{self.domain}/wp-admin/edit.php?s={encoded_name}&post_status=all&post_type=post")
        # List table rows
        table_rows = self.page.locator('#the-list').locator("tr")
        # Check if post exist
        if table_rows.nth(0).locator("input").count() > 0:
            print(f"[{post_name} Post] Moving To Trash...")
            # Select first post
            table_rows.nth(0).locator("input").check()
            # select trash from item menu
            self.page.select_option('#bulk-action-selector-top', 'trash')
            # move to trash
            self.page.click('#doaction')
            # go to the trash
            self.page.goto(f"https://{self.domain}/wp-admin/edit.php?post_status=trash&post_type=post")
            # select first item in the list
            self.page.locator('#the-list').locator("tr").nth(0).locator("input").check()
            # select delete option
            self.page.select_option('#bulk-action-selector-top', 'delete')
            # press delete button
            self.page.click('#doaction')
            print(f"[{post_name} Post] Deleted Successfully.")
        else:
            print(f"[{post_name} Post] Post Doesn't Exist")

    def delete_page(self, page_name):
        # names used in the URL
        encoded_name = page_name.replace(" ", "+")
        self.page.goto(f"https://{self.domain}/wp-admin/edit.php?s={encoded_name}&post_status=all&post_type=page")
        # Check if page exist
        if self.page.locator('#the-list').locator("tr").nth(0).locator("input").count() > 0:
            print(f"[{page_name} Page] Moving To Trash...")
            # select first page
            self.page.locator('#the-list').locator("tr").nth(0).locator("input").check()
            # select trash from menu
            self.page.select_option('#bulk-action-selector-top', 'trash')
            # press apply button
            self.page.click('#doaction')
            # go to the trash
            self.page.goto(f"https://{self.domain}/wp-admin/edit.php?post_status=trash&post_type=page")
            # select first element
            self.page.locator('#the-list').locator("tr").nth(0).locator("input").check()
            # select delete option
            self.page.select_option('#bulk-action-selector-top', 'delete')
            # press delete button
            self.page.click('#doaction')
            print(f"[{page_name} Page] Deleted Successfully.")
        else:
            print(f"[{page_name} Page] Page Doesn't Exist")

    def install_plugin(self, plugin_name):
        # names used in the URL
        encoded_name = plugin_name.replace(" ", "+")
        print(f"[{plugin_name} Plugin] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/plugin-install.php?s={encoded_name}&tab=search&type=term")
        # get all plugins from the page
        plugin_cards = self.page.locator("[class*='plugin-card plugin-card-']")
        if plugin_cards.count():
            # if plugin exist, check if the first plugin has an Active button
            active_buttons = plugin_cards.nth(0).locator('[class="button activate-now"]')
            if active_buttons.count():
                # if Active button existed, Click it.
                active_buttons.nth(0).click()
                print(f"[{plugin_name} Plugin] Installed Successfully.")
            else:
                print(f"[{plugin_name} Plugin] Already Installed.")

        else:
            print(f"[{plugin_name} Plugin] Plugin Doesn't Exist.")

    def delete_plugin(self, plugin_name):
        print(f"[{plugin_name}] Deleting...")
        self.page.goto(f"https://{self.domain}/wp-admin/plugins.php?plugin_status=all&paged=1&s")
        # List table rows
        table_rows = self.page.locator('#the-list').locator("tr")
        # Check if there are existing items
        if table_rows.count():
            found = False
            for row_idx in range(table_rows.count()):
                # get the first column which contains plugin name
                first_column = table_rows.nth(row_idx).locator("td").nth(0)
                # get the plugin name
                p_name = first_column.locator("strong").inner_text()
                # Check if the plugin name matches the input plugin name
                if p_name == plugin_name:
                    # Deactivate plugin if activated
                    if first_column.locator('[class="deactivate"]').count():
                        first_column.locator('[class="deactivate"]').locator("a").click()
                        print(f"[{plugin_name}] Deactivated.")

                    # Uninstall the plugin
                    found = True
                    first_column.locator('[class="delete"]').locator("a").click()
                    print(f"[{plugin_name}] Deleted Successfully.")
                    break

            if not found:
                print(f"[{plugin_name}] Plugin Doesn't exist.")
        else:
            print(f"[{plugin_name}] Plugin Doesn't exist.")

    def install_theme(self, theme_name):
        # names used in the URL
        encoded_name = theme_name.replace(" ", "+")
        print(f"[{theme_name} Theme] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/theme-install.php?search={encoded_name}")
        print(f"[{theme_name} Theme] Installing...")
        # list all available themes
        theme_carts = self.page.locator('[class="theme"]')
        if theme_carts.count():
            # Install theme if it exists
            theme_carts.nth(0).locator('[class="button button-primary theme-install"]').click()
            print(f"[{theme_name} Theme] Installed Successfully.")
        else:
            print(f"[{theme_name} Theme] Theme Doesn't Exist.")

    def uncheck_submit_comments(self, ):
        print(f"[Uncheck Submit Comments] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/options-discussion.php")
        # Uncheck the check-box besides submit_comments
        self.page.uncheck('#default_comment_status')
        # press submit button
        self.page.click('#submit')
        print(f"[Uncheck Submit Comments] Unchecked Successfully.")

    def delete_unused_theme(self):
        print(f"[Delete Unused Theme] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/themes.php")
        # Search of the unactivated themes
        theme_carts = self.page.locator('[class="theme"]')
        while theme_carts.count():
            # get the theme name
            t_name = theme_carts.nth(0).locator('h2').inner_text()
            # click on the theme
            theme_carts.nth(0).locator('button').click()
            # click the delete button
            self.page.locator('[class="button delete-theme"]').nth(0).click()
            print(f"[Delete Unused Theme] Theme {t_name} Deleted Successfully.")
            # Reload the theme pages (to list the remaining themes)
            self.page.goto(f"https://{self.domain}/wp-admin/themes.php")
            self.page.reload()
            theme_carts = self.page.locator('[class="theme"]')

    def change_title_tagline(self, title, tageline):
        print(f"[Change Title and Tagline] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/options-general.php")
        # Fill the title and tagline text boxes
        self.page.fill('#blogname', title)
        self.page.fill('#blogdescription', tageline)
        self.page.click('#submit')
        print(f"[Change Title and Tagline] Changed Successfully.")

    def import_customization_file(self):
        print(f"[Import Customization Block] Navigating...")
        self.page.goto(f"https://{self.domain}/wp-admin/customize.php?return="
                       f"%2Fwp-admin%2Fplugin-install.php%3Fs%3DKadence%2BBlocks%26tab%3Dsearch%26type%3Dterm")

        # Click Export/Import section
        self.page.locator('[id="accordion-section-cei-section"]').nth(0).click()
        self.page.wait_for_timeout(1)

        # check if file-input exists
        file_inputs = self.page.locator('[name="cei-import-file"]')
        if file_inputs.count():
            # Upload file to the fileinput field
            file_inputs.nth(0).set_input_files('./kadence-export.dat')
            # press upload button
            self.page.locator('[name="cei-import-button"]').click()

        print(f"[Import Customization Block] Imported Successfully.")
