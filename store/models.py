from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
import stripe

#
# class ProductGroup(models.Model):
#     """A group of products with some settings in common"""
#     name = models.CharField(max_length=128,
#                             help_text="name of the product group (displayed on web page). "
#                                       "Should uniquely identify the group for all time. E.g. "
#                                       "Tickets for Fall 2013 Voices Concert")
#     description = models.TextField(
#         blank=True,
#         help_text="More description of the product group."
#     )
#     url = models.URLField(
#         blank=True,
#         help_text="Link for more information about this product group. Optional."
#     )
#     to_notify = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         help_text="Users to notify when sales occur and with period reports"
#     )
#     display_start = models.DateTimeField(
#         help_text="Products will not be displayed before this time"
#     )
#     display_end = models.DateTimeField(
#         blank=True, null=True,
#         help_text="Products will not be displayed after this time"
#     )
#
#     public = models.BooleanField(
#         help_text="Whether to display products to the public"
#     )
#     members = models.BooleanField(
#         help_text="Whether to display products to members"
#     )
#
#     donation = models.BooleanField(
#         default=False,
#         help_text="True if this group contains donations instead of normal products. "
#                   "We model those as products with a price of 0.01. "
#                   "(We don't display them that way on the site, obviously)"
#     )
#
#     def __str__(self):
#         return self.name
#
#     def quantity_sold(self):
#         if self.donation:
#             return self.total_sales()
#         return sum([itemsale.quantity
#                     for itemsale in ItemSale.objects.filter(product__group=self,
#                                                             sale__complete=True)])
#
#     def total_sales(self):
#         return sum([itemsale.amount()
#                     for itemsale in ItemSale.objects.filter(product__group=self,
#                                                             sale__complete=True)])


class Product(models.Model):
    """
    One product item to sell.  E.g. '2013 voices t-shirt, small' or
    'Ticket for 2013 Dec. 14 8pm concert, general admission'
    """
    PRICE_ONE = 1
    PRICE_MULTIPLE = 2
    PRICE_USER = 3
    PRICE_STRATEGY_CHOICES = (
        (PRICE_ONE, "One price - Enter one price in Prices. Price name is ignored."),
        (PRICE_MULTIPLE, "Multiple - user has choices, enter multiple in Prices, which see."),
        (PRICE_USER, "User entered - user can enter a price. Used for donations."),
    )

    name = models.CharField(
        max_length=40,
        help_text="""A one-line (40 chars or less) text string uniquely identifying the product.
        Example: May 2013 Cantari Concert Ticket""",
        unique=True,
    )
    blurb = models.CharField(
        max_length=128,
        help_text="A phrase (no more than two lines) that is included in product "
                  "listings to describe the product a little more than the name.",
    )
    description = models.TextField(
        blank=True,
        help_text="A complete description of the product, used on the product page. Can "
                  "be multiple paragraphs if necessary. Optional."
    )
    draft = models.BooleanField(
        default=True,
        help_text=""" A product in draft mode is displayed only to logged-in staff members, and
    ignores the product sell dates. It is clearly marked "DRAFT" anywhere it
    appears on the site. It cannot really be bought; a cart with draft products
    in it will refuse to check out.""",
    )
    sell_start = models.DateTimeField(
        blank=True,
        null=True,
        help_text="""The date/times between which the product is shown on the site and can be purchased.
    Both dates are optional, indicating no restriction on that end of the sell period.""",
    )
    sell_stop = models.DateTimeField(
        blank=True,
        null=True,
        help_text="""The date/times between which the product is shown on the site and can be purchased.
    Both dates are optional, indicating no restriction on that end of the sell period.""",
    )
    member_only = models.BooleanField(
        default=False,
        help_text="""A member-only product is only displayed to those who are members.""",
    )
    pricing = models.PositiveSmallIntegerField(
        choices=PRICE_STRATEGY_CHOICES,
        default=PRICE_ONE,
        help_text="How this item is priced"
    )
    prices = models.ManyToManyField('store.Price')
    special_instructions_prompt = models.TextField(
        blank=True,
        help_text="""(optional) This is an optional text field. If text is entered here for a product, then
    during checkout, under this product in the list of purchases, this text will be
    displayed as a prompt, along with a text field that the user will be required to
    enter something into.

    What is this for? For example, on a member dues product, you could add special
    instructions "Who is this dues payment for" to force the purchaser to name the
    chorus member they're paying dues for. This is because commonly one person might
    pay dues for themself and their partner.""",
    )
    quantifiable = models.BooleanField(
        default=True,
        help_text="""(default True) if False, user will not be allowed to enter a quantity for this
    product, but may add it to their cart multiple times.  If true, we might some day
    implement merging items in the cart that have all the same options... but no
    hurry on that.

    This is also intended to cope with people paying dues, to force them to enter
    a separate name for each dues payment.""",
    )
    account = models.ForeignKey(
        'accounting.Account',
    )
    klass = models.ForeignKey(
        'accounting.Klass',
        verbose_name='class',
    )

    def __str__(self):
        return self.name


class Price(models.Model):
    name = models.CharField(
        max_length=80,
        help_text="If product has multiple prices, the name field must identify which price "
                  "the user should pick.  E.g. 'General Admission' or 'Student'",
    )
    amount = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return "%s - %s" % (self.name, self.amount)
