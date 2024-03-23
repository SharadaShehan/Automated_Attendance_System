import 'package:flutter/material.dart';
import 'package:frontend/views/employee_attendance.dart';

class EmployeeAttendancePage extends StatefulWidget {
  final int id;
  final String date;
  const EmployeeAttendancePage(
      {super.key, required this.id, required this.date});

  @override
  State<EmployeeAttendancePage> createState() => _EmployeeAttendancePageState();
}

class _EmployeeAttendancePageState extends State<EmployeeAttendancePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Employee Attendance'),
      ),
      body: EmployeeAttendance(id: widget.id, date: widget.date),
    );
  }
}
