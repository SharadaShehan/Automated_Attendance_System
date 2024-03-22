import 'package:flutter/material.dart';

class EmployeeAttendance extends StatefulWidget {
  const EmployeeAttendance({super.key});

  @override
  State<EmployeeAttendance> createState() => _EmployeeAttendanceState();
}

class _EmployeeAttendanceState extends State<EmployeeAttendance> {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: const Center(
        child: Text('Employee Attendance'),
      ),
    );
  }
}
