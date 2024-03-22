import 'package:flutter/material.dart';
import '../models/user.dart';

class GlobalVariablesProvider with ChangeNotifier {
  bool isLoggedIn;
  bool isAdminUser = false;
  User? user;

  GlobalVariablesProvider(
      {this.isLoggedIn = false, this.isAdminUser = false, this.user});

  void updateLogin() {
    isLoggedIn = true;
    notifyListeners();
  }

  void updateLogout() {
    isLoggedIn = false;
    notifyListeners();
  }

  void setAdmin(bool value) {
    isAdminUser = value;
    notifyListeners();
  }

  void setUser(User value) {
    user = value;
    notifyListeners();
  }
}
