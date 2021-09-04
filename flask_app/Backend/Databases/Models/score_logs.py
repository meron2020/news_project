from flask_app.Backend.Databases.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator


class ScoreLogsModel:
    def __init__(self):
        self.handler = DatabaseHandlerOrchestrator()

    def get_url_to_url_score(self, path):
        url_to_url_score = []
        article_dict = self.handler.get_all_rows_for_graph(path)
        for score_row in self.handler.get_all_rows_from_scores(path):
            first_url = article_dict[score_row[0]][1]
            second_url = article_dict[score_row[1]][1]
            first_title = article_dict[score_row[0]][5]
            second_title = article_dict[score_row[1]][5]
            score_dict = {"first_url": first_url, "second_url": second_url, "first_title": first_title,
                          "second_title": second_title, "title_score": score_row[4], "text_score": score_row[5],
                          "score": score_row[6]}
            url_to_url_score.append(score_dict)
        return url_to_url_score

    def select_url_to_url_score(self):
        url_to_url_score = self.get_url_to_url_score(r"..\news_texts.db")
        return url_to_url_score
