### app/utils.py

import hashlib
import time
from uuid import UUID, SafeUUID

from app.config import Config


class UUIDv8:
    """Custom UUID class for generating domain-specific identifiers.
    The UUIDv8 structure is as follows:

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           secret_1                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            secret_2           |1 0 0 0|0 0 0 0 0 0 0 0 0 0 0 0|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |1 0|0 0 0 0 0 0 0 0 0 0 0 0 0 0|            domain             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           timestamp                           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """

    version = 0b1000
    variant = 0b10

    def __init__(self, secret1: str, secret2: str) -> None:
        self.secret1 = secret1
        self.secret2 = secret2
        pass

    def _hash_value(self, value: str, length: int) -> int:
        """Hash a value using SHA-256 and return the first `length` bits."""
        hash_digest = hashlib.sha256(value.encode()).digest()
        return int.from_bytes(hash_digest[: (length // 8)], byteorder="big")

    def generate(self, domain: str) -> UUID:
        """Generate a UUIDv8 with the specified structure."""

        # First 32 bits from hash(secret1)
        # e.g., [12345678]-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        part1 = self._hash_value(self.secret1, 32)

        # Next 16 bits from hash(secret2 + first 32 bits)
        # e.g., 12345678-[1234]-xxxx-xxxx-xxxxxxxxxxxx
        part2 = self._hash_value(str(part1) + self.secret2, 16)

        # Next 4 bits for the version and 12 empty bits, so 16 bits total
        # e.g., 12345678-1234-[8000]-xxxx-xxxxxxxxxxxx
        #                    /      \
        #              [1000][000000000000]
        part3 = UUIDv8.version << 12

        # Next 2 bits for the variant and 14 empty bits, so 16 bits total
        # e.g., 12345678-1234-8000-[8000]-xxxxxxxxxxxx
        #                         /      \
        #                   [10][00000000000000]
        part4 = UUIDv8.variant << 14

        # Next 16 bits from hash(domain + first 80 bits)
        # e.g., 12345678-1234-8000-8000-[1234]xxxxxxxx
        part5 = self._hash_value(
            str(part1) + str(part2) + str(part3) + str(part4) + domain,
            16,
        )

        # Last 32 bits from hash(current_timestamp[nanoseconds] + first 96 bits)
        # e.g., 12345678-1234-8000-8000-1234[12345678]
        part6 = self._hash_value(
            str(part1)
            + str(part2)
            + str(part3)
            + str(part4)
            + str(part5)
            + str(time.time_ns()),
            32,
        )

        # Construct the 128-bit UUID
        uuid_int = (
            (part1 << 96)
            | (part2 << 80)
            | (part3 << 64)
            | (part4 << 48)
            | (part5 << 32)
            | part6
        )

        # Convert to UUID format
        return UUID(int=uuid_int, is_safe=SafeUUID.unsafe)

    def complete(self, part5n6: str) -> UUID:
        """Knowing the last 48 bits of the UUID, generate the whole UUID."""
        part1 = self._hash_value(self.secret1, 32)
        part2 = self._hash_value(str(part1) + self.secret2, 16)
        part3 = UUIDv8.version << 12
        part4 = UUIDv8.variant << 14
        part5n6 = int(part5n6, 16)

        uuid_int = (
            (part1 << 96)
            | (part2 << 80)
            | (part3 << 64)
            | (part4 << 48)
            | part5n6
        )
        return UUID(int=uuid_int, is_safe=SafeUUID.unsafe)


def uuid8(domain: str) -> UUID:
    """Generate a UUIDv8 with the default structure."""
    return UUIDv8(Config.UUID_SECRET1, Config.UUID_SECRET2).generate(domain)


def complete_uuid8(part5n6: str) -> UUID:
    """Generate a UUIDv8 with the default structure, knowing the secrets and"
    the last 48 bits of the UUID."""
    return UUIDv8(Config.UUID_SECRET1, Config.UUID_SECRET2).complete(part5n6)
