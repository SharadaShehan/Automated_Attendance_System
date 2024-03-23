import 'package:flutter/material.dart';
import 'package:frontend/models/user.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:provider/provider.dart';
import '../api/view_employee_attendance_api.dart';
import '../utilities/persistent_store.dart';

class EmployeeAttendance extends StatefulWidget {
  final int id;
  final String date;
  const EmployeeAttendance({super.key, required this.id, required this.date});

  @override
  State<EmployeeAttendance> createState() => _EmployeeAttendanceState();
}

class _EmployeeAttendanceState extends State<EmployeeAttendance> {
  User? _employee;

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
                Text(
                    'Employee: ${_employee!.firstName} ${_employee!.lastName}'),
                Text('Attendance: ${_employee!.attendance}'),
                Text('Date: ${widget.date}'),
              ],
            ),
    );
  }
}
