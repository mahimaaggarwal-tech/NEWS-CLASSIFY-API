from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class NewsItem(Base):
    __tablename__ = 'news_items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    link = Column(String)
    category = Column(String)
    pub_date = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "category": self.category,
            "pub_date": self.pub_date.isoformat() if self.pub_date else None
        }
