from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout

from .decorators import *
from .models import *

# Create your views here.

def home(request):
    return render(request, 'bank_app/landing.html')

def about(request):
    return render(request, 'bank_app/about.html')

def contact(request):
    return render(request, 'bank_app/contact.html')

def services(request):
    return render(request, 'bank_app/services.html')

def onepage(request):
    return render(request, 'bank_app/one-page.html')

# LOGIN PAGE
@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # If profile incomplete → go to reset_setting
            if not user.userprofile.is_completed:
                return redirect('reset_setting')

            # Otherwise → dashboard
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'bank_app/login.html')
@login_required(login_url= 'LoginPage')
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'transaction': transaction,
        'currency': user_profile.currency,
        'current_balance': user_profile.balance,
    }
    return render(request, 'bank_app/transaction_detail.html', context)


# PROFILE COMPLETION PAGE
@login_required(login_url='LoginPage')
@transaction.atomic
def reset_setting(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_completed = True   # ✅ mark completed after save
            profile.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'bank_app/reset_setting.html', {'form': form})

@unauthenticated_user
def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create blank UserProfile for the new user
            UserProfile.objects.create(user=user, is_completed=False)

            # Auto-login after registration
            login(request, user)

            # Send user to profile completion page
            return redirect('reset_setting')

    return render(request, 'bank_app/register.html', {'form': form})

# DASHBOARD PAGE
@login_required(login_url='LoginPage')
def dashboard(request):
    user_profile = request.user.userprofile

    # Alert handling
    if not user_profile.is_linked:
        show_alert = request.session.get('show_alert', True)
        if show_alert:
            last_refresh_str = request.session.get('last_refresh', None)
            if last_refresh_str:
                last_refresh = timezone.datetime.fromisoformat(last_refresh_str)
            else:
                last_refresh = None

            if last_refresh is None or (timezone.now() - last_refresh) > timedelta(minutes=5):
                request.session['last_refresh'] = timezone.now().isoformat()
                request.session['show_alert'] = True
                alert_message = "Link account with the payment system for secure transfer"
            else:
                alert_message = None
        else:
            alert_message = None
    else:
        alert_message = None
        request.session['show_alert'] = False

    # Deposit form
    if request.method == 'POST':
        form = DepositForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            if not user_profile.is_linked:
                form.add_error(None, "Please link your account before making a deposit.")
            else:
                form.save()
                return redirect('imf')
    else:
        form = DepositForm(user_profile=user_profile)

    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10]

    context = {
        'user_profile': user_profile,
        'alert_message': alert_message,
        'form': form,
        'transactions': transactions,
    }
    return render(request, 'bank_app/dashboard.html', context)

@login_required(login_url='LoginPage')
def bank(request):
    user_profile = request.user.userprofile  # Retrieve user profile associated with the current user

    if request.method == 'POST':
        form = DepositForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            try:
                if not user_profile.is_linked:
                    form.add_error(None, "Please activate your account before making a deposit.")
                else:
                    deposit_amount = form.cleaned_data['deposit_amount']
                    if deposit_amount <= 0:
                        form.add_error('amount', "Deposit amount must be greater than zero.")
                    else:
                        # Create a transaction record without deducting the balance
                        Transaction.objects.create(
                            user=user_profile.user,
                            amount=deposit_amount,
                            balance_after=user_profile.balance,  # Balance remains unchanged
                            description='Pending'
                        )

                        return redirect('imf')  # Redirect to dashboard view after processing the deposit
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = DepositForm(user_profile=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'bank_app/bank.html', context)

@login_required(login_url='LoginPage')
def crypto(request):
    user_profile = request.user.userprofile  # Retrieve user profile associated with the current user

    if request.method == 'POST':
        form = DepositForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            try:
                if not user_profile.is_linked:
                    form.add_error(None, "Please activate your account before making a deposit.")
                else:
                    deposit_amount = form.cleaned_data['deposit_amount']
                    if deposit_amount <= 0:
                        form.add_error('amount', "Deposit amount must be greater than zero.")
                    else:
                        # Create a transaction record without deducting the balance
                        Transaction.objects.create(
                            user=user_profile.user,
                            amount=deposit_amount,
                            balance_after=user_profile.balance,  # Balance remains unchanged
                            description='Pending'
                        )

                        return redirect('imf')  # Redirect to dashboard view after processing the deposit
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = DepositForm(user_profile=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'bank_app/crypto.html', context)

@login_required(login_url='LoginPage')
def paypal(request):
    user_profile = request.user.userprofile  # Retrieve user profile associated with the current user

    if request.method == 'POST':
        form = DepositForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            try:
                if not user_profile.is_linked:
                    form.add_error(None, "Please activate your account before making a deposit.")
                else:
                    deposit_amount = form.cleaned_data['deposit_amount']
                    if deposit_amount <= 0:
                        form.add_error('amount', "Deposit amount must be greater than zero.")
                    else:
                        # Create a transaction record without deducting the balance
                        Transaction.objects.create(
                            user=user_profile.user,
                            amount=deposit_amount,
                            balance_after=user_profile.balance,  # Balance remains unchanged
                            description='Pending'
                        )

                        return redirect('imf')  # Redirect to dashboard view after processing the deposit
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = DepositForm(user_profile=user_profile)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'bank_app/paypal.html', context)

@login_required(login_url='LoginPage')
def Upgrade_Account(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    # Check if the account is upgraded
    if user_profile.is_upgraded:
        message = 'Account upgraded successfully'
    else:
        message = 'Account upgrade processing contact support for more information'

    context = {
        'user_profile': user_profile,
        'message': message,
    }
    return render(request, 'bank_app/account_upgrade.html', context)

@login_required(login_url='LoginPage')
def profile_setting(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/profile_settings.html', context)

@login_required(login_url='LoginPage')
def aml(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/aml.html')

@login_required(login_url='LoginPage')
def imf(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/imf.html')

@login_required(login_url='LoginPage')
def tac(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/tac.html')

@login_required(login_url='LoginPage')
def kyc(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/kyc.html', context)

@login_required(login_url='LoginPage')
def statistics(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/statistics.html', context)

@login_required(login_url='LoginPage')
def alert(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/alert.html', context)

@login_required(login_url='LoginPage')
def transaction_details(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/transaction_details.html')

@login_required(login_url='LoginPage')
def pending(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/pending.html')

@login_required(login_url='LoginPage')
def loans(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/loans.html', context)

@login_required(login_url='LoginPage')
@transaction.atomic
def linking_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = LinkingCodeForm(request.POST)
        if form.is_valid():
            # Check if the linking code matches
            entered_code = form.cleaned_data['linking_code']
            if entered_code == profile.linking_code:
                messages.success(request, 'Account successfully linked.')
                # Handle linking logic here, e.g., set a flag in UserProfile
                profile.is_linked = True
                profile.save()
                return redirect('dashboard')  # Redirect to dashboard or another view
            else:
                messages.error(request, 'Invalid linking code. Please try again.')
        else:
            messages.error(request, 'Form validation failed. Please check the input.')

    else:
        form = LinkingCodeForm()

    context = {
        'form': form,
        'user_profile': profile
    }
    return render(request, 'bank_app/linking_page.html', context)


@login_required(login_url='LoginPage')
def LogOut(request):
    logout(request)
    return redirect('LoginPage')