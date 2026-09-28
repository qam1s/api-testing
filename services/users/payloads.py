from dataclasses import dataclass, field

from faker import Faker

faker = Faker()


@dataclass
class UpdateUserPayloads:
    email: str = field(default_factory=faker.email)


@dataclass
class CreateUserPayloads(UpdateUserPayloads):
    username: str = field(default_factory=faker.user_name)
    password: str = field(default_factory=faker.password)
