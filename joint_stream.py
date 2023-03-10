import faust

app = faust.App(
    'joint_stream',
    broker='kafka://localhost:9092'
)


class Purchase(faust.Record):
    user: str
    product: str


purchase_topic = app.topic('purchases', value_type=Purchase)
product_counter = app.Table('count_purchases', default=int)
join_topic = app.topic('joint_purchases')


@app.agent(purchase_topic)
async def join(purchases):
    async for purchase in purchases:
        if purchase.product in product_counter.keys():
            await join_topic.send(
                value=f"user: {purchase.user}, product: {purchase.product}, amount: {product_counter[purchase.product]}")


@app.agent(purchase_topic)
async def process(purchases):
    async for purchase in purchases.group_by(Purchase.product):
        product_counter[purchase.product] += 1
