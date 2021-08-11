from sqlalchemy import Column, String,Integer
from linebot.models import  *
from database import Base,db_session
from urllib.parse import quote

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    product_image_url = Column(String)

    @staticmethod
    def list_all():
        products=db_session.query(Products).all()

        bubbles=[]

        for product in products:
            bubble = BubbleContainer(
                hero=ImageComponent(
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
                    url=product.product_image_url
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=product.name,wrap=True,
                                      weight='bold',size='xl'),
                        BoxComponent(
                            layout='baseline',
                            contents=[
                                TextComponent(text='NT${price}'.format(price=product.price),wrap=True,
                                      weight='bold',size='xl')
                            ]
                        ),
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            style='primary',
                            color='#1DB446',
                            action=URIAction(label='加入',
                                             uri='line://oaMessage/{base_id}/?{message}'.format(base_id='@816ekxou',
                                                                                                message=quote("{product},我想要幾個:".format(product=product.name)))
                                             ),
                        )
                    ]
                )
            )
            bubbles.append(bubble)

        carousel_container=CarouselContainer(contents=bubbles)
        message = FlexSendMessage(alt_text='products',contents=carousel_container)
        return message