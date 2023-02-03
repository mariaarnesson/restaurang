

def make_reservation(request):
    weekdays = validweekday(22)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('select a table')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please select a table!")
            return redirect('make_reservation')
        request.session['day'] = day
        request.session['service'] = service

        return redirect('choose_time')

    return render(request, 'make_reservation.html', {
                'weekdays': weekdays,
                'validateWeekdays' : validateweekdays,
                })           


def choose_time(request):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    guest = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Table.objects.filter(day=day).count() < 11:
                        if Table.objects.filter(day=day, time=time).count() < 1:
                            TableForm = Table.objects.get_or_create(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Reservation saved!")
                            return redirect('home')
                        else:
                            messages.success(request, "This selected time is already taken!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Table!")

    return render(request, 'choose_time.html', {
        'times':hour,
    })


def userPanel(request):
    user = request.user
    tables = Table.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user': user,
        'table': table,
    })


def userUpdate(request, id):
    table = Table.objects.get(pk=id)
    userdatepicked = table.day
    # Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    # 24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    # Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    
    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        # Store day and service in django session:
        request.session['day'] = day
        request.session['editbooking'] = service

        return redirect('editbooking', id=id)

    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def editbooking(request, id):
    user = request.user
    times = [
        "6 PM", "6:30 PM", "7 PM", "7:30 PM", "8 PM", "8:30 PM", "9 PM", "9:30 PM", "10 PM", "10:30 PM"
    ]
    guest = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    # Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    table = Table.objects.get(pk=id)
    userSelectedTime = table.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Table.objects.filter(day=day).count() < 11:
                        if Table.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            TableForm = Table.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Table edited!")
                            return redirect('home')
                        else:
                            messages.success(request, "This selected time is already taken!")
                    else:
                        messages.success(request, "The selected day is full!")
                else:
                    messages.success(request, "The selected date is incorrect")
            else:
                messages.success(request, "The selected date isn't in the correct time period!")
        else:
            messages.success(request, "Please select a table!")
        return redirect('userPanel')

    return render(request, 'editbooking.html', {
        'times': hour,
        'id': id,
    })

def mybookings(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    # Only show the free table 21 days from today
    items = Table.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'mybookings.html', {
        'items': items,
    })


def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y


def validWeekday(days):
    # Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range(0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays


def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Table.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays


def checkTime(times, day):
    # Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Table.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x


def checkEditTime(times, day, id):
    # Only show the time of the day that has not been selected before:
    x = []
    table = Table.objects.get(pk=id)
    time = table.time
    for k in times:
        if Table.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
    