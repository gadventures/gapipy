from requests.status_codes import codes

# Date formats

# ISO Date
DATE_FORMAT = "%Y-%m-%d"

# ISO Date-Time Local
DATE_TIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M:%S"

# ISO Date-Time UTC
DATE_TIME_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


# The default set of HTTP Status codes that will result in Query.get
# returning a `None` value.
#
# Since 2.25.0 (See: https://github.com/gadventures/gapipy/pull/119)
#
# This is now passed as default parameter to `Query.get`. This has allowed
# a slight modification to the behaviour of Resource.fetch, which now passes
# in an explicit `None` value for `httperrors_mapped_to_none` kwarg.`Query.get`
# will now raise the requests.HTTTPError when an attempt to `fetch` stub fails,
# providing more expressive errors to be bubbled up.
HTTPERRORS_MAPPED_TO_NONE = (
    codes.FORBIDDEN,  # 403
    codes.NOT_FOUND,  # 404
    codes.GONE,       # 410
)

# A list of OK Response codes
ACCEPTABLE_RESPONSE_STATUS_CODES = (
    codes.OK,        # 200
    codes.CREATED,   # 201
    codes.ACCEPTED,  # 202
)

ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "OPTIONS", ]

JSON_CONTENT_TYPE = "application/json; charset=utf-8"

# Resource Constants

# Image Types
IMAGE_TYPE_BANNER = "BANNER"
IMAGE_TYPE_MAP = "MAP"
IMAGE_TYPE_OTHER = "OTHER"
IMAGE_TYPES = (
    IMAGE_TYPE_BANNER,
    IMAGE_TYPE_MAP,
    IMAGE_TYPE_OTHER,
)
