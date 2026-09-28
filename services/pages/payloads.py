from dataclasses import dataclass, field

from faker import Faker

faker = Faker()


@dataclass
class PagePayloads:
    title: str = field(default_factory=faker.pystr)
