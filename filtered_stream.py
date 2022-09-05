import faust

app = faust.App(
    'filtered_stream',
    broker='kafka://localhost:9092'
)


class Purchase(faust.Record):
    user: str
    product: str


purchase_topic = app.topic('purchases', value_type=Purchase)
filtered_topic = app.topic('filtered_purchases')


def filter_products(purchase):
    if purchase.product in ['book', 'batteries']:
        return purchase


@app.agent(purchase_topic)
async def process(purchases):
    async for purchase in purchases.filter(filter_products):
        await filtered_topic.send(value=purchase)