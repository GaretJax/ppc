from progressbar import Bar, Percentage, ProgressBar, SimpleProgress, Timer


class ValueProgressBar(ProgressBar):
    def __next__(self):
        try:
            self.iter_value = next(self._ProgressBar__iterable)
            if self.start_time is None:
                self.start()
            else:
                self.update(self.currval + 1)
            return self.iter_value
        except StopIteration:
            self.finish()
            raise
    next = __next__


class FormatLabel(Timer):

    'Displays a formatted label'

    mapping = {
        'elapsed': ('seconds_elapsed', Timer.format_time),
        'finished': ('finished', None),
        'last_update': ('last_update_time', None),
        'max': ('maxval', None),
        'seconds': ('seconds_elapsed', None),
        'start': ('start_time', None),
        'index': ('currval', None),
        'value': ('iter_value', None),
    }

    def __init__(self, format):
        self.format = format

    def update(self, pbar):
        context = {}
        for name, (key, transform) in self.mapping.items():
            try:
                value = getattr(pbar, key)

                if transform is None:
                    context[name] = value
                else:
                    context[name] = transform(value)
            except:  # pragma: no cover
                pass

        return self.format.format(**context)


def get_generic_progress(label):
    progress = ProgressBar(widgets=[
        ' ', label, '  ', Bar(left='[', right=']'), ' ',
        Percentage(), ' (', SimpleProgress(), ') ',
    ])
    return progress


def get_label_progress(label):
    print label
    progress = ValueProgressBar(widgets=[
        ' ', FormatLabel('{value:40}'), '  ', Bar(left='[', right=']'), ' ',
        Percentage(), ' (', SimpleProgress(), ') ',
    ])
    return progress
