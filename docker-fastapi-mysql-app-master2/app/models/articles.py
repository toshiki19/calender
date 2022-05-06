"""
記事モデル
"""
from app.models.abstract import AbstractModel


class ArticleModel(AbstractModel):
    def __init__(self, config):
        super(ArticleModel, self).__init__(config)

    def fetch_recent_articles(self, limit=10):
        """
        最新の記事を取得する．デフォルトでは最新5件まで
        :param limit: 取得する記事の数
        :return:
        """
        sql = "SELECT * FROM articles ORDER BY created_at DESC LIMIT %s"
        return self.fetch_all(sql, limit)

    def fetch_article_by_id(self, article_id):
        """
        指定されたIDの記事を取得
        :param article_id: 取得したい記事のID
        :return: 指定された記事のID
        """
        sql = "SELECT * FROM articles INNER JOIN users u on articles.user_id = u.id WHERE articles.id=%s"
        return self.fetch_one(sql, article_id)

    def fetch_article_by_id_all(self, user_id):
      
        sql = "SELECT * FROM articles WHERE user_id=%s ORDER BY created_at DESC"
        return self.fetch_all(sql, user_id)

    def create_article(self, user_id, title, body, start, end):
        """
        新しく記事を作成する
        :param user_id: 投稿したユーザのOD
        :param title: 記事のタイトル
        :param body: 記事の本文
        :return: None
        """
        sql = "INSERT INTO articles(user_id, title, body, start, end) VALUE (%s, %s, %s, %s, %s);"
        self.execute(sql, user_id, title, body, start, end)

    # def create_evants(self, user_id, title, body, start, end):
    #     """
    #     新しく記事を作成する
    #     :param user_id: 投稿したユーザのOD
    #     :param title: 記事のタイトル
    #     :param body: 記事の本文
    #     :return: None
    #     """
    #     sql = "INSERT INTO articles(user_id, title, body, start, end) VALUE (%s, %s, %s, %s, %s);"
    #     self.execute(sql, user_id, title, body, start, end)

    # def change_article(user_id, self, title, body, dates):
        
    #     sql = "UPDATE articles(user_id, title, body, dates) VALUE (%s, %s, %s, %s);"
    #     self.execute(sql, user_id, title, body, dates)

    def change_article(self, user_id, title, body, start, end, id):
        sql = "UPDATE articles SET user_id=%s, title=%s, body=%s, start=%s, end=%s WHERE id = %s;"
        self.execute(sql, user_id, title, body, start, end, id)

    # def delete_article(user_id, self, title, body, dates):
    #     sql = "DETELE articles(user_id, title, body, dates) VALUE (%s, %s, %s, %s);"
    #     self.execute(sql, user_id, title, body, dates)

    def delete_article(self, id):
        sql = "DELETE FROM articles WHERE id = %s;"
        self.execute(sql, id)