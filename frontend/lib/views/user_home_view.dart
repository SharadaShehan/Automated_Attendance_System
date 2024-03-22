import 'package:flutter/material.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';

class UserHomeView extends StatefulWidget {
  const UserHomeView({super.key});

  @override
  State<UserHomeView> createState() => _UserHomeViewState();
}

class _UserHomeViewState extends State<UserHomeView> {
  int selectedViewIndex = 0;
  bool isLoading = false;

  logOut(GlobalVariablesProvider provider) async {
    setState(() {
      isLoading = true;
    });
    await removeToken();
    provider.updateLogout();
    setState(() {
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    return Scaffold(
        appBar: AppBar(
          title: const Text('User Home Page'),
          actions: [
            IconButton(
              onPressed: () => logOut(provider),
              icon: const Icon(Icons.logout),
              tooltip: 'Logout',
            ),
          ],
        ),
        body: const Text("User Home Page"));
  }
}
