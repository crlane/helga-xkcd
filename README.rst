==========
helga-xkcd
==========

Description
===========

The helga-xkcd plugin provides a helga_ command for retrieving xkcd comics through that site's `JSON based api`_.

--------

Usage:
======
Get the latest xkcd
.. code-block:: none
    !xkcd

Get a random xkcd comic
.. code-block:: none
    !xkcd random

Get xkcd comic number <n>. For example, to fetch comic number 10:
.. code-block:: none
    !xckd number 10


Get a comic about a given text string. Using text indexing
.. code-block:: none
    !xkcd about pi


Features:
=========

Provides commands for fetching official xkcd comic images and displaying its hidden text

- [ ] fetch the latest comic `!xkcd`
- [ ] fetch a specific comic `!xkcd [n]`
- [ ] fetch a comic about a keybword: `!xkcd about [keyword]`

- [ ] Periodically refreshes index of comics it knows about

.. _helga: https://github.com/shaunduncan/helga
.. _`JSON based api`: https://xkcd.com/json.html


