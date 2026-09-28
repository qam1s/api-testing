from dataclasses import dataclass, field

from faker import Faker

faker = Faker()


@dataclass
class PostPayloads:
    title: str = field(default_factory=faker.pystr)
    status: str = "publish"
