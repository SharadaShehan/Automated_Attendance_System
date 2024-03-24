import 'package:flutter/material.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:frontend/views/account_details.dart';
import 'package:frontend/views/own_attendance.dart';
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
    await removeUserId();
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
        title: const Padding(
          padding: EdgeInsets.fromLTRB(40, 0, 0, 0),
          child: Center(child: Text('User Home Page')),
        ),
        backgroundColor: Colors.blue.shade500,
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20.0,
        ),
        actions: [
          IconButton(
            onPressed: () => logOut(provider),
            icon: const Icon(Icons.logout),
            color: Colors.white,
            tooltip: 'Logout',
          ),
        ],
      ),
      body: selectedViewIndex == 0
          ? const OwnAttendance()
          : const AccountDetails(),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: selectedViewIndex,
        selectedItemColor: Colors.blue.shade500,
        onTap: (index) {
          setState(() {
            selectedViewIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Attendance',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_circle),
            label: 'Account',
          ),
        ],
      ),
    );
  }
}
