from requests.status_codes import codes

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

