import 'package:flutter/material.dart';
import 'package:frontend/pages/employee_attendance_page.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:table_calendar/table_calendar.dart';
import '../api/attendance_by_date_api.dart';
import '../models/user_attendance.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';

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

  getUserAttendanceByDate(GlobalVariablesProvider provider) async {
    _userAttendanceList = null;
    final token = await getToken();
    final userAttendanceList = await AttendanceByDateApi.getAttendanceByDate(
        token!, _selectedDay.toString());
    if (userAttendanceList == null) {
      await removeToken();
      provider.updateLogout();
      return;
    }
    setState(() {
      // remove current user from the list
      userAttendanceList
          .removeWhere((element) => element.id == provider.user!.id);
      _userAttendanceList = userAttendanceList;
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    if (_userAttendanceList == null) {
      getUserAttendanceByDate(provider);
    }
    return Container(
      child: Column(
        children: [
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
          ),
          _userAttendanceList == null
              ? const CircularProgressIndicator()
              : Expanded(
                  child: ListView.builder(
                    itemCount: _userAttendanceList!.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(_userAttendanceList![index]
                                .firstName
                                .toString() +
                            ' ' +
                            _userAttendanceList![index].lastName.toString()),
                        subtitle: Text('Item subtitle'),
                        leading: Icon(Icons.star),
                        trailing: Icon(Icons.chevron_right),
                        onTap: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => EmployeeAttendancePage(
                                      id: _userAttendanceList![index].id)));
                        },
                      );
                    },
                  ),
                ),
        ],
      ),
    );
  }
}
