import 'package:flutter/material.dart';
import 'package:frontend/views/admin_home_view.dart';
import '../utilities/providers.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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
    return provider.isAdminUser
        ? Scaffold(
            appBar: AppBar(
              title: const Text('Admin Home Page'),
              actions: [
                IconButton(
                  onPressed: () => logOut(provider),
                  icon: const Icon(Icons.logout),
                  tooltip: 'Logout',
                ),
              ],
            ),
            body: const AdminHomeView())
        : Scaffold(
            appBar: AppBar(
              title: const Text('Home Page'),
            ),
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text('Welcome!'),
                ],
              ),
            ),
          );
  }
}
