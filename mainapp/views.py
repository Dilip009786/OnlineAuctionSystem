from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateformat import DateFormat
from .models import Category, Product, Wishlist, Bidding, DeliveryPerson, Order, UserProfile, BiddingHistory
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import csv
import io
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password


# View for testing
def user_list(request):
    users = User.objects.all()  # Retrieve all users
    userprofiles = UserProfile.objects.all()  # Retrieve all user profiles

    # Determine which data to pass to the template
    if userprofiles.exists():
        context = {'users': users, 'userprofiles': userprofiles}
    else:
        context = {'users': users}

    return render(request, 'admin/display-user.html', context)


def user_profile(request):
    try:
        # Check if the user already has a profile
        user_profile = UserProfile.objects.get(user=request.user)
        
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        # If profile exists, update it; otherwise, create a new one
        if user_profile:
            user_profile.phoneno = request.POST.get('phoneno')
            user_profile.address = request.POST.get('address')
            if 'photo' in request.FILES:  # Handle profile photo if uploaded
                user_profile.photo = request.FILES['photo']
            user_profile.save()
        else:
            # Create a new profile for the user
            UserProfile.objects.create(
                user=request.user,
                phoneno=request.POST.get('phoneno'),
                address=request.POST.get('address'),
                profile_photo=request.FILES.get('photo')  # Optional photo field
            )
        return redirect('profile')  # Redirect to the profile view after saving

    if request.GET.get('edit'):
        # If edit is clicked, pass an empty profile or the existing one to the template
        context: dict[str, UserProfile | None] = {
            'user_profile': user_profile,
        }
        return render(request, 'admin/profile.html', context)  # Render the edit profile page

    if user_profile:
        # Render the template for users with a profile
        template = 'admin/profile.html'
    else:
        # Render the template for users without a profile
        template = 'admin/profile.html'

    context = {
        'user_profile': user_profile,  # Pass the user profile to the template
    }
    
    return render(request, template, context)


def dpuser_profile(request):
    try:
        # Check if the user already has a profile
        user_profile = UserProfile.objects.get(user=request.user)
        
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        # If profile exists, update it; otherwise, create a new one
        if user_profile:
            user_profile.phoneno = request.POST.get('phoneno')
            user_profile.address = request.POST.get('address')
            if 'photo' in request.FILES:  # Handle profile photo if uploaded
                user_profile.photo = request.FILES['photo']
            user_profile.save()
        else:
            # Create a new profile for the user
            UserProfile.objects.create(
                user=request.user,
                phoneno=request.POST.get('phoneno'),
                address=request.POST.get('address'),
                profile_photo=request.FILES.get('photo')  # Optional photo field
            )
        return redirect('dpprofile')  # Redirect to the profile view after saving

    if request.GET.get('edit'):
        # If edit is clicked, pass an empty profile or the existing one to the template
        context = {
            'user_profile': user_profile,
        }
        return render(request, 'deliveryperson/profile.html', context)  # Render the edit profile page

    if user_profile:
        # Render the template for users with a profile
        template = 'deliveryperson/profile.html'
    else:
        # Render the template for users without a profile
        template = 'deliveryperson/profile.html'

    context = {
        'user_profile': user_profile,  # Pass the user profile to the template
    }
    
    return render(request, template, context)


def test_view(request):
    return render(request, 'user/user-bids.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find the user by email
            user = User.objects.get(email=email)

            # Authenticate user by username and password
            user = authenticate(username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                request.session['email'] = user.email

                if user.is_superuser:
                    return redirect('dashboard')  # Redirect to dashboard for superusers
                elif user.is_staff:
                    return redirect('deliverydashboard')  # Redirect to a staff-specific dashboard
                else:
                    subject = 'Login Notification'
                    html_message = render_to_string('admin/login_email.html', {'user': user})  # Create an HTML template for the email
                    plain_message = strip_tags(html_message)  # This will strip the HTML tags
                    from_email = 'your_email@gmail.com'  # Replace with your email
                    to_email = user.email  # Assuming the User model has an email field

                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                    return redirect('home')  # Redirect to the home page for regular users
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'admin/auth-login.html')

        except User.DoesNotExist:
            messages.error(request, 'No account found with this email')
            return render(request, 'admin/auth-login.html')

    return render(request, 'admin/auth-login.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the email exists
        try:
            user = User.objects.get(email=email)

            # Check if the passwords match
            if password == confirm_password:
                # Encrypt the new password and save
                user.password = make_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')  # Redirect to login page after reset
            else:
                messages.error(request, 'Passwords do not match.')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')

    return render(request, 'admin/reset_password.html')


# Registration form view
def registration(request):
    return render(request, 'admin/auth-register.html')


# Home view
def dashboard(request):
    if request.user.is_authenticated:
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
    else:
        context = {}
    return render(request, 'admin/home.html', context)


# Logout view
def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('login')


# Registration processing logic
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('registration')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Log the user in after successful registration
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('registration')

    return render(request, 'registration/register.html')


def add_or_edit_category(request, category_id=None):
    if category_id:  # Editing an existing category
        category = get_object_or_404(Category, id=category_id)
    else:  # Adding a new category
        category = None

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description', '')

        if category:  # Update existing category
            category.title = title
            if image:  # Update image only if a new one is provided
                category.image = image
            category.description = description
            category.save()
            messages.success(request, 'Category updated successfully!')
        else:  # Create a new category
            Category.objects.create(title=title, image=image, description=description)
            messages.success(request, 'Category added successfully!')

        return redirect('display_category')  # Redirect to category display view

    context = {
        'category': category
    }
    return render(request, 'admin/add-category.html', context)


def display_category(request):
    categories = Category.objects.all()
    return render(request, 'admin/display-category.html', {'categories': categories})


def add_edit_product(request, product_id=None):
    # Check if editing or adding a product
    product = get_object_or_404(Product, id=product_id) if product_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        askingprice = request.POST.get('askingprice')
        expirytime = request.POST.get('expirytime')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        status = request.POST.get('status', 'available')

        # If editing, update the existing product
        if product:
            product.name = name
            product.description = description
            product.category_id = category_id
            product.askingprice = askingprice
            product.expirytime = expirytime
            product.status = status
            if image1:
                product.image1 = image1
            if image2:
                product.image2 = image2
            if image3:
                product.image3 = image3
            product.save()
            return redirect('display_product')
        
        # Otherwise, create a new product
        else:
            product = Product(
                seller=request.user,
                name=name,
                description=description,
                category_id=category_id,
                askingprice=askingprice,
                expirytime=expirytime,
                image1=image1,
                image2=image2,
                image3=image3,
                status=status
            )
            product.save()
            return redirect('display_product')
    
    # Fetch categories and render the form with product data if editing
    categories = Category.objects.all()
    return render(request, 'admin/add-product.html', {
        'product': product,
        'categories': categories,
    })


def display_product(request):
    products = Product.objects.all()
    return render(request, 'admin/display-product.html', {'products': products})


def admin_wishlist(request):
    user_wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'admin/display-wishlist.html', {'wishlist': user_wishlist})


def add_to_wishlist(request, product_id):
    # Ensure user is logged in
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)

        # Check if product is already in the user's wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if created:
            # The item was added to the wishlist
            return redirect('wishlist')  # Redirect to the wishlist page or another page
        else:
            # The product is already in the wishlist
            return HttpResponse("Product already in wishlist.")
    else:
        # If the user is not authenticated, redirect to login page
        return redirect('login')


def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        # Remove the product from the wishlist if it exists
        Wishlist.objects.filter(user=request.user, product=product).delete()

        return redirect('wishlist')  # Redirect to the wishlist page after removal
    else:
        # Handle non-POST requests, like GET
        return redirect('home')  # Redirect to home or another appropriate page


def add_edit_bid(request, bid_id=None):
    # If `bid_id` is provided, we're editing an existing bid
    bid = get_object_or_404(Bidding, id=bid_id) if bid_id else None

    if request.method == 'POST':
        product_id = request.POST.get('product')
        bidder_id = request.POST.get('bidder')
        bidamount = request.POST.get('bidamount')

        if product_id and bidder_id and bidamount:
            product = get_object_or_404(Product, id=product_id)
            bidder = get_object_or_404(User, id=bidder_id)

            if bid:
                # Update existing bid
                bid.product = product
                bid.bidder = bidder
                bid.bidamount = bidamount
                bid.seller = product.seller
                bid.save()
                messages.success(request, 'Bid has been updated successfully!')
            else:
                # Create a new bid
                Bidding.objects.create(
                    product=product, 
                    bidder=bidder, 
                    bidamount=bidamount, 
                    seller=product.seller
                )
                messages.success(request, 'New bid has been created successfully!')

            return redirect('bidding_list')
        else:
            messages.error(request, 'Please fill in all required fields.')

    # Retrieve data for form dropdowns
    products = Product.objects.all()
    users = User.objects.all()

    return render(request, 'admin/add-bidding.html', {
        'products': products,
        'users': users,
        'bid': bid  # Pass bid instance if editing
    })


def bidding_list_view(request):
    bidding_list = Bidding.objects.all()  # Fetch all bidding entries
    return render(request, 'admin/display-bidding.html', {'bids': bidding_list})


def change_bidding_status(request, bid_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        bidding = get_object_or_404(Bidding, id=bid_id)

        if new_status:
            # Change the status of the bidding
            bidding.status = new_status
            bidding.save()

        if new_status:
            # Change the status of the bidding
            bidding.status = new_status
            bidding.save()

            # Get the associated product
            product = bidding.product

            # Update the product status based on the bidding status
            if new_status == 'win':
                product.status = 'sold'
                messages.success(request, f'Bidding status changed to {new_status} and product status set to sold!')
            elif new_status in ['loss', 'wait']:
                # If the bidding is not won, ensure the product status is set to available
                product.status = 'available'
                messages.success(request, f'Bidding status changed to {new_status} and product is now available!')

            # Save the product's status changes
            product.save()
        else:
            messages.error(request, 'Invalid status selected.')

        return redirect('bidding_list')  # Redirect to the list page


def add_edit_deliveryperson(request, deliveryperson_id=None):
    delivery_person = None

    # Fetch existing delivery person if editing
    if deliveryperson_id:
        delivery_person = get_object_or_404(DeliveryPerson, id=deliveryperson_id)

    if request.method == 'POST':
        user_id = request.POST.get('user')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')
        user = User.objects.get(id=user_id)

        if delivery_person:
            # Update existing delivery person
            delivery_person.user = user
            delivery_person.phoneno = phoneno
            delivery_person.address = address
            delivery_person.save()
        else:
            # Create a new delivery person
            DeliveryPerson.objects.create(
                user=user,
                phoneno=phoneno,
                address=address
            )
        
        return redirect('display_deliveryperson')

    users = User.objects.all()
    return render(request, 'admin/add-deliveryperson.html', {
        'users': users,
        'delivery_person': delivery_person,
    })


def display_deliveryperson(request):
    delivery_people = DeliveryPerson.objects.all()

    return render(request, 'admin/display-deliveryperson.html', {'delivery_people': delivery_people})


def add_order(request):
    orders = Order.objects.filter(orderstatus='pending')  # Only show pending orders
    delivery_persons = DeliveryPerson.objects.all()

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        delivery_person_id = request.POST.get('delivery_person_id')

        if order_id and delivery_person_id:
            try:
                # Retrieve the order and delivery person
                order = Order.objects.get(id=order_id)
                delivery_person = DeliveryPerson.objects.get(id=delivery_person_id)

                # Assign the delivery person to the order
                order.deliveryperson = delivery_person
                order.save()

                messages.success(request, "Delivery person assigned successfully!")
                return redirect('display_order')  # Replace with the correct URL name
            except Order.DoesNotExist:
                messages.error(request, "Order not found!")
            except DeliveryPerson.DoesNotExist:
                messages.error(request, "Delivery person not found!")
        else:
            messages.error(request, "Both fields are required!")

    return render(request, 'admin/add-order.html', {'orders': orders, 'delivery_persons': delivery_persons})


def display_order(request):
    orders = Order.objects.all()
    return render(request, 'admin/display-order.html', {'orders': orders})


def delete_object(request, model_name, object_id):
    # Dynamically get the model based on the provided model_name
    model = ContentType.objects.get(model=model_name).model_class()
    
    # Fetch the object, or return a 404 if not found
    obj = get_object_or_404(model, id=object_id)
    
    if request.method == "POST":
        obj.delete()
        # Redirect to a success page or list page for the model
        return redirect('home')

    return render(request, 'admin/confirm_delete.html', {'object': obj})


# User Side

def user_profile_view(request):
    try:
        # Check if the user already has a profile
        user_profile = UserProfile.objects.get(user=request.user)
        
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        # If profile exists, update it; otherwise, create a new one
        if user_profile:
            user_profile.phoneno = request.POST.get('phoneno')
            user_profile.address = request.POST.get('address')
            if 'photo' in request.FILES:  # Handle profile photo if uploaded
                user_profile.photo = request.FILES['photo']
            user_profile.save()
        else:
            # Create a new profile for the user
            UserProfile.objects.create(
                user=request.user,
                phoneno=request.POST.get('phoneno'),
                address=request.POST.get('address'),
                profile_photo=request.FILES.get('photo')  # Optional photo field
            )
        return redirect('user_profile')  # Redirect to the profile view after saving

    if request.GET.get('edit'):
        # If edit is clicked, pass an empty profile or the existing one to the template
        context = {
            'user_profile': user_profile,
        }
        return render(request, 'user/edit-profile.html', context)  # Render the edit profile page

    if user_profile:
        # Render the template for users with a profile
        template = 'user/user-profile.html'
    else:
        # Render the template for users without a profile
        template = 'user/edit-profile.html'

    context = {
        'user_profile': user_profile,  # Pass the user profile to the template
    }
    
    return render(request, template, context)


def home(request):
    if request.user.is_authenticated:
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
    else:
        context = {}

    products = Product.objects.all()
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product', flat=True)
    else:
        wishlist_products = []

    context = {
        'products': products,
        'user': request.user,  # To use in the template to check authenticated user
        'wishlist_products': wishlist_products,  # List of products in the user's wishlist
    }
    return render(request, 'user/index.html', context)


def all_auction(request):
    products = Product.objects.filter(status='available').order_by('-expirytime')
    return render(request, 'user/auction-grid.html', {'products': products})


def wishlist(request):
    wishlisted_products = Product.objects.filter(wishlist__user=request.user)

    context = {
        'products': wishlisted_products
    }
    return render(request, 'user/wishlist-grid.html', context)


def auction_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bids = Bidding.objects.filter(product=product)
    bidding_histories = BiddingHistory.objects.filter(product=product)

    # Get the updated bids after processing
    bids = Bidding.objects.filter(product=product)
    
    context = {
        'product': product,
        'bids': bids,
        'bidding_histories': bidding_histories,  # Pass bidding history to the template
    }
    return render(request, 'user/auction-details.html', context)


def place_bid(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        bid_amount = request.POST.get('bidamount')

        # Validate the bid amount
        if bid_amount and float(bid_amount) > product.askingprice:
            # Create a new bid
            Bidding.objects.create(
                seller=product.seller,
                product=product,
                bidder=request.user,
                bidamount=bid_amount,
                status='loss'
            )

            # Update the asking price of the product
            product.askingprice = float(bid_amount)
            product.save()

            # Create a bidding history record
            BiddingHistory.objects.create(
                product=product,
                bidder=request.user,
                bidamount=bid_amount
            )

            # Redirect to the bids page
            return redirect('bids')  # Replace 'bids' with the appropriate URL name
        else:
            # Handle invalid bid amount
            error_message = "Bid amount must be greater than the current asking price."
            return render(request, 'user/auction-details.html', {'product': product, 'error_message': error_message})

    return render(request, 'user/auction-details.html', {'product': product})



def user_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        askingprice = request.POST.get('askingprice')
        expirytime = request.POST.get('expirytime')
        
        # Handle images
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        
        # Create and save the product
        if name and description and category_id and askingprice and expirytime:
            product = Product(
                seller=request.user,  # Assuming the seller is the currently logged-in user
                name=name,
                description=description,
                category_id=category_id,
                askingprice=askingprice,
                expirytime=expirytime,
                image1=image1,
                image2=image2,
                image3=image3
            )
            product.save()
            return redirect('home')  # Redirect after successful submission
        else:
            return render(request, 'user/add-product.html', {'error': 'Please fill in all fields.'})
    categories = Category.objects.all()
    return render(request, 'user/add-product.html', {'categories': categories})


def user_watch_product(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        products = Product.objects.filter(seller=request.user)
        return render(request, 'user/user-product.html', {'products': products})
    else:
        return redirect('login')


def bids(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve bids made by the logged-in user
        bids = Bidding.objects.filter(bidder=request.user)

        return render(request, 'user/user-bids.html', {'bids': bids})
    else:
        # Optionally redirect to login or return an error message
        return render(request, 'user/user-bids.html', {'error_message': 'You need to be logged in to view your bids.'})


def order_create(request, bid_id):
    # Fetch the winning bid
    bidding = get_object_or_404(Bidding, id=bid_id, status='win')

    # Only proceed if the request is POST, indicating the user clicked 'Order'
    if request.method == 'POST':
        # Create an order with fields that the admin can later update
        order = Order.objects.create(
            bidding=bidding,
            seller=bidding.seller,
            bidder=request.user,
            winprice=bidding.bidamount,
            orderstatus='pending',  # Initial status for admin to update
            deliveryperson=None,  # Admin assigns later
            deliverycontact='',    # Admin assigns later
            deliverytime=None      # Admin assigns later
        )
        order.save()
        return redirect('home')  # Redirect to a success page

    # Render the bidding page if not POST
    return redirect('bids')  # Replace with the URL name for the bids page


def user_order(request):
    orders = Order.objects.filter(bidder=request.user)
    return render(request, 'user/user-order.html', {'orders': orders})


# Delivery Person
def deliverydashboard(request):
    
    if request.user.is_authenticated:
        context = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'orders' : Order.objects.filter(deliveryperson=request.user.deliveryperson)
        }
    else:
        context = {}
    return render(request, 'deliveryperson/dashboard.html', context)


def order_delivery(request):
    # Assuming you want to filter orders based on the logged-in delivery person
    if request.user.is_authenticated and hasattr(request.user, 'deliveryperson'):
        orders = Order.objects.filter(deliveryperson=request.user.deliveryperson)
    else:
        orders = Order.objects.none()  # No orders if the user is not authenticated or not a delivery person

    return render(request, 'deliveryperson/display-order.html', {
        'orders': orders,
    })


def edit_order_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        orderstatus = request.POST.get('orderstatus')
        deliverytime = request.POST.get('deliverytime')

        # Update the order's status and delivery time
        if orderstatus:
            order.orderstatus = orderstatus

        if deliverytime:
            order.deliverytime = deliverytime

        # Save the changes to the order
        order.save()

        messages.success(request, f'Order {order.id} has been updated successfully!')
        return redirect('order_delivery')  # Redirect to the order list page

    # Render the edit order form
    return render(request, 'deliveryperson/edit-order.html', {
        'order': order,
    })


def generate_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html_content = render_to_string('admin/order_invoice.html', {'order': order})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF", status=500)


def upload_products(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('upload_products')
        
        # Read the CSV file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',')
        next(reader)  # Skip header row if there is one

        for row in reader:
            category = Category.objects.get(id=row[2])  # Assuming category ID is provided in the CSV
            Product.objects.update_or_create(
                name=row[0],
                defaults={
                    'seller': request.user,  # Assuming the current user is the seller
                    'description': row[1],
                    'category': category,
                    'askingprice': row[3],
                    'expirytime': row[4],  # Ensure the date format matches
                    'image1': row[5],  # Assuming you provide image paths or URLs in the CSV
                    'image2': row[6],
                    'image3': row[7],
                    'status': row[8]  # Status should also be provided
                }
            )
        
        messages.success(request, 'Products uploaded successfully!')
        return redirect('upload_products')

    return render(request, 'upload_products.html')


def download_products(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Category ID', 'Asking Price', 'Expiry Time', 'Image 1', 'Image 2', 'Image 3', 'Status'])

    products = Product.objects.all().values_list('name', 'description', 'category_id', 'askingprice', 'expirytime', 'image1', 'image2', 'image3', 'status')
    for product in products:
        writer.writerow(product)

    return response