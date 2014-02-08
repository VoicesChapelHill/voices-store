.. _products:

Product management
-------------------

The product management page allows adding and editing products
(but not viewing sales information, see the
:ref:`reports` section for that).

It's possible some staff will not have access to this section if they
don't need it.

When giving names to products, always remember we'll probably be
selling very similar products for years to come, and looking at
reports of sales and so forth. So "May 2013 Cantari Concert Ticket"
is a better name than "Ticket" for a product.

Here are the main attributes of a product.

Name
    A one-line (40 chars or less) text string uniquely identifying
    the product.

Blurb
    A phrase (no more than two lines) that is included in product listings
    to describe the product a little more than the name.

Description
    A complete description of the product, used on the product page. Can
    be multiple paragraphs if necessary.

Draft
    A product in draft mode is displayed only to logged-in staff members, and
    ignores the product sell dates. It is clearly marked "DRAFT" anywhere it
    appears on the site. It cannot really be bought; a cart with draft products
    in it will refuse to check out.

Sell dates
    The date/times between which the product is shown on the site and can be purchased.
    Both dates are optional, indicating no restriction on that end of the sell period.

Member only
    A member-only product is only displayed to those who are members.

Performances
    (optional) if the product is an event ticket, and the event occurs more than once so
    that a purchaser needs to specify which performance they're buying a ticket for, add
    a performance line for each one to the product.  Each performance has a few
    characteristics of its own:

    * Date/time of the performance
    * Sell dates - like the overall product sell date, except that it further restricts
      when tickets are offered for this particular performance, and the end sell date/time
      is required.

Pricing
    How this product is priced. Possible values:

    * One price - Enter one price in Prices. Price name is ignored.
    * Multiple - user has choices, enter multiple in Prices, which see.
    * User entered - user can enter a price. Used for donations.

Prices
    Enter zero or more prices here (see also Pricing). For example,
    tickets might have a General audience price and a student price:

    * Name
    * Price

    For one price products, the name associated with the price is ignored.

    We could add sell dates to these in the future. That would enable things like
    early-bird pricing that is only available until a month before the concert.

Notifications
    One or more staff members who will be emailed anytime a purchase is
    made of this product, and might also get periodic reports if we implement
    those at some point.

Special instructions prompt
    (optional) This is an optional text field. If text is entered here for a product, then
    during checkout, under this product in the list of purchases, this text will be
    displayed as a prompt, along with a text field that the user will be required to
    enter something into.

    What is this for? For example, on a member dues product, you could add special
    instructions "Who is this dues payment for" to force the purchaser to name the
    chorus member they're paying dues for. This is because commonly one person might
    pay dues for themself and their partner.

Quantifiable
    (default True) if False, user will not be allowed to enter a quantity for this
    product, but may add it to their cart multiple times.  If true, we might some day
    implement merging items in the cart that have all the same options... but no
    hurry on that.

    This is also intended to cope with people paying dues, to force them to enter
    a separate name for each dues payment.

Account
    Which accounting "account" this sale should be assigned to

Class
    Which accounting "class" this sale should be assigned to

Notes
~~~~~

Price changes
    If a price needs to change on an existing product - for example, the price of black
    concert folders goes up - set an end sell date on the current product, and create a
    new product with the new price with a start sell date after the end sell date of the
    product with the old price.

    This is a little awkward, but it happens rarely enough that it's not worth writing
    a lot of special code for it.
