
class UpdateUserEntranceView(APIView):
    def get(self, request, *args, **kwargs):
        secret_key = request.headers.get('hub-secret-key', None)
        if secret_key == hashed_hub_secret_key:
            user_id = kwargs.get('id')
            hour = kwargs.get('hour')
            minute = kwargs.get('minute')

            # time must be received in the format: '%H-%M'
            if user_id and hour and minute:
                try:
                    time_received = f"{str(hour).zfill(2)}-{str(minute).zfill(2)}"
                    # check if datetime is in the correct format
                    if not (re.match(r'^\d{2}-\d{2}$', time_received) and (0 <= int(hour) <= 23) and (0 <= int(minute) <= 59)):
                        return Response({'message': 'Invalid time format'}, status=400)
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    date_strings_list = date.split("-")

                    detected_user = CustomUser.objects.get(id=user_id)
                    attendance_obj = json.loads(detected_user.attendance)

                    # Check if the date is already in the attendance object unlless create it
                    if date_strings_list[0] in attendance_obj:
                        if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
                            if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                                pass
                            else:
                                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {
                                    'entrance': [], 'leave': []}
                        else:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]] = {
                                date_strings_list[2]: {'entrance': [], 'leave': []}}
                    else:
                        attendance_obj[date_strings_list[0]] = {
                            date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}

                    time_format = '%H-%M'  # expected format of time
                    entrance_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance']
                    if len(entrance_list_of_day) > 0:
                        last_entrance = datetime.datetime.strptime(entrance_list_of_day[-1], time_format)
                        current_entrance = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
                        # Check if the time difference between the last entrance and the current entrance is
                        # less than the minimum minutes threshold

                        received_time = datetime.datetime.strptime(time_received, time_format)
                        timeDiffWithCurrent = (current_entrance - last_entrance) if ( current_entrance > last_entrance) else (last_entrance - current_entrance)
                        timeDiffWithLast = (last_entrance - received_time) if ( last_entrance > received_time) else (received_time - last_entrance)
                        if timeDiffWithCurrent < datetime.timedelta(minutes=min_minutes_threshold) or \
                                timeDiffWithLast < datetime.timedelta(minutes=min_minutes_threshold):
                            return Response({'message': 'Entrance not updated. Minimum minutes threshold not reached'}, status=400)
                    attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time_received)

                    # If updated successfully, save the user
                    detected_user.attendance = json.dumps(attendance_obj)
                    detected_user.save()

                    return Response({'message': 'Entrance updated successfully', 'firstName': detected_user.first_name,
                                     'lastName': detected_user.last_name, 'time': time_received})
                except CustomUser.DoesNotExist:
                    return Response({'message': 'User does not exist'}, status=400)
            else:
                return Response({'message': 'Invalid path parameters'}, status=400)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)



class UpdateUserLeaveView(APIView):
    def get(self, request, *args, **kwargs):
        secret_key = request.headers.get('hub-secret-key', None)
        if secret_key == hashed_hub_secret_key:
            user_id = kwargs.get('id')
            hour = kwargs.get('hour')
            minute = kwargs.get('minute')

            # time must be received in the format: '%H-%M'
            if user_id and hour and minute:
                try:
                    time_received = f"{str(hour).zfill(2)}-{str(minute).zfill(2)}"
                    # check if datetime is in the correct format
                    if not (re.match(r'^\d{2}-\d{2}$', time_received) and (0 <= int(hour) <= 23) and (0 <= int(minute) <= 59)):
                        return Response({'message': 'Invalid time format'}, status=400)
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    date_strings_list = date.split("-")

                    detected_user = CustomUser.objects.get(id=user_id)
                    attendance_obj = json.loads(detected_user.attendance)

                    # Check if the date is already in the attendance object unlless create it
                    if date_strings_list[0] in attendance_obj:
                        if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
                            if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                                pass
                            else:
                                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {
                                    'entrance': [], 'leave': []}
                        else:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]] = {
                                date_strings_list[2]: {'entrance': [], 'leave': []}}
                    else:
                        attendance_obj[date_strings_list[0]] = {
                            date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}

                    time_format = '%H-%M'  # expected format of time
                    leave_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave']
                    if len(leave_list_of_day) > 0:
                        last_leave = datetime.datetime.strptime(leave_list_of_day[-1], time_format)
                        current_leave = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
                        # Check if the time difference between the last leave and the current leave is
                        # less than the minimum minutes threshold

                        received_time = datetime.datetime.strptime(time_received, time_format)
                        timeDiffWithCurrent = (current_leave - last_leave) if (current_leave > last_leave) else (last_leave - current_leave)
                        timeDiffWithLast = (last_leave - received_time) if ( last_leave > received_time) else (received_time - last_leave)
                        if timeDiffWithCurrent < datetime.timedelta(minutes=min_minutes_threshold) or \
                                timeDiffWithLast < datetime.timedelta(minutes=min_minutes_threshold):
                            return Response({'message': 'Leave not updated. Minimum minutes threshold not reached'}, status=400)
                    attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time_received)

                    # If updated successfully, save the user
                    detected_user.attendance = json.dumps(attendance_obj)
                    detected_user.save()

                    return Response({'message': 'Leave updated successfully', 'firstName': detected_user.first_name,
                                     'lastName': detected_user.last_name, 'time': time_received})
                except CustomUser.DoesNotExist:
                    return Response({'message': 'User does not exist'}, status=400)
            else:
                return Response({'message': 'Invalid path parameters'}, status=400)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class GetUserEncodingsView(APIView):
    def get(self, request, *args, **kwargs):
        secret_key = request.headers.get('hub-secret-key', None)
        if secret_key == hashed_hub_secret_key:
            try:
                users_data = CustomUser.objects.all().values('id', 'encodings')
                return Response({'users': list(users_data)})
            except CustomUser.DoesNotExist:
                return Response({'message': 'No users found'}, status=400)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
