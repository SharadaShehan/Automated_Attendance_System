import 'package:flutter/material.dart';
import 'package:frontend/views/employee_attendance.dart';

class EmployeeAttendancePage extends StatefulWidget {
  final int id;
  const EmployeeAttendancePage({super.key, required this.id});

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
      body: EmployeeAttendance(id: widget.id),
    );
  }
}
