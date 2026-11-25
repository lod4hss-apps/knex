import os, logging
from dotenv import load_dotenv
from enum import IntEnum

class LogLevel(IntEnum):
    LLM = 21
    FEATURE = 22
    PIPELINE = 23


def prepare():

    load_dotenv()

    logging.addLevelName(LogLevel.LLM, "LLM")
    logging.addLevelName(LogLevel.FEATURE, "FEATURES")
    logging.addLevelName(LogLevel.PIPELINE, "PIPELINE")

    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
