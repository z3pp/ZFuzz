import argparse


class RangeAction(argparse.Action):

    """ Check the range of an argument """

    def __init__(self, mini, maxi, *args, **kwargs):

        self.mini = mini
        self.maxi = maxi
        kwargs["metavar"] = "[{}-{}]".format(self.mini, self.maxi)
        super(RangeAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, value, option_string=None):

        if not (self.mini <= value <= self.maxi):
            error = "invalid choice: '{}': choose from [{}-{}]"\
                     .format(value, self.mini, self.maxi)
            raise argparse.ArgumentError(self, error)
        setattr(namespace, self.dest, value)


class UrlAction(argparse.Action):

    """ Check the format of an url """

    def __call__(self, parser, namespace, value, option_string=None):

        if not value.startswith("http://") | value.startswith("https://"):
            error = "invalid url format: valid format:\
                     'http(s)://example.com/'".format(value)
            raise argparse.ArgumentError(self, error)
        setattr(namespace, self.dest, value)


class DictAction(argparse.Action):

    """ Create a dict from an str """

    def __call__(self, parser, namespace, values, option_string=None):

        headers = {}
        for value in values:
            data = value.replace(' ', '').split(":")
            if not len(data) == 2:
                error = "invalid format: valid format: 'some:value'"
                raise argparse.ArgumentError(self, error)
            headers[data[0]] = data[1]
        setattr(namespace, self.dest, headers)


class DataAction(argparse.Action):

    """ Parse data values """

    def __call__(self, parser, namespace, value, option_string=None):

        datas = {}
        value = value.split("&")
        for data in value:
            d = data.split("=")
            if not len(d) == 2:
                error = "invalid format valid format: 'some=data'"
                raise argparse.ArgumentError(self, error)
            datas[d[0]] = d[1]
        setattr(namespace, self.dest, datas)


class ListAction(argparse.Action):

    """ Convert items separated by commas to a list """

    def __call__(self, parser, namespace, value, option_string=None):

        codes = []
        for code in value.replace(' ', '').split(","):
            if not code.isdigit():
                error = "invalid format valid format: '404, 200, ...'"
                raise argparse.ArgumentError(self, error)
            codes.append(int(code))
        setattr(namespace, self.dest, codes)
