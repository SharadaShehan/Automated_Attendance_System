import 'package:flutter/material.dart';
import 'package:frontend/models/user.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:provider/provider.dart';

class AccountDetails extends StatefulWidget {
  const AccountDetails({super.key});

  @override
  State<AccountDetails> createState() => _AccountDetailsState();
}

class _AccountDetailsState extends State<AccountDetails> {
  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    User? user = provider.user;
    return Column(
      children: [
        Text('First Name: ${user!.firstName}'),
        Text('Last Name: ${user.lastName}'),
        Text('Email: ${user.email}'),
        Text('Role: ${user.roleName}'),
        Text('Notifications: ${user.notifications}'),
      ],
    );
  }
}
