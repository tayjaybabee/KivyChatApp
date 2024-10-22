# *******************************************
#  Copyright (c) 2024. Inspyre Softworks    *
# *******************************************
from inspy_logger import InspyLogger, Loggable


ROOT_LOGGER = InspyLogger('InspyChatClient', console_level='debug', no_file_logging=True)


__all__ = ['ROOT_LOGGER', 'Loggable']
