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
