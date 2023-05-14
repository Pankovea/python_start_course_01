class BotHandlers():
    def __init__(self):
        self.callback_query_handlers = list()
        self.message_handlers = list()
    
    @staticmethod
    def _build_handler_dict(handler, pass_bot=False, **filters):
        return {
            'function': handler,
            'pass_bot': pass_bot,
            'filters': {ftype: fvalue for ftype, fvalue in filters.items() if fvalue is not None}
        }

    def callback_query_handler(self, func = None, **kwargs):
        if func is None:
            func = lambda _: True
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, **kwargs)
            self.callback_query_handlers.append(handler_dict)
            return handler
        return decorator
    
    def message_handler(self, commands=None, regexp=None, func=None, content_types=None, chat_types=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                            chat_types=chat_types, content_types=content_types, commands=commands,
                            regexp=regexp, func=func, **kwargs)
            self.message_handlers.append(handler_dict)
            return handler
        return decorator

    def add_handlers(self, bot):
        bot.message_handlers.extend(self.message_handlers)
        bot.callback_query_handlers.extend(self.callback_query_handlers)