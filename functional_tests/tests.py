from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        # エディスは、クールな新しいオンラインToDoアプリについて聞いた。
        # 彼女はそのホームページをチェックしに行く
        self.browser.get(self.live_server_url)

        # 彼女はページのタイトルとヘッダーがToDoリストについて言及していることに気づく
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # すぐにToDoを入力するよう促される
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # 彼女はテキストボックスに「孔雀の羽を買う」と入力する
        # (エディスの趣味はフライフィッシングのルアーを結ぶこと)
        inputbox.send_keys("孔雀の羽を買う")

        # 彼女がエンターキーを押すと、ページが更新され、次のように表示される。
        # 「1: クジャクの羽を買う」 がToDoリストの項目としてリストアップされる
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 孔雀の羽を買う")

        # 別の項目を追加するよう促すテキストボックスが残っている。
        # 彼女は「孔雀の羽を使ってハエを作る」と入力した。
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("孔雀の羽を使ってハエを作る")
        inputbox.send_keys(Keys.ENTER)

        # ページが再び更新され、リストの両方の項目が表示される。
        self.wait_for_row_in_list_table("1: 孔雀の羽を買う")
        self.wait_for_row_in_list_table("2: 孔雀の羽を使ってハエを作る")

        # 満足した彼女は眠りにつく
