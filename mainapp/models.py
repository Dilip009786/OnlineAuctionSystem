from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# User Profile model linked to Django's User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=15)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Category for products
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    def __str__(self):
        return self.title


# Product model
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    askingprice = models.DecimalField(max_digits=10, decimal_places=2)
    expirytime = models.DateTimeField()
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    status_choices = [('sold', 'Sold'), ('deactivated', 'Deactivated'), ('available', 'Available')]
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    def __str__(self):
        return self.name

    def is_expired(self):
        """Check if the product's auction time has expired."""
        return self.expirytime <= timezone.now()

    def process_auction(self):
        """Process auction after expiry and create an order for the highest bidder."""
        if self.is_expired() and self.status == 'available':
            # Get the highest bid on this product
            highest_bid = Bidding.objects.filter(product=self).order_by('-bidamount').first()
            if highest_bid:
                # Create an order for the highest bidder
                order = Order.objects.create(
                    bidding=highest_bid,
                    seller=self.seller,
                    bidder=highest_bid.bidder,
                    winprice=highest_bid.bidamount,
                    orderstatus='Pending Delivery'
                )
                # Mark product as sold
                self.status = 'sold'
                self.save()
                return order
        return None


# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Ensures each user can wishlist a product only once

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"


# Bidding model
class Bidding(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_bids')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder_bids')
    bidamount = models.DecimalField(max_digits=10, decimal_places=2)
    bidtime = models.DateTimeField(auto_now_add=True)
    status_choices = [('win', 'Win'), ('loss', 'Loss'), ('wait' , 'Wait')]
    status = models.CharField(max_length=10, choices=status_choices, default='wait')

    def __str__(self):
        return f"{self.bidder.username} bid on {self.product.name} for {self.bidamount}"

    def clean(self):
        if self.bidamount <= self.product.askingprice:
            raise ValidationError(f"The bid amount must be greater than the asking price of {self.product.askingprice}.")


# Order model
class Order(models.Model):
    bidding = models.ForeignKey(Bidding, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller_orders', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name='bidder_orders', on_delete=models.CASCADE)
    winprice = models.DecimalField(max_digits=10, decimal_places=2)
    orderstatus = models.CharField(max_length=20)
    deliveryperson = models.ForeignKey('DeliveryPerson', null=True, on_delete=models.SET_NULL)
    deliverycontact = models.CharField(max_length=15, blank=True)
    deliverytime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.productname()}"

    # Optionally, add a method to get the product name
    def productname(self):
        return self.bidding.product.name if self.bidding.product else "Unknown Product"


# DeliveryPerson model
class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"Delivery Person: {self.user.username}"


class BiddingHistory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='bidding_histories')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidding_histories')
    bidamount = models.DecimalField(max_digits=10, decimal_places=2)
    bidtime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-bidtime']  # Orders by most recent bids first
        verbose_name = "Bidding History"
        verbose_name_plural = "Bidding Histories"

    def __str__(self):
        return f"Bidder: {self.bidder.username} | Product: {self.product.name} | Amount: {self.bidamount}"