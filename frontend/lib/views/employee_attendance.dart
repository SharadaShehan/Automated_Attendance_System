import 'package:flutter/material.dart';
import 'package:frontend/models/user.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:provider/provider.dart';
import '../api/view_employee_attendance_api.dart';
import '../utilities/persistent_store.dart';
import 'package:flutter_heatmap_calendar/flutter_heatmap_calendar.dart';
import 'dart:convert';

class EmployeeAttendance extends StatefulWidget {
  final int id;
  final String date;
  const EmployeeAttendance({super.key, required this.id, required this.date});

  @override
  State<EmployeeAttendance> createState() => _EmployeeAttendanceState();
}

class _EmployeeAttendanceState extends State<EmployeeAttendance> {
  User? _employee;
  List<dynamic>? _entrancesOfDate, _exitsOfDate;
  String _selectedDate = '';

  getEmployeeDetails(GlobalVariablesProvider provider) async {
    _employee = null;
    final token = await getToken();
    final employee =
        await ViewEmployeeDetailsApi.getEmployeeDetails(token, widget.id);
    if (employee == null) {
      await removeToken();
      provider.updateLogout();
      return;
    }
    setState(() {
      _employee = employee;
    });
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

  attendanceObjToDateSet(attendanceString) {
    Map<String, dynamic> map =
        jsonDecode(attendanceString) as Map<String, dynamic>;
    Map<DateTime, int> attendanceMap = {};
    map.forEach((key, value) {
      String year = key;
      Map<String, dynamic> monthMap = value as Map<String, dynamic>;
      monthMap.forEach((key, value) {
        String month = key;
        Map<String, dynamic> dayMap = value as Map<String, dynamic>;
        dayMap.forEach((key, value) {
          String day = key;
          // create a date object
          DateTime date = DateTime(
              int.parse(year), int.parse(month), int.parse(day), 0, 0, 0, 0, 0);
          if (value == null || value.isEmpty) {
            attendanceMap[date] = 18;
            return;
          }
          // print type of value
          // print(value.runtimeType);
          // parse value as a _Map<String, dynamic>
          Map<String, dynamic> valueMap = value as Map<String, dynamic>;
          // get the time value
          String time = valueMap['entrance'][0];
          attendanceMap[date] = getTimeObj(time).hour;
        });
      });
    });
    return attendanceMap;
  }

  getAttendancesOfDate(attendanceString, year, month, day) {
    Map<String, dynamic> map =
        jsonDecode(attendanceString) as Map<String, dynamic>;
    Map<String, dynamic> monthsMap =
        map[year.toString()] as Map<String, dynamic>;
    Map<String, dynamic> daysMap =
        monthsMap[month.toString()] as Map<String, dynamic>;
    if (daysMap[day.toString()] == null) {
      Map<String, dynamic> attendanceMap = {
        'entrance': [],
        'leave': [],
      };
      return attendanceMap;
    }
    return daysMap[day.toString()];
    // daysMap contains all the days of the month
    // return all elements of the day. there are multiple entrances and exits
    // Map<String, dynamic> attendaceMap = {};
  }

  updateAttendanceOfDate(attendanceString, year, month, day) {
    Map<String, dynamic> attendanceMap =
        getAttendancesOfDate(attendanceString, year, month, day);
    setState(() {
      _entrancesOfDate = attendanceMap['entrance'];
      _exitsOfDate = attendanceMap['leave'];
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    if (_employee == null) {
      getEmployeeDetails(provider);
    }

    return Container(
      child: _employee == null
          ? const CircularProgressIndicator()
          : Column(
              children: [
                const SizedBox(height: 20),
                Text(
                  '${_employee!.firstName} ${_employee!.lastName}',
                  style: const TextStyle(
                    fontSize: 23,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 10),
                Text(_selectedDate,
                    style: const TextStyle(
                      fontSize: 18,
                      // fontWeight: FontWeight.bold,
                    )),
                const SizedBox(height: 15),
                if (_entrancesOfDate != null && _entrancesOfDate!.isNotEmpty)
                  Column(
                    children: [
                      DataTable(
                        columns: const [
                          DataColumn(label: Center(child: Text('Entrances'))),
                          DataColumn(label: Center(child: Text('Leaves'))),
                        ],
                        rows: List<DataRow>.generate(_entrancesOfDate!.length,
                            (index) {
                          return DataRow(
                            cells: [
                              DataCell(Center(
                                  child: Text(_entrancesOfDate![index]))),
                              DataCell(Center(
                                  child: Text(
                                      '${_exitsOfDate != null ? _exitsOfDate!.length > index ? _exitsOfDate![index] : '' : ''}'))),
                            ],
                          );
                        }),
                        dataRowColor: MaterialStateProperty.resolveWith<Color>(
                            (Set<MaterialState> states) {
                          if (states.contains(MaterialState.selected)) {
                            return Theme.of(context)
                                .colorScheme
                                .primary
                                .withOpacity(0.08);
                          }
                          return Colors.lightBlue[50]!;
                        }),
                        headingRowColor:
                            MaterialStateProperty.resolveWith<Color>(
                                (Set<MaterialState> states) {
                          if (states.contains(MaterialState.selected)) {
                            return Theme.of(context)
                                .colorScheme
                                .primary
                                .withOpacity(0.08);
                          }
                          return Colors.blue.shade400;
                        }),
                        headingTextStyle: const TextStyle(
                            // fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Colors.white),
                      ),
                    ],
                  ),
                const SizedBox(height: 10),
                Center(
                  child: HeatMapCalendar(
                    defaultColor: Colors.lightBlue[50]!,
                    // flexible: true,
                    colorMode: ColorMode.color,
                    textColor: Colors.black,
                    size: 45.0,
                    margin: EdgeInsets.fromLTRB(3, 1, 3, 1),
                    fontSize: 12.0,
                    borderRadius: 20.0,
                    showColorTip: false,
                    monthFontSize: 15.0,
                    datasets: attendanceObjToDateSet(_employee!.attendance),
                    colorsets: const {
                      5: Colors.green,
                      7: Colors.lightGreenAccent,
                      9: Colors.yellow,
                      11: Colors.orange,
                      13: Colors.redAccent,
                    },
                    onClick: (value) {
                      // ScaffoldMessenger.of(context).showSnackBar(
                      //     SnackBar(content: Text(value.toString())));
                      String dateString = value.toString();
                      String year = dateString.substring(0, 4);
                      String month = dateString.substring(5, 7);
                      String day = dateString.substring(8, 10);
                      setState(() {
                        _selectedDate = '$year-$month-$day';
                      });
                      updateAttendanceOfDate(
                          _employee!.attendance, year, month, day);
                    },
                  ),
                ),
              ],
            ),
    );
  }
}
