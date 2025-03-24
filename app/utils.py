### app/utils.py

import hashlib
import time
from uuid import UUID, SafeUUID

from app.config import Config


class UUIDv8:
    """Custom UUID version8 generator.
    See https://www.rfc-editor.org/rfc/rfc9562.html#name-uuid-version-8
    for further information.
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
        part2 = self._hash_value(self.secret2 + str(part1), 16)

        # Next 4 bits for the version and 12 empty bits, so 16 bits total
        # e.g., 12345678-1234-[8000]-xxxx-xxxxxxxxxxxx
        part3 = UUIDv8.version << 12

        # Next 2 bits for the variant and 14 empty bits, so 16 bits total
        # e.g., 12345678-1234-8000-[8000]-xxxxxxxxxxxx
        part4 = UUIDv8.variant << 14

        # Next 16 bits from hash(domain + first 80 bits)
        # e.g., 12345678-1234-8000-8000-[1234]xxxxxxxx
        part5 = self._hash_value(
            domain + str(part1) + str(part2) + str(part3) + str(part4),
            16,
        )

        # Last 32 bits from hash(current_timestamp[nanoseconds] + first 96 bits)
        # e.g., 12345678-1234-8000-8000-1234[12345678]
        part6 = self._hash_value(
            str(time.time_ns())
            + str(part1)
            + str(part2)
            + str(part3)
            + str(part4)
            + str(part5),
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


def uuid8(domain: str) -> UUID:
    """Generate a UUIDv8 with the default structure."""
    return UUIDv8(Config.UUID_SECRET1, Config.UUID_SECRET2).generate(domain)
