import unittest
from selenium import webdriver


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

        # すぐにToDoを入力するよう促される
        self.fail("Finish the test!")

        # 彼女はテキストボックスに「孔雀の羽を買う」と入力する
        # (エディスの趣味はフライフィッシングのルアーを結ぶこと)

        # 彼女がエンターキーを押すと、ページが更新され、次のように表示される。
        # 「1: クジャクの羽を買う」 がToDoリストの項目としてリストアップされる

        # 別の項目を追加するよう促すテキストボックスが残っている。
        # 彼女は 「孔雀の羽を使ってハエを作る 」と入力した。

        # ページが再び更新され、リストの両方の項目が表示される。

        # 満足した彼女は眠りにつく


if __name__ == "__main__":
    unittest.main()
