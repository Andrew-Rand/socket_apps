import asyncio
from asyncio import Queue, QueueShutDown
from random import randrange


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    while not queue.empty():  # get the customer if queue is not empty
        customer: Customer = queue.get_nowait()  # return immediately or raise error
        # use get and programm will be wait until new elemment in queue (see queue_in_web_application.py example)

        print(f'Cashier #{cashier_number} work with customer {customer.customer_id}')

        for product in customer.products:
            print(f'Cashier #{cashier_number} checkout {product.name}')
            await asyncio.sleep(product.checkout_time)

        print(f'Cashier #{cashier_number} work with customer {customer.customer_id} complete')

        queue.task_done()  # signal that all task is finished (task_done) (not queue is empty)

async def main():
    customer_queue = Queue()
    all_products = [
        Product(name='Beer', checkout_time=5),
        Product(name='Vegetables', checkout_time=2),
        Product(name='Milk', checkout_time=3),
        Product(name='Snacks', checkout_time=1),
    ]

    for i in range(10):  # create 10 customer with random products
        products = [all_products[randrange(len(all_products))] for _ in range(randrange(10))]
        customer_queue.put_nowait((Customer(customer_id=i, products=products)))  # add to queue immediately, if no free slot - raise
        # use put if queue is limited, if full it will be wait until free slot (see queue_in_web_application.py example)

    # create 3 cashiers
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i)) for i in range(3)]

    await asyncio.gather(customer_queue.join(), *cashiers)  # join() await the code until all queue is not finished

asyncio.run(main())