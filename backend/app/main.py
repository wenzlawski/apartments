import logging
import multiprocessing
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.scraper.scraper.spiders.quotes_spider import QuotesSpider
from app.utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Optionally: Schedule your job here with APScheduler
    if settings.ACTIVATE_SCHEDULER:
        logger.info("Starting BackgroundScheduler")
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(build_scraper, "interval", minutes=1, id="scraper_job")

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


def build_scraper():
    multiprocessing.set_start_method("spawn", force=True)

    process = multiprocessing.Process(target=run_scraper)
    process.start()
    process.join()
    logger.info("Scraper process joined")


def run_scraper():
    # Add the inner scraper project to path
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.log import configure_logging
    from scrapy.utils.project import get_project_settings
    from scrapy.utils.reactor import install_reactor

    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    settings = get_project_settings()

    runner = CrawlerProcess(settings)

    runner.crawl(QuotesSpider)
    logger.info("Scraper started")
    runner.start()
    logger.info("Scraper finished")
