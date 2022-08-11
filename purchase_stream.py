import faust

app = faust.App(
    'purchases',
    broker='kafka://localhost:9092'
)


class Purchase(faust.Record):
    user: str
    product: str


purchase_topic = app.topic('purchases', value_type=Purchase)
count_purchases = app.Table('count_purchases', default=int)
count_users = app.Table('count_users', default=int)


@app.agent(purchase_topic)
async def process(purchases):
    async for purchase in purchases.group_by(Purchase.product):
        count_purchases[purchase.product] += 1


@app.agent(purchase_topic)
async def users(purchases):
    async for purchase in purchases.group_by(Purchase.user):
        count_users[purchase.user] += 1
