from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from portal.models import Users, UsersPay, UsersFb, FarmLevel, UsersFormscript
import hashlib
import datetime
import time
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.ipn.models import PayPalIPN

# this is custom python script code.
from custom_script.script1_testing import start

def index(request, should_login=False):
    return render(request, 'portal/index.html', {'should_login': should_login})

# importing farmlevel txt file
def import_farmlevel(request):

    try:
        # open file
        file = request.FILES['file']

        # iterating the lines of the file
        for line in file:

            line = line.strip()
            line = str(line, 'utf-8')
            print(line)
            if FarmLevel.objects.filter(level__exact=line.split(',')[0]):
                level = FarmLevel.objects.get(level__exact=line.split(',')[0])
                level.comment = line.split(',')[1]
                try:
                    if line.split(',')[2] is True or line.split(',')[2] is False:
                        level.hidden = line.split(',')[2]
                    else:
                        level.hidden = False
                except:
                    level.hidden = False

                try:
                    if line.split(',')[3] is 1 or line.split(',')[3] is 2:
                        level.raid = line.split(',')[3]
                    else:
                        level.raid = 0
                except:
                    level.raid = 0

                level.save()

            else:

                try:
                    if line.split(',')[2] is True or line.split(',')[2] is False:
                        hidden = line.split(',')[2]
                    else:
                        hidden = False
                except:
                    hidden = False

                try:
                    if line.split(',')[3] is 1 or line.split(',')[3] is 2:
                        raid = line.split(',')[3]
                    else:
                        raid = 0
                except:
                    raid = 0

                farm_level = FarmLevel(level=line.split(',')[0],
                          comment=line.split(',')[1],
                          hidden=hidden,
                          raid=raid)
                farm_level.save()

        print("Imported successfully !")
        return redirect('/admin/portal/farmlevel/')
    except:
        return redirect('/admin/portal/farmlevel/')


# if clicking profile button
def profile(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        user = Users.objects.get(id=user_id)
        return render(request, 'portal/profile/profile.html', {'user': user})
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)


# Returning JSON object FB List of specified user
def fblist(request):
    if "logged_in" in request.session:
        user_id = request.GET.get('user_id', None)
        user_fb = UsersFb.objects.filter(user_id=user_id)
        data = list(user_fb.values())
        return JsonResponse(data, safe=False)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# get fb_key from fb_id
def get_fb_key(request):
    if request.is_ajax():
        id = request.GET.get('id', None)
        data = {
            'is_taken': UsersFb.objects.filter(id__exact=id).exists()
        }
        if data['is_taken']:
            data['fb_key'] = UsersFb.objects.get(id__exact=id).fb_key
        return JsonResponse(data)

# checking if fb_id exists in db
def validate_fb(request):
    if request.is_ajax():
        user_id = request.GET.get('user_id', None)
        fb_id = request.GET.get('fb_id', None)
        data = {
            'is_taken': UsersFb.objects.filter(user_id__exact=user_id, fb_id__exact=fb_id).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'This FB ID already exists.'
        return JsonResponse(data)


# updating FB key of the specified user
def update_fb(request):
    if request.is_ajax():
        id = request.GET.get('id', None)
        fb_key = request.GET.get('fb_key', None)
        user_fb = UsersFb.objects.get(id=id)
        user_fb.fb_key = fb_key
        user_fb.save()

        data = {
            'is_updated': True
        }
        return JsonResponse(data)


# Add new FB ID & KEY to the specified user
def add_fb(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        fb_id = request.GET.get('fb_id', None)
        fb_key = request.GET.get('fb_key', None)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if UsersPay.objects.filter(user_id__exact=user_id):

            user_pay = UsersPay.objects.get(user_id__exact=user_id)
            if UsersFb.objects.filter(user_id__exact=user_id, pay_id__exact=user_pay.id).count() < 1:
                # if UsersFb.objects.filter(user_id__exact=user_id, pay_id__exact=user_pay.id).count() > 0:
                #     data = {
                #         'is_added': False,
                #         'error_message': "After using FB ID & KEY that have already added, </br>you can add other !"
                #     }
                # else:
                user_fb = UsersFb(user_id=user_id,
                                  pay_id=user_pay.id,
                                  fb_id=fb_id,
                                  fb_key=fb_key,
                                  created=now,
                                  used=False)
                user_fb.save()
                data = {
                    'is_added': True
                }
            else:
                data = {
                    'is_added': False,
                    'error_message': "You can add only one fb_id and fb_key !"
                }
        else:
            data = {
                'is_added': False,
                'error_message': "You should set the subscription !"
            }
        return JsonResponse(data)

    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

def tasks(request):
    if "logged_in" in request.session:
        try:
            user_formscript = UsersFormscript.objects.order_by('-id').filter(user_id__exact=request.session.get('user_id'))[0]
            fb_key = UsersFb.objects.get(id__exact=user_formscript.fb_id).fb_key
            fb_id = UsersFb.objects.get(id__exact=user_formscript.fb_id).fb_id
            level_comment = FarmLevel.objects.get(id__exact=user_formscript.level).comment
            return render(request, 'portal/form/start_form.html', {'script' : user_formscript,'fb_key' : fb_key,'fb_id' : fb_id,'comment' : level_comment})
        except:
            return render(request, 'portal/form/start_form.html')
    else:
    # if don't login, redirect to homepage and display login modal
        return index(request, True)

# start Portal Script Form#1
def start_form1(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        form_kind = 1
        fb_id = UsersFb.objects.get(user_id = user_id).id
        level = request.POST.get('form1_level')
        opt = request.POST.get('opt')
        if opt:
            option = opt
        else:
            option = 0
        checking = request.POST.get('checking')

        if checking:
            check = 1
        else:
            check = 0
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # updating used field of the specified in users_fb table
        user_fb = UsersFb.objects.get(id=fb_id)
        user_fb.used = True
        user_fb.save()



        # storing new record in users_formscript
        user_formscript = UsersFormscript(
            user_id = user_id,
            form_kind = form_kind,
            fb_id = fb_id,
            level = level,
            option = option,
            created = now,
            start = True,
            running=False)
        user_formscript.save()
        fb_key = request.POST.get('form1_fb_key')
        fb_id = UsersFb.objects.get(id = fb_id).fb_id
        level_comment = FarmLevel.objects.get(id__exact=level).comment

        # -----------------------------------
        # return render(request, 'portal/form/start_form1.html', {'script' : user_formscript,'fb_key' : fb_key,'fb_id' : fb_id,'comment' : level_comment,'results':return_result['ACTIVE_PARTY'].items()})
        return render(request, 'portal/form/start_form.html', {'script' : user_formscript,'fb_key' : fb_key,'fb_id' : fb_id,'comment' : level_comment})
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# run custom script and return the json result
def running_result_form1(request):
    if "logged_in" in request.session and request.is_ajax():

        if UsersFormscript.objects.filter(id=request.GET.get('id', None),start__exact=True).exists():
            fb_id = request.GET.get('fb_id', None)
            fb_key =request.GET.get('fb_key', None)


            option = request.GET.get('option', None)
            level =str(FarmLevel.objects.get(id = request.GET.get('level', None)).level)

            try:
                script_to_run = UsersFormscript.objects.get(id=request.GET.get('id', None),start__exact=True,running__exact=False)
                # set running status True
                script_to_run.running = True
                script_to_run.save()

                #
                try:
                    return_result = start(fb_id, fb_key, level)
                except:
                    da = {
                        'running': False,
                        'message': "Trying Again, Some Error in running script !"
                    }
                    # set running status False after finishing the script running
                    script_error = UsersFormscript.objects.get(id=request.GET.get('id', None))
                    script_error.running = False
                    script_error.save()
                    return JsonResponse(da)
                # set running status False after finishing the script running
                script = UsersFormscript.objects.get(id=request.GET.get('id', None))
                script.running = False
                script.save()

                return JsonResponse(return_result)
            except:
                dat = {
                    'running': True,
                    'message': "runing now !"
                }
                return JsonResponse(dat)
            # return the result of running the custom script

        else:
            data = {
                'no_task': True,
                'message': "No task to run !"
            }
            return JsonResponse(data)
    else:
    # if don't login, redirect to homepage and display login modal
        return index(request, True)


# stop custom script running

def script_stop(request):
    if "logged_in" in request.session and request.is_ajax():

        if UsersFormscript.objects.filter(id=request.GET.get('id', None)).exists():
            running_script = UsersFormscript.objects.get(id=request.GET.get('id', None))

            running_script.start = False

            running_script.save()

            data = {
                'stopped': True,
            }
            return JsonResponse(data)
            # return tasks(request)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)


# displaying Portal Script Form#1
def form1(request):
    if "logged_in" in request.session:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if UsersPay.objects.filter(user_id__exact=request.session.get('user_id'), membership__gte=1,
                                   publish__exact=1).exists():
            # if currnent date is not next payment
            temp = UsersPay.objects.get(user_id__exact=request.session.get('user_id'), membership__gte=1,
                                   publish__exact=1)
            if temp.next_pay.strftime("%Y-%m-%d %H:%M:%S") < now:
                data = {
                    'result': False,
                    'error_message': "Payment date is passed, please repay !"
                }
                return subscription(request, data)
            else:
                return render(request, 'portal/form/form1.html',
                          {'fb_list' : list(UsersFb.objects.filter(user_id__exact=request.session.get('user_id')).values()),
                           'levels': FarmLevel.objects.filter(hidden=False,raid__exact=0)})
        else:
            data = {
                'result': False,
                'error_message': "You should get Basic subscription !"
            }
            return subscription(request,data)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# start Portal Script Form#2
def start_form2(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        form_kind = 2
        fb_id = UsersFb.objects.get(user_id=user_id).id
        level = request.POST.get('form1_level')
        opt = request.POST.get('opt')
        if opt:
            option = opt
        else:
            option = 0

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # updating used field of the specified in users_fb table
        user_fb = UsersFb.objects.get(id=fb_id)
        user_fb.used = True
        user_fb.save()

        # storing new record in users_formscript
        user_formscript = UsersFormscript(
            user_id=user_id,
            form_kind=form_kind,
            fb_id=fb_id,
            level=level,
            option=option,
            created=now,
            start = True,
            running=False)
        user_formscript.save()
        fb_key = request.POST.get('form1_fb_key')
        fb_id = UsersFb.objects.get(id = fb_id).fb_id
        level_comment = FarmLevel.objects.get(id__exact=level).comment

        # custom python script part here

        # -----------------------------------
        return render(request, 'portal/form/form2.html', {'script' : user_formscript,'fb_key' : fb_key,'fb_id' : fb_id,'comment' : level_comment})

    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)
# displaying Portal Script Form#2
def form2(request):
    if "logged_in" in request.session:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if UsersPay.objects.filter(user_id__exact=request.session.get('user_id'), membership__gte=2,
                                   publish__exact=1).exists():
            # if currnent date is not next payment
            temp = UsersPay.objects.get(user_id__exact=request.session.get('user_id'), membership__gte=2,
                                   publish__exact=1)
            if temp.next_pay.strftime("%Y-%m-%d %H:%M:%S") < now:
                data = {
                    'result': False,
                    'error_message': "Payment date is passed, please repay !"
                }
                return subscription(request, data)
            else:
                return render(request, 'portal/form/form2.html',
                          {'fb_list' : list(UsersFb.objects.filter(user_id__exact=request.session.get('user_id')).values()),
                           'levels': FarmLevel.objects.filter(hidden=False,raid__exact=0)})
        else:
            data = {
                'result': False,
                'error_message': "You should get Professional subscription !"
            }
            return subscription(request,data)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# start Portal Script Form#3
def start_form3(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        form_kind = 3
        fb_id = UsersFb.objects.get(user_id=user_id).id
        level = request.POST.get('form1_level')
        opt = int(request.POST.get('opt'))
        if opt:
            option = opt
        else:
            option = 0

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # updating used field of the specified in users_fb table
        user_fb = UsersFb.objects.get(id=fb_id)
        user_fb.used = True
        user_fb.save()

        # storing new record in users_formscript
        user_formscript = UsersFormscript(
            user_id=user_id,
            form_kind=form_kind,
            fb_id=fb_id,
            level=level,
            option=option,
            created=now,
            start = True,
            running=False)
        user_formscript.save()
        fb_key = request.POST.get('form1_fb_key')
        fb_id = UsersFb.objects.get(id=fb_id).fb_id
        level_comment = FarmLevel.objects.get(id__exact=level).comment

        # custom python script part here

        # -----------------------------------
        return render(request, 'portal/form/form3.html',
                      {'script': user_formscript, 'fb_key': fb_key, 'fb_id': fb_id, 'comment': level_comment})
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)


# displaying Portal Script Form#3
def form3(request):
    if "logged_in" in request.session:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if UsersPay.objects.filter(user_id__exact=request.session.get('user_id'), membership__gte=3,
                                   publish__exact=1).exists():
            # if currnent date is not next payment
            temp = UsersPay.objects.get(user_id__exact=request.session.get('user_id'), membership__gte=3,
                                   publish__exact=1)
            if temp.next_pay.strftime("%Y-%m-%d %H:%M:%S") < now:
                data = {
                    'result': False,
                    'error_message': "Payment date is passed, please repay !"
                }
                return subscription(request, data)
            else:
                return render(request, 'portal/form/form3.html',
                          {'fb_list' : list(UsersFb.objects.filter(user_id__exact=request.session.get('user_id')).values()),
                           'levels': FarmLevel.objects.filter(hidden=False,raid__exact=0)})
        else:
            data = {
                'result': False,
                'error_message': "You should get Premier subscription !"
            }
            return subscription(request,data)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# start Portal Script Form#4
def start_form4(request):
    if "logged_in" in request.session:
        user_id = request.session.get('user_id')
        form_kind = 4
        fb_id = UsersFb.objects.get(user_id=user_id).id
        level = request.POST.get('form1_level')
        opt = int(request.POST.get('opt'))
        if opt:
            option = opt
        else:
            option = 0

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # updating used field of the specified in users_fb table
        user_fb = UsersFb.objects.get(id=fb_id)
        user_fb.used = True
        user_fb.save()

        # storing new record in users_formscript
        user_formscript = UsersFormscript(
            user_id=user_id,
            form_kind=form_kind,
            fb_id=fb_id,
            level=level,
            option=option,
            created=now,
            start = True,
            running=False)
        user_formscript.save()
        fb_key = request.POST.get('form1_fb_key')
        fb_id = UsersFb.objects.get(id=fb_id).fb_id
        level_comment = FarmLevel.objects.get(id__exact=level).comment

        # custom python script part here

        # -----------------------------------

        return render(request, 'portal/form/form4.html',
                      {'script': user_formscript, 'fb_key': fb_key, 'fb_id': fb_id, 'comment': level_comment})
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# displaying Portal Script Form#4
def form4(request):
    if "logged_in" in request.session:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if UsersPay.objects.filter(user_id__exact=request.session.get('user_id'), membership__gte=3,
                                   publish__exact=1).exists():
            # if currnent date is not next payment
            temp = UsersPay.objects.get(user_id__exact=request.session.get('user_id'), membership__gte=3,
                                   publish__exact=1)
            if temp.next_pay.strftime("%Y-%m-%d %H:%M:%S") < now:
                data = {
                    'result': False,
                    'error_message': "Payment date is passed, please repay !"
                }
                return subscription(request, data)
            else:
                return render(request, 'portal/form/form4.html',
                          {'fb_list' : list(UsersFb.objects.filter(user_id__exact=request.session.get('user_id')).values()),
                           'levels': FarmLevel.objects.filter(hidden=False,raid__exact=0)})
        else:
            data = {
                'result': False,
                'error_message': "You should get Premier subscription !"
            }
            return subscription(request,data)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# payment success
@csrf_exempt
def payment_success(request):
    time.sleep(8)
    if "logged_in" in request.session:
        try:
            latest_payment = PayPalIPN.objects.all().order_by('-id')[0];
            # payment is success
            if latest_payment.payment_status == "Completed":
                # transaction is not already used
                if latest_payment.option_selection2 !='used':
                    latest_payment.option_selection2 = 'used'
                    latest_payment.save()
                    if int(latest_payment.mc_gross) == 10:
                        membership = 1
                    elif int(latest_payment.mc_gross) == 15:
                        membership = 2
                    elif int(latest_payment.mc_gross) == 20:
                        membership = 3
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # splitting the current date
                    splited_date = now.split('-')
                    if splited_date[1] == '12':
                        year = int(splited_date[0]) + 1
                        next_month_date = str(year) + "-01" + "-" + splited_date[2]
                    else:
                        month = int(splited_date[1]) + 1
                        next_month_date = splited_date[0] + "-" + str(month) + "-" +splited_date[2]
                    # user has already paid
                    if UsersPay.objects.filter(user_id__exact=request.session.get('user_id')).exists():
                        user_payment = UsersPay.objects.get(user_id__exact=request.session.get('user_id'))
                        user_payment.membership = membership
                        user_payment.amount = int(latest_payment.mc_gross)
                        user_payment.payed = now
                        user_payment.next_pay = next_month_date
                        user_payment.save()
                    else:
                        new_payment = UsersPay(user_id = request.session.get('user_id'),
                                               membership = membership,
                                               amount = int(latest_payment.mc_gross),
                                               payed = now,
                                               next_pay = next_month_date,
                                               period = 1,
                                               publish = 1)
                        new_payment.save()

                    latest_payment.option_selection2 = 'used'
                    latest_payment.save()
                    result = 'Welcome, your payment is successed !'
                else:
                    return index(request, False)
            else:
                result = 'Sorry, payment is not completed !'
        except:
            return index(request, False)
        return render(request, "portal/subscription/success.html", {'result':result})
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# payment failed
@csrf_exempt
def payment_failed(request):
    if "logged_in" in request.session:
        return render(request, "portal/subscription/failed.html")
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)

# if clicking subscription button
def subscription(request,payment_status=None):
    if "logged_in" in request.session:
        invoice_stamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        # What you want the button to do.
        paypal_dict1 = {
            "business": "lopoevil+buss_seller@gmail.com",
            "amount": "10.00",
            "item_name": "TMR_1_Month_Access_1_ID",
            "invoice": invoice_stamp,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('success')),
            "cancel_return": request.build_absolute_uri(reverse('failed')),
            "custom": "1_Mo_1_Acct",  # Custom command to correlate to some function later (optional)
        }

        paypal_dict2 = {
            "business": "lopoevil+buss_seller@gmail.com",
            "amount": "15.00",
            "item_name": "name of the item",
            "invoice": invoice_stamp,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('success')),
            "cancel_return": request.build_absolute_uri(reverse('failed')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }
        paypal_dict3 = {
            "business": "lopoevil+buss_seller@gmail.com",
            "amount": "20.00",
            "item_name": "name of the item",
            "invoice": invoice_stamp,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('success')),
            "cancel_return": request.build_absolute_uri(reverse('failed')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }
        # Create the instance for the 1st portal.
        form1 = PayPalPaymentsForm(initial=paypal_dict1)
        # Create the instance for the 2nd portal.
        form2 = PayPalPaymentsForm(initial=paypal_dict2)
        # Create the instance for the 3th portal.
        form3 = PayPalPaymentsForm(initial=paypal_dict3)
        context = {"form1": form1,"form2": form2,"form3": form3,'payment_status':payment_status}

        return render(request, 'portal/subscription/subscription.html', context)
    else:
        # if don't login, redirect to homepage and display login modal
        return index(request, True)


# logging in
def login(request):
    if request.is_ajax():
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)
        data = {
            # 'is_logged': True
            'is_logged': Users.objects.filter(email__iexact=email, password__iexact=hashlib.md5(
                password.encode("utf-8")).hexdigest()).exists()
        }
        if data['is_logged'] is False:
            data['error_message'] = 'Invalid password or email. Try again.'

        else:
            user = Users.objects.get(email__iexact=email,
                                     password__iexact=hashlib.md5(password.encode("utf-8")).hexdigest())
            request.session['logged_in'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email

        return JsonResponse(data)


# logging out
def logout(request):
    del request.session['logged_in']
    del request.session['user_id']
    del request.session['user_name']
    del request.session['user_email']
    return redirect('/')


# validating if the name is already existed in users table
def validate_username(request):
    if request.is_ajax():
        name = request.GET.get('name', None)
        data = {
            'is_taken': Users.objects.filter(name__iexact=name).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'A user with this username already exists.'
        return JsonResponse(data)


# validating if email is already existed in users table
def validate_email(request):
    if request.is_ajax():
        email = request.GET.get('email', None)
        data = {
            'is_taken': Users.objects.filter(email__iexact=email).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'A user with this email already exists.'
        return JsonResponse(data)


# sending email if forggetting password
def forget_email(request):
    if request.is_ajax():
        email = request.GET.get('email', None)
        if Users.objects.filter(email__iexact=email).exists():
            # sending eamil part
            password = Users.objects.get(email__iexact=email).basic_password

            try:
                send_mail("Hello", "Your password: " + password, "yifeili924@outlook.com", [email])
                data = {
                    'message': "We've sent email to your address. Please check."
                }
            except:
                data = {
                    'message': "Email sendig error, try again !"
                }
        else:
            data = {
                'message': "No such email address, input the correct email !"
            }
        return JsonResponse(data)


# registering the user
def register(request):
    if request.is_ajax():
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = Users(name=name,
                     email=email,
                     password=hashlib.md5(password.encode("utf-8")).hexdigest(),
                     basic_password=password,
                     created=now,
                     updated=now)
        user.save()
        data = {
            'is_registered': True
        }
        user = Users.objects.get(email__iexact=email,
                                 password__iexact=hashlib.md5(password.encode("utf-8")).hexdigest())
        request.session['logged_in'] = True
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_email'] = user.email

        return JsonResponse(data)


class IndexView(generic.ListView):
    template_name = 'portal/index.html'
    # context_object_name = 'latest_question_list'
