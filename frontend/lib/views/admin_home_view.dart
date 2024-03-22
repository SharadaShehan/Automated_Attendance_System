import 'package:flutter/material.dart';
import 'package:frontend/utilities/providers.dart';
import 'package:frontend/views/account_details.dart';
import 'package:frontend/views/employees_attendance.dart';
import 'package:provider/provider.dart';
import 'package:frontend/utilities/persistent_store.dart';

class AdminHomeView extends StatefulWidget {
  const AdminHomeView({super.key});

  @override
  State<AdminHomeView> createState() => _AdminHomeViewState();
}

class _AdminHomeViewState extends State<AdminHomeView> {
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
          title: const Padding(
            padding: EdgeInsets.fromLTRB(40, 0, 0, 0),
            child: Center(child: Text('Admin Home Page')),
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
            ? const EmployeesAttendance()
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
              label: 'Profile',
            ),
          ],
        ));
  }
}
