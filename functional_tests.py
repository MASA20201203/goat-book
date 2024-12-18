from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # エディスは、クールな新しいオンラインToDoアプリについて聞いた。
        # 彼女はそのホームページをチェックしに行く
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(
            any(row.text == "1: 孔雀の羽を買う" for row in rows),
            "新しいToDo項目がテーブルに表示されませんでした",
        )

        # 別の項目を追加するよう促すテキストボックスが残っている。
        # 彼女は 「孔雀の羽を使ってハエを作る 」と入力した。
        self.fail("Finish the test!")

        # ページが再び更新され、リストの両方の項目が表示される。

        # 満足した彼女は眠りにつく


if __name__ == "__main__":
    unittest.main()
