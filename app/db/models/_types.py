from dataclasses import dataclass
from enum import Enum

import base64
from io import BytesIO
from PIL import Image

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    LargeBinary,
    Numeric,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.types import SmallInteger as SmallIntegerType
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import PasswordType
from sqlalchemy_utils import IPAddressType


class PNGImageType(TypeDecorator):
    """
    A TypeDecorator that allows for PNG images to be stored in the database as
    a base64 encoded string.
    """

    impl = LargeBinary  # the underlying column type to store the value in the
    # database is a LargeBinary

    cache_ok = True  # the ImageType is immutable, so it can be cached
    # (see https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.type
    # s.ExternalType.cache_ok)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)

    def process_bind_param(self, value, dialect):
        if value is not None:
            buffered = BytesIO()
            value.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            return base64.b64encode(img_bytes)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Image.open(BytesIO(base64.b64decode(value)))
        return None


class EnumType(TypeDecorator):
    """
    A TypeDecorator that allows for an Enum class to be used as a column type,
    where the value stored in the database is the Enum's integer ID and not the
    Enum's name as per the default EnumType in SQLAlchemy.
    E.g., when defining a Enum class like so:

    class MyEnum(enum.PrintableEnum):
        FOO = 1
        BAR = 2

    and using this EnumType as a column type, the value stored in the database
    will be 1 or 2, and not 'FOO' or 'BAR'.
    The EnumType also allows for the Enum's value to be a (named)tuple, in
    which case the code of the (named)tuple is stored in the database.
    E.g., when defining a Enum class like so:

    NamedTupleType = namedtuple('NamedTupleType', ['code', 'desc']):

    class MyEnum(enum.PrintableEnum):
        FOO = NamedTupleType(1, 'Foo')
        BAR = NamedTupleType(2, 'Bar')

    and using this EnumType as a column type, the value stored in the database
    will be 1 or 2, and not 'FOO' or 'BAR' (and neither 'Foo' or 'Bar').
    This is the preferred way to use this class.
    """

    impl = SmallIntegerType  # the underlying column type to store the value in
    # the database is an (Small)Integer, opposed to the default EnumType which
    # uses a String

    cache_ok = True  # the EnumType is immutable, so it can be cached
    # (see https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.type
    # s.ExternalType.cache_ok)

    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__()

    @property
    def python_type(self):
        return self.enum_class

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_class):
            return value.code
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            for member in self.enum_class:
                if member.code == value:
                    return member
            return ValueError(
                f"Unknown type with ID {value} in {self.enum_class.__name__}"
                " enum"
            )
        return None


@dataclass
class ColumnsDomains:
    ID = UUIDType(binary=False)  # Universally unique identifier
    SHORT_NAME = String(63)  # Alphanumeric short name
    LONG_NAME = String(127)  # Alphanumeric long name
    TEXT = Text  # Variable sized text
    PASSWORD = PasswordType(
        31,
        schemes=["pbkdf2_sha512", "md5_crypt"],
        deprecated=["md5_crypt"],
    )
    MAC_ADDRESS = String(17)  # MAC address
    IP_ADDRESS = IPAddressType  # IP address
    NO = SmallInteger  # Numeric ID
    POS = SmallInteger  # Index, position or offset
    FLAG = Boolean  # Flag (True/False)
    DATETIME = DateTime(timezone=True)  # UTC DateTime with timezone info
    TIME = Integer  # Interval expressed as integer number of seconds
    STRING = String(255)  # Alphanumeric value
    CHOICE = EnumType  # Enumerated value
    INT = Integer  # Integer number
    DECIMAL = Numeric(16, 8, asdecimal=False)  # Decimal number
    SIZE = SmallInteger  # Size, length or count expressed as number of items
    DATA = LargeBinary  # Binary type to save unstructured data
    IMG = PNGImageType  # Binary type to save PNG image data
    INFOS = LargeBinary  # Binary type to save structured data


@dataclass(frozen=True, eq=False)
class TypeDescriptionMixin:
    code: int  # Unique identifier of the type in the enumeration class
    desc: str  # Description of the type

    def __repr__(self):
        return self.desc


class UserRoleType(TypeDescriptionMixin, Enum):
    ADMIN = 1, "Administrator"  # Administrator
    OPERATOR = 2, "Operator"  # Operator


class OrderStatusType(TypeDescriptionMixin, Enum):
    CANCELLED = -1, "Cancelled"  # The order is cancelled
    PENDING = 0, "Pending"  # The order is pending
    IN_PROGRESS = 1, "In progress"  # The order is in progress
    COMPLETED = 2, "Completed"  # The order is completed


class PaymentMethodType(TypeDescriptionMixin, Enum):
    CASH = 0, "Cash"  # The payment is done in cash
    ELECTRONIC = 1, "Electronic"  # The payment is done electronically


class MenuSectionType(TypeDescriptionMixin, Enum):
    APPEETIZERS = 1, "Appetizers"  # Appetizers
    FIRST_COURSES = 2, "First courses"  # First courses
    MAIN_COURSES = 3, "Main courses"  # Main courses
    SIDE_DISHES = 4, "Side dishes"  # Side dishes
    DESSERTS = 5, "Desserts"  # Desserts
    SINGLE_DISHES = 6, "Single dishes"  # Single dishes
    DRINKS = 7, "Drinks"  # Drinks


class AllergenType(TypeDescriptionMixin, Enum):
    # Allergen types enumeration class based on the European Union Regulation
    # No 1169/2011 of the European Parliament and of the Council of 25 October
    # 2011 on the provision of food information to consumers, amending
    # Regulations (EC) No 1924/2006 and (EC) No 1925/2006 of the European
    # Parliament and of the Council, and repealing Commission Directive
    # 87/250/EEC, Council Directive 90/496/EEC, Commission Directive 1999/10/EC,
    # Directive 2000/13/EC of the European Parliament and of the Council,
    # Commission Directives 2002/67/EC and 2008/5/EC and Commission Regulation
    # (EC) No 608/2004 (Text with EEA relevance).
    #
    # https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2011:304:0018:0063:en:PDF

    # Cereals containing gluten, namely: wheat, rye, barley, oats, spelt, kamut
    # or their hybridised strains, and products thereof, except:
    # (a) wheat based glucose syrups including dextrose ( 1 );
    # (b) wheat based maltodextrins ( 1 );
    # (c) glucose syrups based on barley;
    # (d) cereals used for making alcoholic distillates including ethyl alcohol
    #   of agricultural origin;
    GLUTEN = 1, "Cereals containing gluten"  # Gluten

    # Crustaceans and products thereof;
    CRUSTACEANS = 2, "Crustaceans"  # Crustaceans and derivatives

    # Eggs and products thereof;
    EGGS = 3, "Eggs"  # Eggs and derivatives

    # Fish and products thereof, except:
    # (a) fish gelatine used as carrier for vitamin or carotenoid preparations;
    # (b) fish gelatine or Isinglass used as fining agent in beer and wine;
    FISH = 4, "Fish"  # Fish and derivatives

    # Peanuts and products thereof;
    PEANUTS = 5, "Peanuts"  # Peanuts and derivatives

    # Soybeans and products thereof, except:
    # (a) fully refined soybean oil and fat(1);
    # (b) natural mixed tocopherols (E306), natural D-alpha tocopherol,
    #   natural D-alpha tocopherol acetate, and natural
    # D-alpha tocopherol succinate from soybean sources;
    # (c) vegetable oils derived phytosterols and phytosterol esters from
    #   soybean sources;
    # (d) plant stanol ester produced from vegetable oil sterols from soybean
    #   sources;
    #
    # ( 1 ) And the products thereof, in so far as the process that they have
    # undergone is not likely to increase the level of allergenicity assessed
    # by the Authority for the relevant product from which they originated.
    SOYBEANS = 6, "Soybeans"  # Soybeans and derivatives

    # Milk and products thereof (including lactose), except:
    # (a) whey used for making alcoholic distillates including ethyl alcohol
    #   of agricultural origin;
    # (b) lactitol;
    MILK = 7, "Milk (including lactose)"  # Milk and derivatives

    # Nuts, namely: almonds (Amygdalus communis L.), hazelnuts (Corylus
    # avellana), walnuts (Juglans regia), cashews (Anacardium occidentale),
    # pecan nuts (Carya illinoinensis [Wangenh.] K. Koch), Brazil nuts
    # (Bertholletia excelsa), pistachio nuts (Pistacia vera), macadamia or
    # Queensland nuts (Macadamia ternifolia), and products thereof, except for
    # nuts used for making alcoholic distillates including ethyl alcohol of
    # agricultural origin;
    NUTS = 8, "Nuts"  # Nuts and derivatives

    # Celery and products thereof;
    CELERY = 9, "Celery"  # Celery and derivatives

    # Mustard and products thereof;
    MUSTARD = 10, "Mustard"  # Mustard and derivatives

    # Sesame seeds and products thereof;
    SESAME_SEEDS = 11, "Sesame seeds"  # Sesame seeds and derivatives

    # Sulphur dioxide and sulphites at concentrations of more than 10 mg/kg or
    # 10 mg/litre in terms of the total SO2 which are to be calculated for
    # products as proposed ready for consumption or as reconstituted according
    # to the instructions of the manufacturers;
    SULFUR_DIOXIDE = 12, "Sulphur dioxide and sulphites"  # Sulfur dioxide

    # Lupin and products thereof;
    LUPIN = 13, "Lupin"  # Lupin and derivatives

    # Molluscs and products thereof;
    MOLLUSCS = 14, "Molluscs"  # Molluscs and derivatives
