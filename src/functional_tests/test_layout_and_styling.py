from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # エディスはホームページに行く
        self.browser.get(self.live_server_url)

        # 彼女のブラウザウィンドウは非常に特殊なサイズに設定されている
        self.browser.set_window_size(1024, 768)

        # 入力ボックスがきれいに中央に配置されていることに気づく
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )

        # 彼女は新しいリストを始め、そこでも入力がうまく中央に配置されているのを見る。
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )
