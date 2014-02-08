User View of the Site
=====================

This is how the site looks and works to the end users - our customers.

There are two kinds of customers, the public and our members.

Accounts
--------

Users can create an account at any time while visiting the site, and can log in
while using the site.

Having an account does the following:

* validates their email address (before they can use the account, they have to click a
  link that is emailed to them, this proves they have access to the email address that
  they gave)
* remembers their name and email address
* optionally remember their payment details
* keep a history of their purchases
* remember whether they've authenticated as a member
* stores their shopping cart indefinitely, and across browsers and computers

Sessions
--------

A session is the period when the site will remember information about the
person's visit in a particular browser. For example, if the person logs in,
they'll stay logged in until the session expires; if they don't log in, their
shopping cart will only last until the session expires.

Sessions for the site will last 24 hours from the last interaction with
the site in a browser, or until the browser is closed.  After either of those
events, the user will have to log in again, or will see an empty cart again.

Public
------

The public is anyone who visits the site. No special authentication
is needed to view and use the site as a public customer.

Products
~~~~~~~~

Here are the kinds of products we sell to the public:

* Event tickets

 Tickets can come in variants, mainly different dates for performances, and different
 kinds of attendees - general vs. student.

 We might someday have to limit the number we sell (based on available seats), but that's not
 really an issue so far.

* Donations

 Opportunities to donate always have an indicated purpose (general use is always
 offered), and might have a pre-determined amount or let the user specify.
 E.g. maybe it costs $300 to sponsor an orchestra member for the Spring 2013 concert, or
 someone could donate some money toward member scholarships.

* Ads?

 Some day we might want to sell/accept payment for ads on the site.

* Pecans

 Same?

* Raffle tickets

 Like event tickets, only already have a strict max number sold, and we need to be sure to
 identify each ticket sold uniquely and who bought it. We would probably need to set aside
 some tickets and enter their numbers into the site as the raffle tickets available to
 be sold, and tell buyers specifically which ticket #'s they bought.

Front page
~~~~~~~~~~

The front page lists all the products currently for sale.

Each product listed has a link to a page for that particular product.

On that page, the user can customize the product if relevant - e.g.
pick a performance date and an attendee type - then specify a quantity
and add the product to their cart.  Adding the product to their cart
takes them to the cart.

Shopping Cart
~~~~~~~~~~~~~

Every page, in the header, displays a count of the number of products
in the cart and a link to the shopping cart.

On the shopping cart page, a list is shown of the products that the
user has added to the cart.  Each product name is a link to the product's
page. Quantities are editable fields, with an "update quantities" button
at the bottom of that column.  The total cost is shown.

If the user comes to the shopping cart page by adding a product to
the cart, a message at the top of the page will tell them that has
happened, and give them three links: return to the <product> page,
continue shopping (goes to home page), or check out.

If the user comes to the shopping cart page some other way, there
will be two links: continue shopping (goes to home page), or check out.

Clicking Check Out from the shopping cart page will go to the start of
the check out process.

Check Out Summary Page
~~~~~~~~~~~~~~~~~~~~~~

The first page in the check out process is the summary page.

The check out page will list the products in the cart, but no longer
in an editable format. A link will be provided to go back to the
cart or to the front page.

If the user is not logged in, three options will be provided:

* Log in before continuing - returns here after logging in
* Create an account - returns here after registering AND validating email
* Enter payment info without an account

If the user is logged in, only one option is provided, to enter
payment info.

Payment Info Popup
~~~~~~~~~~~~~~~~~~

This is not a separate page, but is a optional step in the process.

If the user is not logged in, or has not stored payment info in their
account, then when the user clicks to enter payment info, a popup will
ask for their email and credit card data.

Upon submitting the popup data, or if they stored payment info, immediately
when they click the button on the checkout summary page, they go to
the final confirmation page.

Final confirmation page
~~~~~~~~~~~~~~~~~~~~~~~
`
Once more, lists the items to be purchased, and the total.

Shows a summary of how the payment is to be made - email address, last
4 of credit card, that kind of thing.

Has a big button to say "Yes, I'm sure, charge my card for this purchase."

Has opt-out links to go back to the cart or the front page.

Post-payment page
~~~~~~~~~~~~~~~~~

Shows what happened - typically, your card has successfully been charged $x.yy
on xxx yy, zzzz at hh:mm for x, y, and z. Includes some kind of transaction
identifier.  Also tells the user that this same info has been emailed to
xxxx@example.com.

Email
~~~~~

The user receives an email at the email address they gave, with the same
info as the post-payment page.

Members
-------

Members will be instructed to click the "Members" link at the top of the
page in the store. When they do, they'll be asked to enter the member
password, which is given out at the first rehearsal. Having done that,
additional products might become visible for the rest of the session.

If someone who has entered the member password during the current session
is logged in, or logs in, or registers, their account will be flagged as
belonging to a member, and thereafter, any time they login, they'll be
treated as a member.

The only difference between using the site as public or as a member is
that members can see and buy more products.

Member Products
~~~~~~~~~~~~~~~

There are some additional product types that can be available to
members.

* Pay dues and music
* Buy concert recordings
* Buy black concert folders

There might also be member-specific products of the same types offered
to the public, e.g. tickets for member-only events. and of course, the
products offered to the public continue to be visible to members.

Common Page Layout
------------------

Header
~~~~~~

left-to-right:

* Voices Store - title and/or logo, links to front page
* rubber space
* Shopping cart
  * cart icon
  * N items
  * links to the shopping cart page
* Members
  * only appears if the user is not known to be a member yet
  * links to page to enter member password, or login or register
* Member
  * appears if user is known to be a member
  * not a link to anything
* Log in/register
  * Appears if user not logged in
  * Goes to page to log in or register (duh!)
* My account
  * Appears if user is logged in
  * Is a dropdown menu with
    * Log out
    * Edit profile information

Footer
~~~~~~

* Voices - link to main site front page
* About - link to a page briefly describing the purpose of the store site
* copyright
* contact us - link to a contact us page
