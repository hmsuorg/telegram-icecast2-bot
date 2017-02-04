import os
import importlib as imp
import inspect

from telegram.ext import CommandHandler

from api.interfaces import CommandHandlerAPI


class CommandsLoader:

    """CommandsLoader"""

    def __init__(self):

        self.ignore_list = [
            'CommandHandlerAPI'
        ]


    def __module_load(self, load):

        """
        __module_load

        :param load
        """

        selected = []

        for klass in dir(load):

            if inspect.isclass(getattr(load, klass)):

                test_klass = getattr(load, klass)

                if test_klass.__name__ in self.ignore_list:
                    continue

                if issubclass(test_klass, CommandHandlerAPI):
                    selected.append(test_klass)

        return selected

    def __callback_load(self, klasses, dispatcher):

        """
        __callback_load

        :param klasses
        :param dispatcher
        """

        for klass in klasses:
            klass = klass()

            for callback in dir(klass):

                if callback.endswith('_tcb'):

                    dispatcher.add_handler(CommandHandler(
                        callback.replace('_tcb', ''),
                        getattr(klass, callback),
                        pass_args=True
                    ))


    def load(self, dispatcher):

        """
        dispatch

        :param bot
        :param dispatcher
        """

        for root, _, files in os.walk('api'):

            for module in files:
                root = root.replace('/', '.')

                if module == '__init__.py':

                    try:
                        load = imp.import_module(root)

                    except ImportError:
                        pass

                    else:

                        self.__callback_load(self.__module_load(load), dispatcher)

