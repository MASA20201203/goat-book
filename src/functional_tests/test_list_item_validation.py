from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # エディスはホームページに行き、誤って空のリスト項目を送信しようとした。
        # 彼女は空の入力ボックスでEnterを押した
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # ブラウザはリクエストをインターセプトし、リストページをロードしない。
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # 彼女は新しいアイテムのためにテキストを入力し始め、エラーは消えます。
        self.get_item_input_box().send_keys("ミルクを買う")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )

        # 項目にテキストを追加して再試行すると、うまくいった
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: ミルクを買う")

        # ひょんなことから、彼女は2つ目の空白のリスト項目を投稿することにした。
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 再び、ブラウザは応じない
        self.wait_for_row_in_list_table("1: ミルクを買う")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # そして、彼女はテキストを入力することで満足させることができる。
        self.get_item_input_box().send_keys("紅茶を作る")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: ミルクを買う")
        self.wait_for_row_in_list_table("2: 紅茶を作る")
