import sys
import logging
from rest_framework import routers

logger = logging.getLogger(__name__)

# extjs can't put with a trailing slash
router = routers.DefaultRouter(trailing_slash=False)
