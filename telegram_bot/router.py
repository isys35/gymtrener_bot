import re

from telegram_bot.bot import Bot


class ReFormat:
    VAR_NAME = r'[_a-zA-Z][_a-zA-Z0-9]*'

    WILDCARD = r'.*'
    URL_SUBSTRING = r'[^/]+'
    INT_NUMBER = r'[0-9]+'
    FLOAT_NUMBER = r'[0-9]+[.,]?[0-9]+'
    PHONE_NUMBER = r"\+?(375|80|0)?\(?[0]?(?<tcode>\d{2})\)?(?<tphone>\d{3}[-\s]*\d{2}[-\s]*\d{2})"
    EMAIL = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+.+.[a-zA-Z]{2,4}'
    USERNAME = r'[a-zA-Z0-9_-]{3,16}'
    ZIP_CODE = r"\d{6}"
    HEX_COLOR = r'#([a-fA-F]|[0-9]){3, 6}'

    URL_VAR = [
        (f'wc', WILDCARD),
        (f'str', URL_SUBSTRING),
        (f'int', INT_NUMBER),
        (f'float', FLOAT_NUMBER),
        (f'phone', PHONE_NUMBER),
        (f'email', EMAIL),
    ]

    @classmethod
    def re_url(cls, url: str) -> str:
        """
        Преобразует параметры запроса в регулярные выражения.
        Допустимые параметры запроса:
        <wc:par_name> - любое совпадение
        <str:par_name> - строка
        <int:par_name> - целое число
        <float:par_name> - число с плавающей точкой
        <phone:par_name> - номер телефона
        <email:par_name> - email
        <re:regexp:par_name> - регулярное выражение (проверяется)
        :param url: строка url-запроса
        :return: преобразованная строка
        """
        for param in cls.URL_VAR:
            param_name_list = re.findall(f"<{param[0]}:(?P<var>{cls.VAR_NAME})>", url)
            if param_name_list:
                for param_name in param_name_list:
                    url = url.replace(fr'<{param[0]}:{param_name}>', fr'(?P<{param_name}>{param[1]})')

        re_param_list = re.finditer(f"<re:(?P<var>{cls.VAR_NAME}):(?P<regexp>.+)>", url)
        for re_param in re_param_list:
            group_dict = re_param.groupdict()
            pattern = fr"(?P<{group_dict['var']}>{group_dict['regexp']})"
            try:
                re.compile(pattern)
                url = url.replace(
                    fr"<re:{group_dict['var']}:{group_dict['regexp']}>",
                    pattern)
            except re.error as exc:
                raise ValueError(
                    "Bad pattern '{}': {}".format(pattern, exc)) from None
        return url


class Router:
    static_urls: dict = None
    dynamic_urls: list = None

    def __init__(self, urls: list):
        self.static_urls = {}
        self.dynamic_urls = []

        for url in urls:
            url_after_re = ReFormat.re_url(url[0])
            if url_after_re == url[0]:
                self.static_urls.update([url])
            else:
                self.dynamic_urls.append((url_after_re, url[1]))

    def url_dispatcher(self, bot: Bot):
        view = self.static_urls.get(bot.user.full_request)
        if view is not None:
            try:
                 view(bot)
            except Exception as ex:
                print(ex)
                bot.error_404()
            return
        else:
            result = {}
            for dynamic_url in self.dynamic_urls:
                result = re.fullmatch(dynamic_url[0],
                                      bot.user.full_request)
                if result:
                    view = dynamic_url[1]
                    break
            if view:
                try:
                    view(bot, **result.groupdict())
                except Exception as ex:
                    print(ex)
                    bot.error_404()
                return
        bot.error_404()

