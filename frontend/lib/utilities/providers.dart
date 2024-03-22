import 'package:flutter/material.dart';

class GlobalVariablesProvider with ChangeNotifier {
  bool isLoggedIn;

  GlobalVariablesProvider({this.isLoggedIn = false});

  void updateLogin() {
    isLoggedIn = true;
    notifyListeners();
  }

  void updateLogout() {
    isLoggedIn = false;
    notifyListeners();
  }
}
