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

        # ホームページがリフレッシュされ、エラーメッセージが表示された。
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        # 項目にテキストを追加して再試行すると、うまくいった
        self.get_item_input_box().send_keys("ミルクを買う")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: ミルクを買う")

        # ひょんなことから、彼女は2つ目の空白のリスト項目を投稿することにした。
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 同じような警告がリストページに表示される
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        # テキストを入力することで修正できる
        self.get_item_input_box().send_keys("紅茶を作る")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: ミルクを買う")
        self.wait_for_row_in_list_table("2: 紅茶を作る")
