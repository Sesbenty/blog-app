from dataclasses import dataclass


class Event:
    pass


@dataclass
class PublishBlog(Event):
    pass
