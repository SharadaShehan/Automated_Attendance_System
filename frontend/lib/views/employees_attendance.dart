import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/pages/employee_attendance_page.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:table_calendar/table_calendar.dart';
import '../api/attendance_by_date_api.dart';
import '../models/user_attendance.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';
import 'package:intl/intl.dart';

class EmployeesAttendance extends StatefulWidget {
  const EmployeesAttendance({super.key});

  @override
  State<EmployeesAttendance> createState() => _EmployeesAttendanceState();
}

class _EmployeesAttendanceState extends State<EmployeesAttendance> {
  DateTime _selectedDay = DateTime.now();
  DateTime _focusedDay = DateTime.now();
  CalendarFormat _calendarFormat = CalendarFormat.month;
  List<UserAttendance>? _userAttendanceList;
  bool displayCalendar = false;

  getUserAttendanceByDate(GlobalVariablesProvider provider) async {
    _userAttendanceList = null;
    final token = await getToken();
    final userAttendanceList = await AttendanceByDateApi.getAttendanceByDate(
        token, _selectedDay.toString());
    if (userAttendanceList == null) {
      await removeToken();
      provider.updateLogout();
      return;
    }
    setState(() {
      // remove current user from the list
      userAttendanceList
          .removeWhere((element) => element.id == provider.user!.id);
      // sort users by last entrance time
      userAttendanceList.sort((a, b) {
        if (a.entrance.length == 0) {
          return 1;
        } else if (b.entrance.length == 0) {
          return -1;
        } else {
          return getTimeObj(b.entrance.last)
              .compareTo(getTimeObj(a.entrance.last));
        }
      });
      _userAttendanceList = userAttendanceList;
    });
  }

  getAttendanceCount() {
    return _userAttendanceList
        ?.where((userObj) => userObj.entrance.length > 0)
        .length
        .toString();
  }

  getTimeObj(timeString) {
    List<String> timeParts = timeString.split('-');
    int hour = int.parse(timeParts[0]);
    int minute = int.parse(timeParts[1]);

    // Optional: Create a DateTime object with current date
    DateTime now = DateTime.now();
    DateTime timeOnly = DateTime(now.year, now.month, now.day, hour, minute);
    return timeOnly;
  }

  getPresenceStatus(userObj) {
    if (userObj != null) {
      List<String> entranceTimes = userObj.entrance ?? [];
      List<String> exitTimes = userObj.leave ?? [];
      if (entranceTimes.length == 0) {
        return 0;
      } else if (exitTimes.length == 0) {
        return 2;
      } else {
        String latestEntrance = entranceTimes.last;
        String latestExit = exitTimes.last;
        if (latestExit == null) {
          return 2;
        } else if (getTimeObj(latestEntrance).isAfter(getTimeObj(latestExit))) {
          return 2;
        } else {
          return 1;
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    if (_userAttendanceList == null) {
      getUserAttendanceByDate(provider);
    }
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Container(
              padding: const EdgeInsets.fromLTRB(80, 30, 0, 10),
              child: Text(
                '${DateFormat('MMMM').format(_selectedDay).toString().substring(0, 3)} ${_selectedDay.day.toString()}, ${_selectedDay.year.toString()}',
                style: const TextStyle(fontSize: 25),
              ),
            ),
            GestureDetector(
              child: const Icon(Icons.calendar_today),
              onTap: () {
                setState(() {
                  displayCalendar = !displayCalendar;
                });
              },
            ),
          ],
        ),
        if (!displayCalendar)
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.fromLTRB(0, 0, 0, 8),
                child: const Text(
                  'Attendance Count',
                  style: TextStyle(
                    fontSize: 18,
                    color: Color.fromARGB(255, 97, 97, 97),
                  ),
                ),
              ),
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.blue.shade400,

                  // borderRadius: BorderRadius.circular(10),
                ),
                // padding: const EdgeInsets.fromLTRB(0, 0, 0, 10),
                child: Center(
                  child: Text(
                    '${getAttendanceCount()}',
                    style: const TextStyle(
                      fontSize: 28,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 15.0)
            ],
          ),
        if (displayCalendar)
          TableCalendar(
            daysOfWeekHeight: 20.0,
            rowHeight: 40.0,
            firstDay: DateTime.utc(2024, 3, 1),
            lastDay: DateTime.utc(2024, 3, 31),
            focusedDay: _focusedDay,
            selectedDayPredicate: (day) {
              return isSameDay(_selectedDay, day);
            },
            onDaySelected: (selectedDay, focusedDay) {
              setState(() {
                _selectedDay = selectedDay;
                _focusedDay = focusedDay;
                getUserAttendanceByDate(provider);
              });
            },
            calendarFormat: _calendarFormat,
            onFormatChanged: (format) {
              setState(() {
                _calendarFormat = format;
              });
            },
            onPageChanged: (focusedDay) {
              _focusedDay = focusedDay;
            },
            calendarStyle: CalendarStyle(
              defaultDecoration: BoxDecoration(
                color: Colors.lightBlue.shade50,
                shape: BoxShape.circle,
              ),
              weekendDecoration: BoxDecoration(
                color: Colors.lightBlue.shade50,
                shape: BoxShape.circle,
              ),
              selectedDecoration: const BoxDecoration(
                color: Colors.blue,
                shape: BoxShape.circle,
              ),
              defaultTextStyle: const TextStyle(color: Colors.black54),
              weekendTextStyle: const TextStyle(color: Colors.black54),
              selectedTextStyle: const TextStyle(color: Colors.white),
              todayDecoration: const BoxDecoration(
                color: Colors.orange,
                shape: BoxShape.circle,
              ),
            ),
            headerStyle: const HeaderStyle(
              titleCentered: true,
              formatButtonVisible: false,
              titleTextStyle: TextStyle(fontSize: 18),
            ),
          ),
        _userAttendanceList == null
            ? const CircularProgressIndicator()
            : Expanded(
                child: ListView.builder(
                  itemCount: _userAttendanceList!.length,
                  itemBuilder: (context, index) {
                    return DecoratedBox(
                      decoration: BoxDecoration(
                        color: getPresenceStatus(_userAttendanceList![index]) ==
                                0
                            ? Colors.red.shade50
                            : getPresenceStatus(_userAttendanceList![index]) ==
                                    1
                                ? Colors.orange.shade50
                                : Colors.green.shade50,
                        borderRadius: BorderRadius.circular(20.0),
                        border: Border(
                          bottom: BorderSide(
                            color: Colors.grey.shade300,
                            width: 1.0,
                          ),
                          // top: BorderSide(
                          //   color: Colors.grey.shade300,
                          //   width: 1.0,
                          // ),
                        ),
                      ),
                      child: ListTile(
                        title: Text(
                          '${_userAttendanceList![index].firstName.toString()} ${_userAttendanceList![index].lastName.toString()}',
                          style: const TextStyle(fontSize: 18),
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${getPresenceStatus(_userAttendanceList![index]) == 0 ? 'Absent' : getPresenceStatus(_userAttendanceList![index]) == 1 ? 'Out of Office' : 'In Office'}',
                              style: TextStyle(
                                  color: getPresenceStatus(
                                              _userAttendanceList![index]) ==
                                          0
                                      ? Colors.red.shade800
                                      : getPresenceStatus(_userAttendanceList![
                                                  index]) ==
                                              1
                                          ? Colors.orange.shade800
                                          : Colors.green.shade800),
                            ),
                            Text(
                                'First Entrance: ${_userAttendanceList![index].entrance.length == 0 ? 'N/A' : _userAttendanceList![index].entrance.first}'),
                          ],
                        ),
                        leading: const Icon(Icons.star),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => EmployeeAttendancePage(
                                      id: _userAttendanceList![index].id,
                                      date: _selectedDay.toString())));
                        },
                      ),
                    );
                  },
                ),
              ),
      ],
    );
  }
}
