from dataclasses import dataclass, field

from faker import Faker

faker = Faker()


@dataclass
class UpdateCommentPayloads:
    content: str = field(default_factory=faker.pystr)


@dataclass
class CreateCommentPayloads(UpdateCommentPayloads):
    post: int = field(default_factory=faker.pyint)
