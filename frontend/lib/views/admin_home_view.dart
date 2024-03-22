import 'package:flutter/material.dart';
import 'package:frontend/models/user.dart';
import 'account_details.dart';

class AdminHomeView extends StatefulWidget {
  const AdminHomeView({super.key});

  @override
  State<AdminHomeView> createState() => _AdminHomeViewState();
}

class _AdminHomeViewState extends State<AdminHomeView> {
  @override
  Widget build(BuildContext context) {
    return const AccountDetails();
  }
}
