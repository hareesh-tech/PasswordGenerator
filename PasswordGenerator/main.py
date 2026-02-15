import logging
import os
from pathlib import Path

Path("Output").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Output/pass_fort.log', mode='a')
    ],
    force=True
)

logger = logging.getLogger(__name__)

os.environ['KIVY_NO_CONSOLELOG'] = '1'

from app import PassFortApp

if __name__ == '__main__':

    logger.info("="*80)
    logger.info("PassFort Application Started")
    logger.info("="*80)

    try:
        PassFortApp().run()
    except Exception as e:
        logger.error(f"Application crashed: {e}", exc_info=True)
    finally:
        logger.info("="*80)
        logger.info("PassFort Application Closed")
        logger.info("="*80)