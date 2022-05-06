"""
記事モデル
"""
from app.models.abstract import AbstractModel


class EventModel(AbstractModel):
    def __init__(self, config):
        super(EventModel, self).__init__(config)

    def fetch_recent_events(self, user_id):
        """
        最新の記事を取得する．デフォルトでは最新5件まで
        :param limit: 取得する記事の数
        :return:
        """
        sql = "SELECT * FROM events WHERE user_id = %s ORDER BY created_at DESC"
        return self.fetch_all(sql, user_id)
        

    def create_events(self, user_id, title, body, start, end):
        """
        新しく記事を作成する
        :param user_id: 投稿したユーザのOD
        :param title: 記事のタイトル
        :param body: 記事の本文
        :return: None
        """
        sql = "INSERT INTO events(user_id, title, body, start, end) VALUE (%s, %s, %s, %s, %s);"
        self.execute(sql, user_id, title, body, start, end)

    # def create_events(self, user_id, title, body, dates, start, end):
    #     """
    #     新しく記事を作成する
    #     :param user_id: 投稿したユーザのOD
    #     :param title: 記事のタイトル
    #     :param body: 記事の本文
    #     :return: None
    #     """
    #     sql = "INSERT INTO events(user_id, title, body, dates, start, end) VALUE (%s, %s, %s, %s, %s, %s);"
    #     self.execute(sql, user_id, title, body, dates, start, end)

    # def change_events(self, user_id, title, body, dates, id):
    #     sql = "UPDATE events SET user_id=%s, title=%s, body=%s, dates=%s WHERE id = %s;"
    #     self.execute(sql, user_id, title, body, dates, id)
    
    def change_events(self, user_id, title, body, start, end, id):
        sql = "UPDATE events SET user_id=%s, title=%s, body=%s, start=%s, end=%s WHERE id = %s;"
        self.execute(sql, user_id, title, body, start, end, id)


    def delete_events(self, id):
        sql = "DELETE FROM events WHERE id = %s;"
        self.execute(sql, id)