from celery import Celery

celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

celery_app.conf.task_routes = {
    'app.tasks.*': {'queue': 'main-queue'}
}

@celery_app.task
def send_order_confirmation(order_id: str):
     # Implement order confirmation email logic
     pass

@celery_app.task
def generate_invoice(order_id: str):
    # Implement invoice generation logic
    pass