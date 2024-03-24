import 'package:shared_preferences/shared_preferences.dart';

Future<String> getToken() async {
  SharedPreferences store = await SharedPreferences.getInstance();
  String token = (store.getString('token') ?? '');
  return token;
}

Future<void> setToken(String token) async {
  SharedPreferences store = await SharedPreferences.getInstance();
  await store.setString('token', token);
}

Future<void> removeToken() async {
  SharedPreferences store = await SharedPreferences.getInstance();
  await store.remove('token');
}

Future<int?> getUserId() async {
  SharedPreferences store = await SharedPreferences.getInstance();
  int? userId = (store.getInt('userId'));
  return userId;
}

Future<void> setUserId(int userId) async {
  SharedPreferences store = await SharedPreferences.getInstance();
  await store.setInt('userId', userId);
}

Future<void> removeUserId() async {
  SharedPreferences store = await SharedPreferences.getInstance();
  await store.remove('userId');
}
