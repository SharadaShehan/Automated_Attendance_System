import 'package:flutter/material.dart';

class EmployeeAttendance extends StatefulWidget {
  final int id;
  const EmployeeAttendance({super.key, required this.id});

  @override
  State<EmployeeAttendance> createState() => _EmployeeAttendanceState();
}

class _EmployeeAttendanceState extends State<EmployeeAttendance> {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text('Employee id: ${widget.id}'),
    );
  }
}
