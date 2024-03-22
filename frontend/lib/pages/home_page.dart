import 'package:flutter/material.dart';
import 'package:frontend/views/admin_home_view.dart';
import '../utilities/providers.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';

import '../views/user_home_view.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    return provider.isAdminUser ? const AdminHomeView() : const UserHomeView();
  }
}
