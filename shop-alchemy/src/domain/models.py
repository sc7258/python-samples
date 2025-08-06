import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# N:M 관계를 위한 연결 테이블
item_category = Table(
    'item_category',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('item.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    orders = relationship("Order", back_populates="member")

    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    items = relationship("Item", secondary=item_category, back_populates="categories")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    item_type = Column(String(50), nullable=False)

    categories = relationship("Category", secondary=item_category, back_populates="items")
    order_items = relationship("OrderItem", back_populates="item")

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': item_type
    }

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price})>"

    def remove_stock(self, quantity: int):
        """재고를 감소시킵니다."""
        if self.stock_quantity < quantity:
            raise ValueError("재고가 부족합니다.")
        self.stock_quantity -= quantity

class Book(Item):
    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }
    author = Column(String(50))
    isbn = Column(String(20))

    def __repr__(self):
        return f"<Book(id={self.id}, name='{self.name}', author='{self.author}')>"

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    status = Column(String(20), nullable=False, default='ORDERED')

    member = relationship("Member", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, member_id={self.member_id}, status='{self.status}')>"

    @staticmethod
    def create_order(member: Member, order_items_info: list[dict]):
        """주문 생성 로직"""
        order = Order(member=member)
        for item_info in order_items_info:
            item = item_info['item']
            count = item_info['count']
            item.remove_stock(count)
            order_item = OrderItem(
                item=item,
                order_price=item.price,
                count=count
            )
            order.order_items.append(order_item)
        return order

class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    order_price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, item_id={self.item_id}, count={self.count})>"
