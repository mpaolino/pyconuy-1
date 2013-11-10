Pyker
=====

Expand voice recognition library.

This library takes care of:

* Audio format checking.
* Audio format conversion.
* `Expand Voice Recognition API <https://github.com/expanduc/pyconuy>`_
  communication.
* Sync or async modes.

  + Poll the server until the recognition is finished (sync).
  + Issue the recognition request and return immediately (async).


------------
Installation
------------

* Clone the repo::

.. code:: sh

    $ git clone https://github.com/tooxie/pyconuy.git
    $ cd pyconuy

* Create a virtualenv::

.. code:: sh

    $ virtualenv .venv
    $ source .venv/bin/activate

* Install::

.. code:: sh

    $ python setup.py develop


-----------------
Available methods
-----------------

These are the methods available in the *pyker.GenderRecognizer* class.


recognize(async=True)
---------------------

Starts the recognition process. If *async* is set to True, it will just start
the job, but return before the recognition is complete. It will be up to the
developer to poll the server manually using *get_result()*.


is_male() and is_female()
-------------------------

Checks if the result is one of those options. Be careful because if job has not
yet finished, both methods will return False. Use the *recognition_complete()*
method first.


get_result()
------------

Issues a request to the recognition server asking if the current job has
completed. If it has, it caches the result to avoid subsequent hits to the
server.


recognition_complete()
----------------------

Indicates whether the recognition process finished.


----------
Exceptions
----------

Possible exceptions.


ConversionError
---------------

The converter (ffmpeg by default) return a non-zero code.


FileDoesNotExistError
---------------------

The file provided to *GenderRecognizer* does not exist.


UnsupportedFormatError
----------------------

The file provided to *GenderRecognizer* is not in the correct format and cannot
be converted.


ServerError
-----------

The server returned an non-200 status code. Keep in mind that this could also
mean that the request issued did not meet the server's expectations.


InsufficientDataError
---------------------

The audio file does not contain enough information.


---------
Constants
---------

The constants **GenderRecognizer.MALE** and **GenderRecognizer.FEMALE** are
available to abstract you from the internal representation that the API uses
for these values. Quick example:

.. code:: python

    recognizer = GenderRecognizer(audio_file)
    result = recognizer.recognize()
    assert result == GenderRecognizer.FEMALE


-----
Usage
-----

You will need an audio file of any format, Pyker will convert it to the
appropriate format if needed. Here is an example:

.. code:: python

    # -*- coding: utf-8 -*-
    from pyker import GenderRecognizer

    audio_file = '/var/sources/audio.mp3'

    recognizer = GenderRecognizer(audio_file)
    recognizer.recognize()

    while not recognizer.recognition_complete():
        recognizer.get_result()

    print('Female' if recognizer.is_female() else 'Male')


You can do this in a synchronous way as well:

.. code:: python

    # -*- coding: utf-8 -*-
    from pyker import GenderRecognizer

    audio_file = '/var/sources/audio.mp3'

    recognizer = GenderRecognizer(audio_file)
    result = recognizer.recognize(async=False)

    print('Female' if recognizer.is_female() else 'Male')


-----------------
Running the tests
-----------------

To run the test suite you need to do 2 quick things.

* Install the development dependencies::

.. code:: sh

    $ pip install -r requirements-dev.pip

* Run the tests::

.. code:: sh

    $ PYTHONPATH=`pwd` nosetests --with-coverage --cover-package=pyker


--------------
Nice-to-have's
--------------

Given the time restrictions, I had to prioritize and focus on certain aspects
of the library. If I had more time, I would:

* Write more tests (even though the code coverage is above 90% already)
* More abstractions and modularity: allow to easily switch the classes in use.
* Better sequence handling.
* Write more code examples.


----------
Questions?
----------

Read the source =)

Or find me as `@tuxie_ <https://twitter.com/tuxie_>`_ in twitter.

Happy hacking!
