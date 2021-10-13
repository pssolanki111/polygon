
.. _enums_header:

What the Hell are Enums Anyways
===============================

Sooooo... you've had enough of these ``enums`` and finally decided to know what the hell they actually are and why you should care about them.

Well read this page to get your answers.

You should have seen them on many methods' documentation as argument choices.

First up, does everyone need them? that depends on their use case. enums in this library are only used on some endpoints, especially the ones in reference APIs and some basic uses in
stream clients. So if someone only needs to ochlv chart data, they probably won't need to use enums.

**If you notice any value which is supported by the API but not included in the enums, Let me Know using discussions**

What are they
-------------

Simplest non technical terms definition
 They are a way to define pseudo constants (read constants) in python (python doesn't have anything as constants. That's why enums are precious :D). They have many use cases other than constants but for this library you only need to know this far.

For example
 consider the enum :class:`polygon.enums.AssetClass` which has 4 values inside of it.  The values are just class attribute and you can access
 them just like you'd access any other class attribute. ``print(polygon.enums.AssetClass.STOCKS)`` would print the string ``stocks``.
 so in another words this enum class has 4 member enums which can be used to specify the value wherever needed.
 Like this ``some_function(arg1, asset=AssetClass.STOCKS)``.

**when you pass in an enum to a function or a method, it is equal to passing in the value of that enum.**

so instead of `some_function(arg1, asset=AssetClass.STOCKS)`` i could have said `some_function(arg1, asset='stocks')`` and both mean the same thing.

Here are `All the enums of this library in one place <https://polygon.readthedocs.io/en/latest/Library-Interface-Documentation.html#module-polygon.enums>`__

Then why not just pass in raw values? Why do we need enums?
-----------------------------------------------------------

I mean you could do that. In fact many people would still do that despite the notes here (I'll be watching you all :/).

but think about it this way, can you have enums for a parameter which expects a person's name? Of course not.
Because there isn't any constant value (or a fixed set of values) to choose from.

but can i have enums for TickerTypes? Yes.
Because it has a set of fixed values and the API would not return the correct data if the value passed in is different than the ones which are
in the fixed set.

**Using enums**

* Avoids passing in incorrect values.
* Avoids typing mistakes while passing in parameter values (I'm looking at you ``TRAILING_TWELVE_MONTHS_ANNUALIZED``)
* gives you a fixed set of values to choose from and you don't have to hit and trial to know supported values.
* And finally, IDE autocomplete would make your life even easier while writing code that makes use of enums

Finally, it's not an absolute necessity to use enums but they are very much recommended.

Okay how do I use them then
---------------------------

To start off, like any other name, you'd need to import the names. Now there are many ways to do that and it's up to your
coding preferences. Make use of your IDE auto-completions to make it easier to fill in enums.

Some common ways are

Approach 1 - importing all enums at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  import polygon  # which you already do for using other clients so nothing new to import here

  # now you can use enums as

  client.some_function(other_args, arg=polygon.enums.TickerType.ADRC)

  # OR
  import polygon.enums as enums

  client.some_function(other_args, arg=enums.TickerType.ETF)

as you see this allows you to access `all enums <https://polygon.readthedocs.io/en/latest/Library-Interface-Documentation.html#module-polygon.enums>`__ without having to import each
one individually. But this also mean you'd be typing longer names (not big of an issue considering IDE completions).

Note that importing all enums doesn't have any resource overhead so don't worry about enums eating your RAM.

Approach 2 - importing just the enums you need
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This approach is nicer for cases when you only specifically need a few enums.

.. code-block:: python

  from polygon.enums import TickerType

  # using it as
  client.some_function(other_args, arg=TickerType.CS)

  # OR
  from polygon.enums import (TickerType, AssetClass)

  client.some_function(other_args, arg=TickerType.CS)

  client.some_other_function(other_args, arg=TickerType.CS, other_arg=AssetClass.STOCKS)


You could use any other import syntax if you like.