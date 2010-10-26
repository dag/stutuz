Werkzeug WSGI utilities
=======================

.. module:: werkzeug

Werkzeug is a lower-level library for dealing with HTTP over WSGI.
Flask is built on top of Werkzeug and provides many higher-level interfaces,
but Werkzeug is very powerful and it's good to know a little about it.

* `Full documentation <http://werkzeug.pocoo.org/documentation/dev/>`_


Utilities
---------

URLs
^^^^

.. autofunction:: url_encode

.. autofunction:: url_quote

.. autofunction:: url_quote_plus

.. autofunction:: url_unquote

.. autofunction:: url_unquote_plus

.. autofunction:: url_fix

.. autofunction:: uri_to_iri

.. autofunction:: iri_to_uri


HTML
^^^^

.. autofunction:: escape

.. autofunction:: unescape


HTTP
^^^^

Useful attributes on Flask's request object.

``request.accept_charsets``
    .. autoclass:: CharsetAccept
       :members:
       :inherited-members:

``request.accept_languages``
    .. autoclass:: LanguageAccept
       :members:
       :inherited-members:

``request.accept_mimetypes``
    .. autoclass:: MIMEAccept
       :members:
       :inherited-members:

``request.user_agent``
    .. autoclass:: UserAgent
       :members:

``request.authorization``
    .. autoclass:: Authorization
       :members:


Security
^^^^^^^^

.. autofunction:: secure_filename

.. autofunction:: generate_password_hash

.. autofunction:: check_password_hash


General use
^^^^^^^^^^^

.. autofunction:: cached_property

.. autofunction:: import_string

.. autofunction:: find_modules


Exceptions
----------

.. module:: werkzeug.exceptions

.. autoexception:: BadRequest

.. autoexception:: Unauthorized

.. autoexception:: Forbidden

.. autoexception:: NotFound

.. autoexception:: MethodNotAllowed

.. autoexception:: NotAcceptable

.. autoexception:: RequestTimeout

.. autoexception:: Gone

.. autoexception:: LengthRequired

.. autoexception:: PreconditionFailed

.. autoexception:: RequestEntityTooLarge

.. autoexception:: RequestURITooLarge

.. autoexception:: UnsupportedMediaType

.. autoexception:: InternalServerError

.. autoexception:: NotImplemented

.. autoexception:: BadGateway

.. autoexception:: ServiceUnavailable
