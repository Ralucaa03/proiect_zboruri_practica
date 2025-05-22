#from playwright.sync_api import sync_playwright

#with sync_playwright() as p:
   # browser = p.chromium.launch(headless=False)
   # page = browser.new_page()
   # page.goto('https://www.google.com/')
   # print('Chrome successfully opened')
   # print(page.title())  # Now it's safely within the context
   # page.wait_for_timeout(3000)
   # browser.close()


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')

    # Wait and fill in username
    page.wait_for_selector('input[name="username"]').fill('Admin')

    # Wait and fill in password
    page.wait_for_selector('input[type="password"]').fill('admin123')

    # Wait and click login button
    page.wait_for_selector('button[type="submit"]').click()

    page.wait_for_timeout(5000)  # optional: see the result
    browser.close()



from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')

    # Login folosind XPath (relative)
    username_element = page.wait_for_selector('//input[@name="username"]')
    username_element.type('Admin')

    password_element = page.wait_for_selector('//input[@placeholder="Password"]')
    password_element.type('admin123')

    login_element = page.wait_for_selector('//button[@type="submit"]')
    login_element.click()

    # Așteaptă 3 secunde pentru încărcare completă după login
    page.wait_for_timeout(3000)

    # XPath: element text exact
    page.wait_for_selector('//p[text()="Forgot your password? "]')

    # XPath: folosind contains pe atribut
    page.wait_for_selector('//input[contains(@placeholder, "User")]')

    # XPath: folosind contains pe text
    page.wait_for_selector('//p[contains(text(),"Forgot you")]')

    # XPath: label care conține textul "Username"
    page.wait_for_selector('//label[contains(text(),"Username")]')
