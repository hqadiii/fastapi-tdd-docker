import nltk
from newspaper import Article

from app.models.tortoise import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    await TextSummary.filter(id=summary_id).update(summary=article.summary)
