from apscheduler.schedulers.background import BackgroundScheduler
from .products.schemas import SearchQuery
from .products.core import ProductScrapping

scheduler = BackgroundScheduler()

scheduler.add_job(ProductScrapping().get_products, 'interval', [SearchQuery(pages=1, proxy="")], seconds=3)