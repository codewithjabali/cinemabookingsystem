from django.shortcuts import render, redirect
from .models import Customer, Booking, Production
from django.contrib import messages
from django.core.mail import send_mail



def home(request):
    return render(request, "index.html")


# Register
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")
        password = request.POST.get("password")

        if not all([first_name, last_name, email, phone, address, city, zip_code, password]):
            return redirect("home")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists please login!")
            return redirect("home")

        Customer.objects.create(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone, address=address,
            city=city, zip_code=zip_code, password=password
        )
        send_mail(
            subject="Welcome to Gold Cinema Company",
            message=f"Hi {first_name}, thank you for registering at Gold Cinema Company. You can now book your tickets and enjoy our services.",
            from_email="Golden Cinema Company <jabaliamunga@gmail.com>",
            recipient_list=[email],
            fail_silently=False,
            
        )
        
        return redirect("index")

    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not all([email, password]):
            return redirect("home")
        if Customer.objects.filter(email=email, password=password).exists():
                   
            return redirect("index")
        messages.error(request, "Invalid login credentials, recreate the account, check email or password or contact admin +254 112770449 to be asigned an advisor")
        return redirect("home")
    return render(request, "index.html")
        
def index(request):
    return render(request, "account.html")    

def booking_view(request):
    if request.method == "POST":
        customer_email = request.POST.get("email")
        advisor = request.POST.get("advisor")
        production_name = request.POST.get("production_name")
        production_type = request.POST.get("production_type")
        seat_preference = request.POST.get("seat_preference")

        if not all([customer_email, production_name, production_type, seat_preference]):
            messages.error(request, "All fields are required!")
            return redirect("index")

        if not Customer.objects.filter(email=customer_email).exists():
            messages.error(request, "Email does not exist, please create an account first!")
            return redirect("home")

        if Booking.objects.filter(
            customer_email=customer_email,
            production_name=production_name,
            seat_preference=seat_preference
        ).exists():
            messages.error(request, "You have already booked this production with the same seat preference!")
            return redirect("index")

        Booking.objects.create(
            customer_email=customer_email,
            advisor=advisor,
            production_name=production_name,
            production_type=production_type,
            seat_preference=seat_preference
        )

        # Use console backend first during testing
        send_mail(
            subject="Booking Confirmation - Gold Cinema",
            message=f"Hi! Your booking for '{production_name}' ({production_type}) with seat '{seat_preference}' has been received. Thank you for choosing Gold Cinema!",
            from_email="Gold Cinema <jabaliamunga@gmail.com>",
            recipient_list=[customer_email],
            fail_silently=True,  # prevent server error during tests
        )

        messages.success(request, "Booking successful! Check your email for confirmation.")
        return redirect("index")

    return render(request, "account.html")

def daily_reminder():
    users = Customer.objects.all()
    for user in users:
        send_mail(
            "Daily Reminder",
            "This is your daily update from Sister Michaela Portal.",
            None,
            [user.email],

        )

