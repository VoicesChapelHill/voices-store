from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
import stripe


class ProductGroup(models.Model):
    """A group of products with some settings in common"""
    name = models.CharField(max_length=128,
                            help_text="name of the product group (displayed on web page)")
    to_notify = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text="Users to notify when sales occur and with period reports"
    )
    display_start = models.DateTimeField(
        help_text="Products will not be displayed before this time"
    )
    display_end = models.DateTimeField(
        help_text="Products will not be displayed after this time"
    )

    public = models.BooleanField(
        help_text="Whether to display products to the public"
    )
    members = models.BooleanField(
        help_text="Whether to display products to members"
    )

    donation = models.BooleanField(
        default=False,
        help_text="True if this group contains donations instead of normal products. "
                  "We model those as products with a price of 0.01. "
                  "(We don't display them that way on the site, obviously)"
    )

    def __str__(self):
        return self.name

    def quantity_sold(self):
        if self.donation:
            return self.total_sales()
        return sum([itemsale.quantity
                    for itemsale in ItemSale.objects.filter(product__group=self,
                                                            sale__complete=True)])


    def total_sales(self):
        return sum([itemsale.amount()
                    for itemsale in ItemSale.objects.filter(product__group=self,
                                                            sale__complete=True)])


class Product(models.Model):
    """
    One product item to sell.  E.g. '2013 voices t-shirt, small' or
    'Ticket for 2013 Dec. 14 8pm concert, general admission'
    """

    name1 = models.CharField(
        max_length=128,
        help_text="Part of the product name that could be common across variations, e.g. '2013 T-shirt'")
    name2 = models.CharField(
        max_length=128,
        help_text="Part of the product name that could vary, e.g. 'Small' (can be blank)",
        blank=True,
    )
    price = models.DecimalField(decimal_places=2, max_digits=6,
                                help_text="Price in dollars for one of this product currently.")
    description = models.TextField(
        blank=True
    )
    group = models.ForeignKey(ProductGroup, related_name='products')

    def __str__(self):
        return "%s/%s" % (self.name1, self.name2) if self.name2 else self.name1

    def completed_sales(self):
        return ItemSale.objects.filter(product=self, sale__complete=True)

    def total_quantity(self):
        if self.group.donation:
            pass
        else:
            return sum([itemsale.quantity for itemsale in self.completed_sales()])

    def total_amount(self):
        return sum([itemsale.amount() for itemsale in self.completed_sales()])


class Customer(models.Model):
    """
    Information about a customer associated with a sale. Not sure yet what will
    go here. We might have a separate one for each sale.
    """
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Sale(models.Model):
    """
    A purchase of one or more items, charged as the total cost in one payment
    """
    when = models.DateTimeField(default=lambda: now())
    who = models.ForeignKey(Customer, null=True)  # don't know until later in process
    comments = models.TextField(
        blank=True,
        help_text="Any comments the customer submitted as part of the sale")
    complete = models.BooleanField(default=False)
    charge_id = models.CharField(blank=True, max_length=40,
                                 help_text="id of Stripe Charge object")

    def kinds_of_things(self):
        product_groups = ProductGroup.objects.filter(products__itemsales__sale=self)
        s = ', '.join(pg.name for pg in product_groups)
        return s

    def __str__(self):
        return "%s on %s ($%s; %s)[%s]" % (self.who, self.when, self.total(), self.kinds_of_things(), self.charge_id)

    def total(self):
        return sum([i.amount() for i in self.items.all()])

    def emails_to_notify(self):
        """Return the email addresses that should be notified about this sale"""
        emails = set()
        for item in self.items.all():
            for user in item.product.group.to_notify.all():
                emails.add(user.email)
        return emails

    @property
    def charge(self):
        """
        Return the Strip Charge object for this sale
        This requires an API call to Stripe so don't call it trivially
        """
        # We cache it the first time we look it up, in case we're referring to
        # this repeatedly in a template
        if hasattr(self, '_charge'):
            return getattr(self, '_charge')
        if not self.charge_id:
            return None
        stripe.api_key = settings.STRIPE_SECRET_KEY
        setattr(self, '_charge', stripe.Charge.retrieve(self.charge_id, expand=['card']))
        return getattr(self, '_charge')


class ItemSale(models.Model):
    """
    A purchase of one or more of a particular product, associated with a Sale.
    """
    product = models.ForeignKey(Product, related_name='itemsales')
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    sale = models.ForeignKey(Sale, related_name='items')
    per_item_price = models.DecimalField(decimal_places=2, max_digits=6,
                                         help_text="Price in dollars for one of this product at the time of this sale")

    def __str__(self):
        if self.product.group.donation:
            return "$%s %s" % (self.amount(), self.product)
        else:
            return "%d of %s" % (self.quantity, self.product)

    def amount(self):
        return self.quantity * self.per_item_price
