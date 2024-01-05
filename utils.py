
class ObservableList(list):
    def __init__(self, *args, callback):
        self.callback = callback
        super().__init__(*args)

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self.callback()

    def append(self, *args, **kwargs):
        super().append(*args, **kwargs)
        self.callback()