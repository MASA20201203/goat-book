from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
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

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # エディスは新しいToDoリストを作成する
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("孔雀の羽を買う")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 孔雀の羽を買う")

        # 彼女は自分のリストに固有のURLが生成されたことを確認する
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # 新しいユーザ、フランシスがサイトにアクセスする

        ## 真新しいユーザーセッションをシミュレートする方法として、ブラウザのクッキーをすべて削除する。
        self.browser.delete_all_cookies()

        # フランシスがアクセスし、エディスのリストの情報が見えないことを確認する
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("孔雀の羽を買う", page_text)
        self.assertNotIn("孔雀の羽を使ってハエを作る", page_text)

        # フランシスは新しい項目を入力することで、新しいリストを開始する。彼はエディスより面白くない...。
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("ミルクを買う")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: ミルクを買う")

        # フランシスは彼女のリストに固有のURLが生成されたことを確認する
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # エディスのリストにはフランシスのリストの情報が表示されないことを確認する
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("孔雀の羽を買う", page_text)
        self.assertIn("ミルクを買う", page_text)

        # 二人は満足して眠りにつく
